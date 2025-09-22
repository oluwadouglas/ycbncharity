from django.core.management.base import BaseCommand
from django.utils import timezone

from charity.models import (
    Category,
    Program,
    School,
    Club,
    BlogPost,
    Donation,
    Impact,
    ImpactCounter,
)


class Command(BaseCommand):
    help = "Seed sample data for development: categories, programs, partner schools, clubs, blog posts, donations, impact counters. Safe to run multiple times."

    def handle(self, *args, **options):
        created_total = 0

        # Categories
        categories = [
            ("Skills Development",),
            ("Community Projects",),
            ("Mentorship & Networking",),
        ]
        cat_objs = {}
        for (name,) in categories:
            obj, created = Category.objects.get_or_create(name=name)
            cat_objs[name] = obj
            created_total += int(created)

        # Programs
        program_defs = [
            ("Digital Literacy Bootcamp", "Skills Development",
             "Hands-on training in basic computer skills, office tools, and safe internet use."),
            ("Entrepreneurship for Youth", "Skills Development",
             "Incubation-style program covering ideation, lean canvas, and pitching."),
            ("Community Clean Water Initiative", "Community Projects",
             "Student-led project to prototype low-cost water filtration and hygiene campaigns."),
        ]
        for title, cat_name, desc in program_defs:
            Program.objects.get_or_create(
                title=title,
                defaults={
                    "category": cat_objs[cat_name],
                    "description": desc,
                },
            )

        # Partner Schools
        schools = [
            {
                "name": "Kampala High School",
                "location": "Kampala, Uganda",
                "description": "Urban secondary school partnering on digital literacy and leadership programs.",
                "website": "https://example.edu",
                "student_population": 1200,
            },
            {
                "name": "Gulu Community SS",
                "location": "Gulu, Northern Uganda",
                "description": "Community-focused school active in social impact projects.",
                "website": "",
                "student_population": 850,
            },
            {
                "name": "Mbarara Girls School",
                "location": "Mbarara, Western Uganda",
                "description": "Championing STEM clubs and mentorship programs for girls.",
                "website": "",
                "student_population": 900,
            },
        ]
        school_objs = {}
        for data in schools:
            obj, _ = School.objects.get_or_create(name=data["name"], defaults=data)
            school_objs[obj.name] = obj

        # Clubs
        clubs = [
            ("Tech Innovators Club", "Kampala High School"),
            ("Eco Warriors", "Gulu Community SS"),
            ("STEM Queens", "Mbarara Girls School"),
        ]
        for title, school_name in clubs:
            Club.objects.get_or_create(
                title=title,
                school=school_objs.get(school_name),
                defaults={
                    "description": "Student-run club under YCBN mentorship.",
                    "member_count": 25,
                    "is_active": True,
                },
            )

        # Blog posts (admin)
        blog_posts = [
            ("Launching the YCBN Digital Literacy Bootcamp", "YCBN Team",
             "We are excited to kick off our digital literacy bootcamps across partner schools."),
            ("Community-Driven Projects: Clean Water Initiative", "YCBN Team",
             "Students are building prototypes to improve water filtration and hygiene in their communities."),
        ]
        for title, author, content in blog_posts:
            BlogPost.objects.get_or_create(
                title=title,
                defaults={
                    "author": author,
                    "date": timezone.now().date(),
                    "content": content,
                    "is_published": True,
                },
            )

        # Donations (info cards)
        Donation.objects.get_or_create(
            title="Equip a School ICT Lab",
            defaults={
                "description": "Help us purchase computers and connectivity for rural schools.",
                "goal_amount": 20000000,
                "raised_amount": 3500000,
            },
        )

        # Impact section & counters
        Impact.objects.get_or_create(
            title="Building Future-Ready Youth",
            defaults={
                "subtitle": "Skills, mentorship, and community action",
                "description": "YCBN empowers youth with practical skills and leadership opportunities.",
            },
        )
        counters = [
            ("Youth Trained", "people", 5000, "+", "fas fa-users"),
            ("Schools Reached", "schools", 25, "+", "fas fa-school"),
            ("Active Projects", "projects", 18, "+", "fas fa-lightbulb"),
        ]
        for title, ctype, num, suffix, icon in counters:
            ImpactCounter.objects.get_or_create(
                title=title,
                defaults={
                    "counter_type": ctype,
                    "target_number": num,
                    "suffix": suffix,
                    "icon_class": icon,
                },
            )

        self.stdout.write(self.style.SUCCESS("Sample data seeded. You can view/edit them in the Django admin."))