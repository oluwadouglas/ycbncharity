from django.db import models
from django.utils import timezone
from django.conf import settings

# 11. Programs
class Program(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='programs')
    image = models.ImageField(upload_to='programs/images/', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

# 12. Partner Schools
class School(models.Model):
    name = models.CharField(max_length=200, help_text="School name")
    location = models.CharField(max_length=300, blank=True, null=True, help_text="School location/address")
    image = models.ImageField(upload_to='schools/photos/', blank=True, null=True, help_text="School photo")
    badge = models.ImageField(upload_to='schools/badges/', blank=True, null=True, help_text="School badge/logo")
    description = models.TextField(blank=True, help_text="Brief description about the school")
    partnership_date = models.DateField(blank=True, null=True, help_text="When partnership began")
    contact_person = models.CharField(max_length=200, blank=True, help_text="Contact person at school")
    contact_email = models.EmailField(blank=True, help_text="Contact email")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    website = models.CharField(max_length=200, blank=True, help_text="School website (e.g., www.school.com or https://school.com)")
    student_population = models.PositiveIntegerField(blank=True, null=True, help_text="Approximate number of students")
    is_active = models.BooleanField(default=True, help_text="Is this partnership currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Partner Schools'

    def __str__(self) -> str:
        return self.name
    
    @property
    def clubs_count(self) -> int:
        """Return count of clubs at this school"""
        return self.clubs.count()
    
    @property
    def comment(self):
        """Backward compatibility with old field name"""
        return self.description

# 1. Categories & Projects
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects")
    image = models.ImageField(upload_to="projects/images/", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    @property
    def members_count(self) -> int:
        return getattr(self, 'memberships', None).count() if hasattr(self, 'memberships') else 0


class ProjectDetails(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="details")
    challenge = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    key_objectives = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Project Details"

    def __str__(self) -> str:
        return f"Details for {self.project.title}"


# Memberships: students/partners can join a project
class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("partner", "Partner"),
        ("mentor", "Mentor"),
        ("contributor", "Contributor"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user")
        ordering = ["-joined_at"]
        verbose_name = "Project Membership"
        verbose_name_plural = "Project Memberships"

    def __str__(self) -> str:
        return f"{self.user} -> {self.project} ({self.role})"


# Project images gallery
class ProjectPhoto(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="projects/photos/")
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        return f"Photo for {self.project.title}"


# Project achievements table rows
class ProjectAchievement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="achievements")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    achieved_on = models.DateField(blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, help_text="Number/metric e.g., 50 kits, 200 students, 80% pass rate")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-achieved_on", "-created_at", "title"]

    def __str__(self) -> str:
        return f"{self.title} - {self.project.title}"


# 2. Clubs
class Club(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="clubs", blank=True, null=True, help_text="School this club belongs to (optional)")
    icon = models.ImageField(upload_to="clubs/icons/", blank=True, null=True, help_text="Club icon/logo")
    image = models.ImageField(upload_to="clubs/images/", blank=True, null=True, help_text="Club photo")
    title = models.CharField(max_length=200, help_text="Club name")
    description = models.TextField(blank=True, help_text="Club description and activities")
    location = models.CharField(max_length=200, blank=True, help_text="Club meeting location")
    meeting_schedule = models.CharField(max_length=200, blank=True, help_text="When the club meets (e.g., 'Every Friday 3-5 PM')")
    coordinator = models.CharField(max_length=200, blank=True, help_text="Club coordinator/leader")
    member_count = models.PositiveIntegerField(default=0, help_text="Number of active members")
    is_active = models.BooleanField(default=True, help_text="Is this club currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["school__name", "title"]

    def __str__(self) -> str:
        if self.school:
            return f"{self.title} ({self.school.name})"
        return self.title
    
    @property
    def comment(self):
        """Backward compatibility with old field name"""
        return self.description


# 3. Blogs (Admin only)
class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="blogs/images/", blank=True, null=True)
    author = models.CharField(max_length=150, help_text="Admin author name")
    date = models.DateField(default=timezone.now)
    content = models.TextField(help_text="Blog post content")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Blog Post (Admin)"
        verbose_name_plural = "Blog Posts (Admin)"

    def __str__(self) -> str:
        return self.title

    @property
    def details(self):
        """Backward compatibility property"""
        return self.content


# 3b. Articles (Member articles)
class Article(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to="articles/images/", blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    date = models.DateField(default=timezone.now)
    content = models.TextField(help_text="Article content")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Article (Member)"
        verbose_name_plural = "Articles (Members)"

    def __str__(self) -> str:
        return self.title

    @property
    def author_name(self) -> str:
        """Return full name or username of the author"""
        return self.author.get_full_name() or self.author.username

    @property
    def details(self):
        """Backward compatibility property"""
        return self.content


# 4. Team
class TeamMember(models.Model):
    image = models.ImageField(upload_to="team/images/", blank=True, null=True)
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    social_links = models.JSONField(default=dict, blank=True, help_text="e.g. {'whatsapp': 'https://wa.me/256...', 'facebook': '...', 'twitter': '...'}")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} - {self.title}"


# 5. Voices of Change
class VoiceOfChange(models.Model):
    image = models.ImageField(upload_to="voices/images/", blank=True, null=True)
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    quote = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Voices of Change"

    def __str__(self) -> str:
        return f"{self.name} - {self.title}"


# 6. Mentors
class Mentor(models.Model):
    image = models.ImageField(upload_to="mentors/images/", blank=True, null=True)
    name = models.CharField(max_length=150, default="Unnamed Mentor", help_text="Mentor's full name")
    title = models.CharField(max_length=200, help_text="Mentor's role/position/expertise area")
    description = models.TextField(blank=True)
    # JSONField is fully supported on PostgreSQL (JSONB)
    social_links = models.JSONField(default=dict, blank=True, null=True, help_text="Add social media links: LinkedIn, WhatsApp, Facebook, Twitter, etc.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} - {self.title}"


# 7. Photo Album
class Photo(models.Model):
    image = models.ImageField(upload_to="photos/images/")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


# 8. Downloadable Resources
class Resource(models.Model):
    icon = models.ImageField(upload_to="resources/icons/", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="resources/files/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title
    
    @property
    def file_size(self):
        """Return a human-readable file size"""
        if self.file and hasattr(self.file, 'size') and self.file.size:
            size_bytes = self.file.size
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        return "N/A"
    
    @property
    def file_type(self):
        """Return the file extension/type"""
        if self.file and self.file.name:
            import os
            _, ext = os.path.splitext(self.file.name)
            return ext.lstrip('.').upper() if ext else "FILE"
        return "FILE"


# 9. Donations (info/cards)
class Donation(models.Model):
    icon = models.ImageField(upload_to="donations/icons/", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    @property
    def progress_percent(self) -> int:
        if self.goal_amount and self.goal_amount > 0:
            try:
                return max(0, min(100, int((self.raised_amount / self.goal_amount) * 100)))
            except Exception:
                return 0
        return 0


# 10. Contact Messages
class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self) -> str:
        return f"{self.name} - {self.email}"

# 13. Impact Statistics & Content
class Impact(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    section_image = models.ImageField(upload_to='impact/sections/', blank=True, null=True)
    
    # Highlight Numbers (3 key statistics)
    highlight_1_number = models.CharField(max_length=50, blank=True, help_text="e.g., '20', '5,000+', '90%'")
    highlight_1_description = models.CharField(max_length=200, blank=True, help_text="e.g., 'New digital literacy centers established in rural schools'")
    
    highlight_2_number = models.CharField(max_length=50, blank=True, help_text="e.g., '5,000+', '90%', '15'")
    highlight_2_description = models.CharField(max_length=200, blank=True, help_text="e.g., 'Youth trained in basic computer skills and internet safety'")
    
    highlight_3_number = models.CharField(max_length=50, blank=True, help_text="e.g., '90%', '100%', '25'")
    highlight_3_description = models.CharField(max_length=200, blank=True, help_text="e.g., 'of trained youth report increased confidence in using digital tools'")
    
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Impact Section'
        verbose_name_plural = 'Impact Sections'

    def __str__(self):
        return self.title


class ImpactCounter(models.Model):
    COUNTER_TYPES = [
        ('people', 'People Helped'),
        ('projects', 'Projects Completed'),
        ('schools', 'Schools Reached'),
        ('communities', 'Communities Served'),
        ('volunteers', 'Active Volunteers'),
        ('funds', 'Funds Raised'),
        ('custom', 'Custom Counter'),
    ]
    
    title = models.CharField(max_length=150)
    counter_type = models.CharField(max_length=20, choices=COUNTER_TYPES, default='custom')
    target_number = models.PositiveIntegerField(help_text="The number to count up to")
    suffix = models.CharField(max_length=10, blank=True, help_text="e.g., '+', 'K', 'M', '%'")
    prefix = models.CharField(max_length=10, blank=True, help_text="e.g., '$', '#'")
    icon_class = models.CharField(max_length=50, default='fas fa-heart', help_text="FontAwesome icon class")
    color_theme = models.CharField(max_length=20, default='primary', choices=[
        ('primary', 'Primary Green'),
        ('secondary', 'Golden Yellow'),
        ('success', 'Success Green'),
        ('info', 'Info Blue'),
        ('warning', 'Warning Orange'),
        ('danger', 'Danger Red'),
        ('custom', 'Custom Color'),
    ])
    custom_color = models.CharField(max_length=7, blank=True, help_text="Hex color code (e.g., #FF5733)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Impact Counter'
        verbose_name_plural = 'Impact Counters'

    def __str__(self):
        return f"{self.title}: {self.prefix}{self.target_number}{self.suffix}"

    @property
    def display_color(self):
        """Return the color to use for this counter"""
        if self.color_theme == 'custom' and self.custom_color:
            return self.custom_color
        
        color_map = {
            'primary': '#1A685B',
            'secondary': '#FFAC00',
            'success': '#28a745',
            'info': '#17a2b8',
            'warning': '#ffc107',
            'danger': '#dc3545',
        }
        return color_map.get(self.color_theme, '#1A685B')


# 14. Spotlight System - Best Performing Categories
class SpotlightCategory(models.Model):
    CATEGORY_TYPES = [
        ('clubs', 'Best Performing Clubs'),
        ('mentors', 'Best Performing Mentors'),
        ('projects', 'Best Performing Projects'),
        ('programs', 'Best Performing Programs'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_TYPES, unique=True)
    title = models.CharField(max_length=200, help_text="Display title for this spotlight section")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Optional subtitle/description")
    icon_class = models.CharField(max_length=50, default='fas fa-star', help_text="FontAwesome icon class")
    background_color = models.CharField(max_length=7, default='#1A685B', help_text="Hex color code for section background")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order on spotlight page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Spotlight Category'
        verbose_name_plural = 'Spotlight Categories'

    def __str__(self):
        return self.get_name_display()


class SpotlightItem(models.Model):
    PERFORMANCE_LEVELS = [
        ('excellent', 'Excellent Performance'),
        ('outstanding', 'Outstanding Performance'),
        ('exceptional', 'Exceptional Performance'),
        ('top_performer', 'Top Performer'),
    ]
    
    category = models.ForeignKey(SpotlightCategory, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, help_text="Role, location, or brief description")
    description = models.TextField(help_text="Detailed description of achievements and performance")
    image = models.ImageField(upload_to='spotlight/images/', blank=True, null=True)
    
    # Performance metrics
    performance_level = models.CharField(max_length=20, choices=PERFORMANCE_LEVELS, default='excellent')
    achievement_score = models.PositiveIntegerField(default=0, help_text="Numeric score for ranking (higher = better)")
    key_achievements = models.TextField(blank=True, help_text="List key achievements (one per line)")
    
    # Additional details
    location = models.CharField(max_length=200, blank=True, help_text="Location or school (for clubs/projects)")
    contact_info = models.JSONField(default=dict, blank=True, help_text="Contact details or social links")
    
    # Display options
    is_featured = models.BooleanField(default=False, help_text="Show as featured item with special styling")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order within category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order', '-achievement_score', 'title']
        verbose_name = 'Spotlight Item'
        verbose_name_plural = 'Spotlight Items'

    def __str__(self):
        return f"{self.category.get_name_display()}: {self.title}"

    @property
    def performance_badge_color(self):
        """Return color for performance level badge"""
        colors = {
            'excellent': '#28a745',
            'outstanding': '#ffc107',
            'exceptional': '#fd7e14',
            'top_performer': '#dc3545',
        }
        return colors.get(self.performance_level, '#28a745')

    @property
    def achievements_list(self):
        """Return achievements as a list"""
        if self.key_achievements:
            return [achievement.strip() for achievement in self.key_achievements.split('\n') if achievement.strip()]
        return []


class SpotlightStats(models.Model):
    """Statistics and counters for the spotlight page"""
    title = models.CharField(max_length=150)
    value = models.CharField(max_length=50, help_text="e.g., '150+', '95%', '2.5K'")
    description = models.CharField(max_length=200)
    icon_class = models.CharField(max_length=50, default='fas fa-trophy')
    color = models.CharField(max_length=7, default='#1A685B', help_text="Hex color code")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Spotlight Statistic'
        verbose_name_plural = 'Spotlight Statistics'

    def __str__(self):
        return f"{self.title}: {self.value}"


# 15. Newsletter Subscription
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True, help_text="Subscriber's email address")
    name = models.CharField(max_length=150, blank=True, help_text="Optional subscriber name")
    is_active = models.BooleanField(default=True, help_text="Whether subscription is active")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields for better management
    subscription_source = models.CharField(max_length=50, default='website', help_text="Where they subscribed from")
    interests = models.CharField(max_length=200, blank=True, help_text="Areas of interest (comma-separated)")
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        name_part = f" ({self.name})" if self.name else ""
        return f"{self.email}{name_part} - {status}"
    
    def deactivate(self):
        """Deactivate subscription (soft delete)"""
        self.is_active = False
        self.save()
