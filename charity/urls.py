from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'charity'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Main pages
    path('about/', views.about, name='about'),
    path('about-us/', views.about_us, name='about_us'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/join/', views.join_project, name='join_project'),
    path('projects/<int:project_id>/leave/', views.leave_project, name='leave_project'),
    path('projects/add/', views.add_project, name='add_project'),
    path('clubs/', views.clubs, name='clubs'),
    path('clubs/add/', views.add_club, name='add_club'),
    path('programs/', views.programs, name='programs'),
    path('programs/<int:program_id>/', views.program_detail, name='program_detail'),
    path('programs/add/', views.add_program, name='add_program'),
    path('partner-schools/', views.partner_schools, name='partner_schools'),
    path('partner-schools/<int:school_id>/', views.school_detail, name='school_detail'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('gallery/', views.gallery, name='gallery'),
    path('pricing/', views.pricing, name='pricing'),
    path('error/', views.error_page, name='error'),
    path('impact/', views.impact, name='impact'),
    path('spotlight/', views.spotlight, name='spotlight'),
    
    # Blog pages (Admin posts)
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_details, name='blog_details'),
    
    # Articles (Member articles)
    path('articles/', views.articles, name='articles'),
    path('articles/<int:post_id>/', views.article_details, name='article_details'),
    path('articles/add/', views.add_article, name='add_article'),
    path('articles/<int:post_id>/edit/', views.edit_article, name='edit_article'),
    
    # Donation pages
    path('donations/', views.donations, name='donations'),
    path('donations/<int:donation_id>/', views.donation_details, name='donation_details'),
    path('donate-now/', views.donate_now, name='donate_now'),
    
    # Team/Volunteer pages
    path('team/', views.team, name='team'),
    path('team/<int:member_id>/', views.team_details, name='team_details'),
    path('add-team/', views.add_team, name='add_team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    
    # Shop pages
    path('shop/', views.shop, name='shop'),
    path('shop/<int:product_id>/', views.shop_details, name='shop_details'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('wishlist/', views.wishlist, name='wishlist'),
    
    # Event pages
    path('event/<int:event_id>/', views.event_details, name='event_details'),

    # Auth: public registration
    path('register/', views.register, name='register'),
    path('become-member/', views.become_member, name='become_member'),
    
    # User profile
    path('profile/', views.profile, name='profile'),
    
    # Volunteer page
    path('volunteer/', views.volunteer, name='volunteer'),
    
    # Newsletter subscription
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
# Serve media files in development
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
