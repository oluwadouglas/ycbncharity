# --- New Views for Navigation Pages ---
from .models import Project, Club, Category, Program, School, VoiceOfChange, TeamMember, Donation, Mentor, Impact, ImpactCounter, ContactMessage, Article, Opportunity, SpotlightCategory, SpotlightItem, SpotlightStats, ProjectMembership, ProjectPhoto, ProjectAchievement, NewsletterSubscription, Resource, Photo
from .forms import ProjectForm, ClubForm, ProgramForm, SchoolForm, NewsletterSubscriptionForm, OpportunityApplicationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import login as auth_login
from .forms import RegistrationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def _is_member(user) -> bool:
    """Return True if user belongs to 'member' group."""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='member').exists()

def about_us(request):
    voices = VoiceOfChange.objects.all()
    context = {
        'voices': voices,
        'page_title': 'About Us | YCBF',
    }
    return render(request, 'charity/about_us.html', context)

def projects(request):
    projects_list = Project.objects.all().prefetch_related('memberships').order_by('-created_at', 'title')
    
    # Pagination - 6 projects per page
    paginator = Paginator(projects_list, 6)
    page = request.GET.get('page')
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        projects = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        projects = paginator.page(paginator.num_pages)
    
    context = {
        'projects': projects,
        'page_title': 'Projects | YCBF',
    }
    return render(request, 'charity/projects.html', context)

def project_detail(request, project_id):
    """Project details page"""
    project = get_object_or_404(Project, id=project_id)
    # Access optional one-to-one details if present
    details = getattr(project, 'details', None)
    
    # Initialize context with common data
    context = {
        'page_title': f'{project.title} | Project - YCBF',
        'project': project,
        'details': details,
        'members': ProjectMembership.objects.filter(project=project).select_related('user'),
        'photos': ProjectPhoto.objects.filter(project=project),
        'achievements': ProjectAchievement.objects.filter(project=project),
        'is_member': False,
        'has_pending_request': False,
        'membership_request': None,
    }
    
    # Check membership and request status for authenticated users
    if request.user.is_authenticated:
        context['is_member'] = ProjectMembership.objects.filter(
            project=project, 
            user=request.user
        ).exists()
        
        # Check for pending requests
        pending_request = ProjectMembershipRequest.objects.filter(
            project=project, 
            user=request.user,
            status='pending'
        ).first()
        
        if pending_request:
            context['has_pending_request'] = True
            context['membership_request'] = pending_request
    return render(request, 'charity/project-details.html', context)

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('charity:projects')
    else:
        form = ProjectForm()
    return render(request, 'charity/add_project.html', {'form': form})

def clubs(request):
    clubs_list = Club.objects.all().order_by('title')
    
    # Pagination - 6 clubs per page
    paginator = Paginator(clubs_list, 6)
    page = request.GET.get('page')
    
    try:
        clubs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        clubs = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        clubs = paginator.page(paginator.num_pages)
    
    context = {
        'clubs': clubs,
        'page_title': 'Clubs | YCBF',
    }
    return render(request, 'charity/clubs.html', context)

def add_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('charity:clubs')
    else:
        form = ClubForm()
    return render(request, 'charity/add_club.html', {'form': form})


def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    context = {
        'page_title': f"{club.title} | Club - YCBF",
        'club': club,
    }
    return render(request, 'charity/club-details.html', context)

def programs(request):
    cat_id = request.GET.get('category')
    if cat_id:
        categories = Category.objects.filter(id=cat_id).prefetch_related('programs')
    else:
        categories = Category.objects.prefetch_related('programs').all()
    context = {
        'categories': categories,
        'page_title': 'Programs | YCBF',
    }
    return render(request, 'charity/programs.html', context)

def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('charity:programs')
    else:
        form = ProgramForm()
    return render(request, 'charity/add_program.html', {'form': form})

def program_detail(request, program_id):
    """Program details page"""
    program = get_object_or_404(Program, id=program_id)
    # Related programs from the same category (excluding current)
    related_programs = Program.objects.filter(category=program.category).exclude(id=program.id)[:6]
    # All categories for quick-pick navigation
    categories = Category.objects.all()
    context = {
        'page_title': f"{program.title} | Program - YCBF",
        'program': program,
        'related_programs': related_programs,
        'categories': categories,
    }
    return render(request, 'charity/program-details.html', context)

def partner_schools(request):
    schools_list = School.objects.all().order_by('name')
    
    # Pagination - 4 schools per page
    paginator = Paginator(schools_list, 4)
    page = request.GET.get('page')
    
    try:
        schools = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        schools = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        schools = paginator.page(paginator.num_pages)
    
    context = {
        'schools': schools,
        'page_title': 'Partner Schools | YCBF',
    }
    return render(request, 'charity/partner_schools.html', context)


def school_detail(request, school_id):
    """School details page showing school info and associated clubs"""
    school = get_object_or_404(School, id=school_id)
    # Get all clubs associated with this school
    clubs = Club.objects.filter(school=school)
    context = {
        'page_title': f'{school.name} | Partner School - YCBF',
        'school': school,
        'clubs': clubs,
    }
    return render(request, 'charity/school_detail.html', context)

# Home page views
def home(request):
    """Main home page view"""
    # Impact data
    impact_sections = Impact.objects.filter(is_active=True).order_by('order', 'title')
    impact_counters = ImpactCounter.objects.filter(is_active=True).order_by('order', 'title')

    # Spotlight data
    spotlight_categories = SpotlightCategory.objects.filter(is_active=True).order_by('order', 'name')
    for category in spotlight_categories:
        category.active_items = category.items.filter(is_active=True).order_by('order', '-achievement_score', 'title')
    spotlight_stats = SpotlightStats.objects.filter(is_active=True).order_by('order', 'title')

    context = {
        'page_title': 'Home - YCBF Charity',
        'youth_leaders': TeamMember.objects.all(),
        'youth_projects': Project.objects.all(),
        'testimonials': VoiceOfChange.objects.all(),
        'mentors': Mentor.objects.all()[:6],  # Limit to 6 mentors for better display
        # Aggregated sections for Home
        'projects': Project.objects.all(),
        'clubs': Club.objects.all(),
        'categories': Category.objects.prefetch_related('programs').all(),
        'schools': School.objects.all(),
        'voices': VoiceOfChange.objects.all(),
        'voices_of_change': VoiceOfChange.objects.all(),  # Add this for the testimonials section
        'donations': Donation.objects.all(),
        # Impact context
        'impact': impact_sections,
        'impact_counter': impact_counters,
        # Spotlight context
        'spotlight_categories': spotlight_categories,
        'spotlight_stats': spotlight_stats,
        # Blog (latest admin posts for News & Articles)
'articles': Article.objects.filter(is_published=True).order_by('-date', '-created_at')[:6],
        # Downloadable resources
        'downloadable_resources': Resource.objects.all()[:6],  # Limit to 6 for home page
        # Gallery
'photos': Photo.objects.all()[:8],
        # Opportunities (latest)
        'opportunities': Opportunity.objects.filter(is_published=True).order_by('-posted_at')[:4],
    }
    return render(request, 'charity/index.html', context)


# Main pages
def about(request):
    """About us page"""
    # Spotlight metrics and donations to support dynamic sections
    spotlight_stats = SpotlightStats.objects.filter(is_active=True).order_by('order', 'title')
    
    # Impact data
    impact_sections = Impact.objects.filter(is_active=True).order_by('order', 'title')
    impact_counters = ImpactCounter.objects.filter(is_active=True).order_by('order', 'title')
    
    context = {
        'page_title': 'About Us - YCBF Charity',
        'youth_leaders': TeamMember.objects.all(),
        'testimonials': VoiceOfChange.objects.all(),
        'youth_projects': Project.objects.all(),
        'voices': VoiceOfChange.objects.all(),
        'mentors': Mentor.objects.all()[:6],  # Add mentors to about page
        # Add missing data for about page sections
        'projects': Project.objects.all(),
        'clubs': Club.objects.all(),
        'categories': Category.objects.prefetch_related('programs').all(),
        'schools': School.objects.all(),
        # Downloadable resources
        'downloadable_resources': Resource.objects.all(),
        # Donations and Spotlight
        'donations': Donation.objects.all(),
        'spotlight_stats': spotlight_stats,
        # Impact context
        'impact': impact_sections,
        'impact_counter': impact_counters,
    }
    return render(request, 'charity/about.html', context)

def contact(request):
    """Contact page"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                message=message_text,
            )
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('charity:contact')
        else:
            messages.error(request, 'Please fill in name, email, and message before submitting the form.')

    context = {
        'page_title': 'Contact Us - YCBF Charity'
    }
    return render(request, 'charity/contact.html', context)

def faq(request):
    """FAQ page"""
    context = {
        'page_title': 'FAQ - YCBF Charity'
    }
    return render(request, 'charity/faq.html', context)

def gallery(request):
    """Gallery page"""
    context = {
        'page_title': 'Gallery - YCBF Charity'
    }
    return render(request, 'charity/gallery.html', context)

def pricing(request):
    """Pricing page"""
    context = {
        'page_title': 'Pricing - YCBF Charity'
    }
    return render(request, 'charity/pricing.html', context)

def error_page(request):
    """Error page"""
    context = {
        'page_title': '404 Error - YCBF Charity'
    }
    return render(request, 'charity/error.html', context)

def impact(request):
    """Impact page showing YCBF's impact and achievements"""
    impact_sections = Impact.objects.filter(is_active=True).order_by('order', 'title')
    impact_counters = ImpactCounter.objects.filter(is_active=True).order_by('order', 'title')
    
    context = {
        'page_title': 'Our Impact - YCBF Charity',
        'impact': impact_sections,
        'impact_counter': impact_counters,
    }
    return render(request, 'charity/impact.html', context)

# Opportunities pages (Admin managed)
def opportunities(request):
    """Opportunities listing page - Admin managed (jobs, scholarships, etc.)"""
    opp_type = request.GET.get('type')
    qs = Opportunity.objects.filter(is_published=True)
    if opp_type:
        qs = qs.filter(opportunity_type=opp_type)
    opportunities = qs.order_by('-posted_at')
    context = {
        'page_title': 'Opportunities - YCBF Charity',
        'opportunities': opportunities,
    }
    return render(request, 'charity/opportunities.html', context)


def opportunity_detail(request, opp_id: int):
    opp = get_object_or_404(Opportunity, id=opp_id, is_published=True)
    return render(request, 'charity/opportunity_detail.html', {
        'page_title': f'{opp.title} | Opportunity - YCBF',
        'opportunity': opp,
    })


def opportunity_apply(request, opp_id: int):
    opp = get_object_or_404(Opportunity, id=opp_id, is_published=True)
    if request.method == 'POST':
        form = OpportunityApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.opportunity = opp
            app.save()
            messages.success(request, 'Application submitted successfully. We will get back to you soon.')
            return redirect('charity:opportunity_detail', opp_id=opp.id)
    else:
        form = OpportunityApplicationForm()
    return render(request, 'charity/opportunity_apply.html', {
        'page_title': f'Apply: {opp.title} | Opportunity - YCBF',
        'opportunity': opp,
        'form': form,
    })


# Backward compatibility routes for old blog URLs
def blog(request):
    from django.shortcuts import redirect
    return redirect('charity:opportunities')


def blog_details(request, post_id):
    from django.shortcuts import redirect
    return redirect('charity:opportunities')
# Article pages (Member articles)
def articles(request):
    """Article listing page - Member articles"""
    articles = Article.objects.filter(is_published=True).order_by('-date', '-created_at')
    context = {
        'page_title': 'Articles - YCBF Charity',
        'articles': articles,
        'is_member': _is_member(request.user),
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'charity/articles.html', context)

def article_details(request, post_id):
    """Article details - Member article"""
    article = get_object_or_404(Article, id=post_id, is_published=True)
    context = {
        'page_title': f'Article: {article.title} - YCBF Charity',
        'post': article,  # Use 'post' for template consistency
        'article': article,  # Keep 'article' for backward compatibility
        'is_member': _is_member(request.user),
    }
    return render(request, 'charity/article-details.html', context)

# Donation pages
def donations(request):
    """Donations listing page"""
    donations = Donation.objects.all()
    context = {
        'page_title': 'Donations - YCBF Charity',
        'donations': donations,
    }
    return render(request, 'charity/donation.html', context)

def donation_details(request, donation_id):
    """Donation details page"""
    context = {
        'page_title': f'Donation {donation_id} Details - YCBF Charity',
        'donation_id': donation_id
    }
    return render(request, 'charity/donation-details.html', context)

def donate_now(request):
    """Donate now page"""
    context = {
        'page_title': 'Donate Now - YCBF Charity'
    }
    return render(request, 'charity/donate-now.html', context)

# Team/Volunteer pages
def team(request):
    """Team/Volunteers listing page"""
    context = {
        'page_title': 'Our Team - YCBF Charity'
    }
    return render(request, 'charity/team.html', context)

def team_details(request, member_id):
    """Team member details page"""
    context = {
        'page_title': f'Team Member {member_id} - YCBF Charity',
        'member_id': member_id
    }
    return render(request, 'charity/team-details.html', context)

def add_team(request):
    """Add team member / Become volunteer page"""
    context = {
        'page_title': 'Become a Volunteer - YCBF Charity'
    }
    return render(request, 'charity/add-team.html', context)

def testimonial(request):
    """Testimonials page"""
    context = {
        'page_title': 'Testimonials - YCBF Charity',
        'testimonials': VoiceOfChange.objects.all(),
        'youth_leaders': TeamMember.objects.all(),
        'youth_projects': Project.objects.all(),
    }
    return render(request, 'charity/testimonial.html', context)

# Shop pages
def shop(request):
    """Shop listing page"""
    context = {
        'page_title': 'Shop - YCBF Charity'
    }
    return render(request, 'charity/shop.html', context)

def shop_details(request, product_id):
    """Product details page"""
    context = {
        'page_title': f'Product {product_id} - YCBF Charity',
        'product_id': product_id
    }
    return render(request, 'charity/shop-details.html', context)

def cart(request):
    """Shopping cart page"""
    context = {
        'page_title': 'Cart - YCBF Charity'
    }
    return render(request, 'charity/cart.html', context)

def checkout(request):
    """Checkout page"""
    context = {
        'page_title': 'Checkout - YCBF Charity'
    }
    return render(request, 'charity/checkout.html', context)

def wishlist(request):
    """Wishlist page"""
    context = {
        'page_title': 'Wishlist - YCBF Charity'
    }
    return render(request, 'charity/wishlist.html', context)

# Event pages
def event_details(request, event_id):
    """Event details page"""
    context = {
        'page_title': f'Event {event_id} - YCBF Charity',
        'event_id': event_id
    }
    return render(request, 'charity/event-details.html', context)

# Spotlight page
def spotlight(request):
    """Spotlight page"""
    # Filter active categories and their active items
    spotlight_categories = SpotlightCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    # Add active items to each category
    for category in spotlight_categories:
        category.active_items = category.items.filter(is_active=True).order_by('order', '-achievement_score', 'title')
    
    # Filter active statistics
    spotlight_stats = SpotlightStats.objects.filter(is_active=True).order_by('order', 'title')
    
    # Debug: Check if data exists
    print(f"Spotlight categories count: {spotlight_categories.count()}")
    print(f"Spotlight stats count: {spotlight_stats.count()}")
    for stat in spotlight_stats:
        print(f"Stat: {stat.title} - {stat.value} - Active: {stat.is_active}")
    
    context = {
        'page_title': 'Spotlight - YCBF Charity',
        'spotlight_categories': spotlight_categories,
        'spotlight_stats': spotlight_stats,
    }
    return render(request, 'charity/spotlight.html', context)

# ---- Member article management ----

@login_required(login_url='/admin/login/')
def add_article(request):
    if not _is_member(request.user):
        messages.error(request, 'You do not have permission to add articles.')
        return redirect('charity:articles')
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article: Article = form.save(commit=False)
            article.author = request.user  # Set the actual user as author
            article.save()
            messages.success(request, 'Article created successfully.')
            return redirect('charity:article_details', post_id=article.id)
    else:
        form = ArticleForm()
    return render(request, 'charity/article_form.html', {
        'form': form,
        'page_title': 'Add Article - YCBF',
        'is_edit': False,
    })

@login_required(login_url='/admin/login/')
def edit_article(request, post_id):
    if not _is_member(request.user):
        messages.error(request, 'You do not have permission to edit articles.')
        return redirect('charity:articles')
    article = get_object_or_404(Article, id=post_id)
    # Only allow editing own articles or if user is admin
    if article.author != request.user and not request.user.is_staff:
        messages.error(request, 'You can only edit your own articles.')
        return redirect('charity:articles')
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully.')
            return redirect('charity:article_details', post_id=article.id)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'charity/article_form.html', {
        'form': form,
        'page_title': f'Edit: {article.title} - YCBF',
        'is_edit': True,
        'article': article,
    })

# ---- Authentication: public registration ----
def register(request):
    """Public user registration. Creates an account and logs the user in."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically add user to the 'member' group
            member_group, created = Group.objects.get_or_create(name='member')
            user.groups.add(member_group)
            messages.success(request, 'Welcome! Your account has been created. You can now write articles!')
            auth_login(request, user)
            return redirect('charity:home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {
        'form': form,
        'page_title': 'Join Now - YCBF'
    })

# ---- Project membership actions ----
@login_required(login_url='/login/')
def request_join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        role = request.POST.get('role', 'student')
        message = request.POST.get('message', '')
        
        # Check if user already has a pending request
        existing_request = ProjectMembershipRequest.objects.filter(
            project=project, 
            user=request.user,
            status='pending'
        ).exists()
        
        if existing_request:
            messages.info(request, 'You already have a pending request to join this project.')
        else:
            # Check if user is already a member
            is_member = ProjectMembership.objects.filter(
                project=project, 
                user=request.user
            ).exists()
            
            if is_member:
                messages.info(request, 'You are already a member of this project.')
            else:
                # Create new request
                ProjectMembershipRequest.objects.create(
                    project=project,
                    user=request.user,
                    role=role,
                    message=message
                )
                messages.success(request, 'Your request to join this project has been submitted for review.')
        
        return redirect('charity:project_detail', project_id=project.id)
    
    # GET request - show request form
    return render(request, 'charity/project_request_join.html', {
        'project': project,
        'role_choices': dict(ProjectMembership.ROLE_CHOICES)
    })

@login_required(login_url='/login/')
def cancel_join_request(request, request_id):
    join_request = get_object_or_404(
        ProjectMembershipRequest, 
        id=request_id, 
        user=request.user,
        status='pending'  # Can only cancel pending requests
    )
    
    if request.method == 'POST':
        project_id = join_request.project.id
        join_request.delete()
        messages.success(request, 'Your join request has been cancelled.')
        return redirect('charity:project_detail', project_id=project_id)
    
    return redirect('charity:project_detail', project_id=join_request.project.id)

@login_required(login_url='/login/')
def leave_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        deleted, _ = ProjectMembership.objects.filter(project=project, user=request.user).delete()
        if deleted:
            messages.success(request, 'You have left this project.')
        else:
            messages.info(request, 'You were not a member of this project.')
    return redirect('charity:project_detail', project_id=project.id)

# ---- Member management ----
@login_required(login_url='/admin/login/')
def become_member(request):
    """Allow authenticated users to join the member group"""
    if _is_member(request.user):
        messages.info(request, 'You are already a member and can write articles!')
        return redirect('charity:articles')
    
    if request.method == 'POST':
        # Add user to member group
        member_group, created = Group.objects.get_or_create(name='member')
        request.user.groups.add(member_group)
        messages.success(request, 'Welcome to YCBF! You are now a member and can write articles.')
        return redirect('charity:articles')
    
    context = {
        'page_title': 'Become a Member - YCBF Charity'
    }
    return render(request, 'charity/become_member.html', context)

# ---- Profile page ----
@login_required(login_url='/login/')
def profile(request):
    """User profile page"""
    context = {
        'page_title': f'Profile | {request.user.get_full_name() or request.user.username} | YCBF',
        'user': request.user,
        'is_member': _is_member(request.user),
    }
    return render(request, 'charity/profile.html', context)

# ---- Volunteer Page ----
def volunteer(request):
    """
    Volunteer page that displays information about volunteering opportunities
    and a form for users to sign up as volunteers.
    """
    context = {
        'title': 'Volunteer With Us',
        'page_header': 'Join Our Volunteer Team',
        'page_subheader': 'Make a difference in your community',
    }
    return render(request, 'charity/volunteer.html', context)

# ---- Newsletter subscription ----
def newsletter_subscribe(request):
    """Handle newsletter subscription form submission"""
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            try:
                subscription = form.save()
                messages.success(request, 'Thank you for subscribing to our newsletter! You will receive updates about our programs and initiatives.')
            except Exception as e:
                messages.error(request, 'An error occurred while processing your subscription. Please try again.')
        else:
            # Get form errors and display them
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(error)
            error_msg = ' '.join(error_messages) if error_messages else 'Please check your input and try again.'
            messages.error(request, error_msg)
    
    # Redirect back to the referring page or home if no referrer
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)
