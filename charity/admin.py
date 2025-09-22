from django.contrib import admin
from .models import (
    Category,
    Project,
    ProjectDetails,
    ProjectMembership,
    ProjectPhoto,
    ProjectAchievement,
    Club,
    School,
    BlogPost,
    TeamMember,
    VoiceOfChange,
    Mentor,
    Photo,
    Resource,
    Donation,
    ContactMessage,
    Program,
    Impact,
    ImpactCounter,
    SpotlightCategory,
    SpotlightItem,
    SpotlightStats,
)


# Register your models here.

# Contact Messages (updated fields: no subject/is_read)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "phone_number", "message")
    readonly_fields = ("created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "members_count_admin", "created_at", "updated_at")
    list_filter = ("category",)
    search_fields = ("title", "description")

    def members_count_admin(self, obj):
        return obj.memberships.count()
    members_count_admin.short_description = "Members"


@admin.register(ProjectDetails)
class ProjectDetailsAdmin(admin.ModelAdmin):
    list_display = ("project", "updated_at")
    search_fields = ("project__title", "challenge", "solution", "key_objectives")


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "role", "joined_at")
    list_filter = ("role", "joined_at")
    search_fields = ("project__title", "user__username", "user__email")


@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(admin.ModelAdmin):
    list_display = ("project", "uploaded_at", "caption")
    search_fields = ("project__title", "caption")


@admin.register(ProjectAchievement)
class ProjectAchievementAdmin(admin.ModelAdmin):
    list_display = ("project", "title", "value", "achieved_on", "created_at")
    list_filter = ("achieved_on",)
    search_fields = ("project__title", "title", "description", "value")


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'student_population', 'partnership_date', 'clubs_count_display', 'is_active', 'created_at')
    list_filter = ('is_active', 'partnership_date', 'created_at', 'location')
    search_fields = ('name', 'location', 'contact_person', 'contact_email')
    readonly_fields = ('created_at', 'updated_at', 'clubs_count_display')
    list_editable = ('is_active',)
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location', 'description', 'is_active')
        }),
        ('Partnership Details', {
            'fields': ('partnership_date', 'student_population'),
            'description': 'Information about when the partnership began and school size'
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_email', 'contact_phone', 'website'),
            'description': 'Primary contact details for this school'
        }),
        ('Media', {
            'fields': ('image', 'badge'),
            'classes': ('collapse',),
            'description': 'School photo and badge/logo'
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'clubs_count_display'),
            'classes': ('collapse',),
            'description': 'Read-only system information'
        })
    )
    
    def clubs_count_display(self, obj):
        count = obj.clubs.count()
        if count == 0:
            return "No clubs"
        elif count == 1:
            return "1 club"
        else:
            return f"{count} clubs"
    clubs_count_display.short_description = 'Associated Clubs'
    clubs_count_display.admin_order_field = 'clubs__count'


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("title", "school", "coordinator", "member_count", "is_active", "created_at")
    list_filter = ("is_active", "school", "created_at")
    search_fields = ("title", "description", "coordinator", "school__name")
    list_editable = ("is_active", "member_count")
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('school__name', 'title')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'school', 'description', 'is_active')
        }),
        ('Club Details', {
            'fields': ('coordinator', 'member_count', 'meeting_schedule', 'location'),
            'description': 'Operational details about the club'
        }),
        ('Media', {
            'fields': ('icon', 'image'),
            'classes': ('collapse',),
            'description': 'Club icon/logo and photo'
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date", "created_at")
    list_filter = ("date",)
    search_fields = ("title", "author", "details")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "created_at")
    search_fields = ("name", "title")


@admin.register(VoiceOfChange)
class VoiceOfChangeAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "created_at")
    search_fields = ("name", "title", "quote")
    fields = ("image", "name", "title", "quote")


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "created_at")
    search_fields = ("name", "title", "description")
    fieldsets = (
        (None, {
            'fields': ('image', 'name', 'title', 'description')
        }),
        ('Social Media Links', {
            'fields': ('social_links',),
            'description': 'Add social media links in JSON format. Example: {"linkedin": "https://linkedin.com/in/username", "whatsapp": "https://wa.me/256700000000", "facebook": "https://facebook.com/username", "twitter": "https://twitter.com/username"}'
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Add placeholder text for social_links field
        if 'social_links' in form.base_fields:
            form.base_fields['social_links'].widget.attrs.update({
                'placeholder': '{"linkedin": "https://linkedin.com/in/username", "whatsapp": "https://wa.me/256700000000", "facebook": "https://facebook.com/username", "twitter": "https://twitter.com/username"}',
                'rows': 4,
                'style': 'width: 100%; font-family: monospace;'
            })
        return form


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "description")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "description")


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("title", "goal_amount", "raised_amount", "created_at")
    list_editable = ("goal_amount", "raised_amount")
    search_fields = ("title", "description")
    list_filter = ("created_at",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "updated_at")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(Impact)
class ImpactAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "subtitle", "description")
    list_editable = ("order", "is_active")
    ordering = ("order", "title")
    
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'description', 'section_image')
        }),
        ('Key Highlights', {
            'fields': (
                ('highlight_1_number', 'highlight_1_description'),
                ('highlight_2_number', 'highlight_2_description'),
                ('highlight_3_number', 'highlight_3_description'),
            ),
            'description': 'Add up to 3 key statistics that highlight the impact of this section. Numbers will be displayed with cool animations.'
        }),
        ('Display Options', {
            'fields': ('order', 'is_active'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ImpactCounter)
class ImpactCounterAdmin(admin.ModelAdmin):
    list_display = ("title", "counter_type", "target_number", "prefix", "suffix", "order", "is_active")
    list_filter = ("counter_type", "color_theme", "is_active")
    search_fields = ("title",)
    list_editable = ("order", "is_active", "target_number")
    ordering = ("order", "title")
    
    fieldsets = (
        (None, {
            'fields': ('title', 'counter_type', 'target_number', 'prefix', 'suffix')
        }),
        ('Display Options', {
            'fields': ('icon_class', 'color_theme', 'custom_color', 'order', 'is_active'),
            'description': 'Configure how this counter appears on the impact page'
        }),
    )


@admin.register(SpotlightCategory)
class SpotlightCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(SpotlightItem)
class SpotlightItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "updated_at")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(SpotlightStats)
class SpotlightStatsAdmin(admin.ModelAdmin):
    list_display = ("title", "value", "order", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    list_editable = ("order", "is_active")
    ordering = ("order", "title")
    
    fieldsets = (
        (None, {
            'fields': ('title', 'value', 'description', 'icon_class', 'color')
        }),
        ('Display Options', {
            'fields': ('order', 'is_active'),
            'description': 'Configure how this statistic appears on the spotlight page'
        }),
    )
