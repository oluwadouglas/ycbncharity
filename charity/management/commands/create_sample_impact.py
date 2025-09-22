from django.core.management.base import BaseCommand
from charity.models import Impact, ImpactCounter

class Command(BaseCommand):
    help = 'Create sample Impact sections and counters for YCBF'

    def handle(self, *args, **options):
        # Clear existing entries to avoid duplicates
        Impact.objects.all().delete()
        ImpactCounter.objects.all().delete()
        
        # Create Impact Sections
        impact_sections = [
            {
                'title': 'Digital Literacy Program',
                'subtitle': 'Empowering Youth with Technology Skills',
                'description': 'Our flagship Digital Literacy Program has transformed how young people in Uganda interact with technology. Through comprehensive training in computer skills, internet safety, and digital communication, we have established learning centers in rural schools and communities. Students learn everything from basic computer operations to advanced digital tools, preparing them for the modern workforce. The program includes hands-on training, certification courses, and ongoing mentorship to ensure sustainable skill development.',
                'highlight_1_number': '20',
                'highlight_1_description': 'Digital literacy centers established in rural schools across Uganda',
                'highlight_2_number': '5,000+',
                'highlight_2_description': 'Youth trained in basic computer skills and internet safety',
                'highlight_3_number': '90%',
                'highlight_3_description': 'of trained youth report increased confidence in using digital tools',
                'order': 1,
                'is_active': True
            },
            {
                'title': 'Leadership Development Initiative',
                'subtitle': 'Building Tomorrow\'s Leaders Today',
                'description': 'Our Leadership Development Initiative focuses on cultivating leadership skills among young Ugandans through intensive training programs, mentorship opportunities, and practical leadership experiences. Participants engage in workshops covering communication, project management, team building, and community engagement. The program includes real-world leadership projects where youth can apply their skills to address community challenges.',
                'highlight_1_number': '800+',
                'highlight_1_description': 'Young leaders trained through our comprehensive programs',
                'highlight_2_number': '95%',
                'highlight_2_description': 'of participants now hold leadership roles in their communities',
                'highlight_3_number': '150',
                'highlight_3_description': 'Community projects initiated by program graduates',
                'order': 2,
                'is_active': True
            },
            {
                'title': 'Entrepreneurship & Business Skills',
                'subtitle': 'Fostering Innovation and Economic Growth',
                'description': 'Through our Entrepreneurship program, we equip young people with the knowledge and skills needed to start and manage successful businesses. The program covers business planning, financial literacy, marketing, and access to micro-financing. We provide ongoing mentorship and support to help young entrepreneurs turn their ideas into viable businesses that contribute to economic growth in their communities.',
                'highlight_1_number': '300+',
                'highlight_1_description': 'Young entrepreneurs supported with business training',
                'highlight_2_number': '120',
                'highlight_2_description': 'New businesses launched by program participants',
                'highlight_3_number': '1,500',
                'highlight_3_description': 'Jobs created through youth-led enterprises',
                'order': 3,
                'is_active': True
            },
            {
                'title': 'Community Development Projects',
                'subtitle': 'Creating Lasting Change in Local Communities',
                'description': 'Our Community Development Projects empower young people to identify and address challenges in their local communities. From clean water initiatives to educational support programs, these projects are designed and implemented by youth with guidance from our experienced mentors. Each project focuses on sustainability and community ownership to ensure long-term impact.',
                'highlight_1_number': '75',
                'highlight_1_description': 'Community development projects completed across 10 districts',
                'highlight_2_number': '25,000+',
                'highlight_2_description': 'Community members directly benefited from youth-led projects',
                'highlight_3_number': '100%',
                'highlight_3_description': 'of projects continue operating independently after program completion',
                'order': 4,
                'is_active': True
            }
        ]
        
        # Create Impact Counters
        impact_counters = [
            {
                'title': 'Youth Trained',
                'counter_type': 'people',
                'target_number': 6200,
                'suffix': '+',
                'prefix': '',
                'icon_class': 'fas fa-users',
                'color_theme': 'primary',
                'order': 1,
                'is_active': True
            },
            {
                'title': 'Communities Served',
                'counter_type': 'communities',
                'target_number': 85,
                'suffix': '+',
                'prefix': '',
                'icon_class': 'fas fa-home',
                'color_theme': 'secondary',
                'order': 2,
                'is_active': True
            },
            {
                'title': 'Projects Completed',
                'counter_type': 'projects',
                'target_number': 275,
                'suffix': '+',
                'prefix': '',
                'icon_class': 'fas fa-project-diagram',
                'color_theme': 'success',
                'order': 3,
                'is_active': True
            },
            {
                'title': 'Success Rate',
                'counter_type': 'custom',
                'target_number': 92,
                'suffix': '%',
                'prefix': '',
                'icon_class': 'fas fa-chart-line',
                'color_theme': 'info',
                'order': 4,
                'is_active': True
            },
            {
                'title': 'Partner Schools',
                'counter_type': 'schools',
                'target_number': 45,
                'suffix': '+',
                'prefix': '',
                'icon_class': 'fas fa-school',
                'color_theme': 'warning',
                'order': 5,
                'is_active': True
            },
            {
                'title': 'Districts Reached',
                'counter_type': 'custom',
                'target_number': 12,
                'suffix': '',
                'prefix': '',
                'icon_class': 'fas fa-map-marked-alt',
                'color_theme': 'danger',
                'order': 6,
                'is_active': True
            }
        ]
        
        # Create Impact sections
        created_sections = 0
        for section_data in impact_sections:
            section, created = Impact.objects.get_or_create(
                title=section_data['title'],
                defaults=section_data
            )
            if created:
                created_sections += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created impact section: {section.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Impact section already exists: {section.title}')
                )
        
        # Create Impact counters
        created_counters = 0
        for counter_data in impact_counters:
            counter, created = ImpactCounter.objects.get_or_create(
                title=counter_data['title'],
                defaults=counter_data
            )
            if created:
                created_counters += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created impact counter: {counter.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Impact counter already exists: {counter.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_sections} impact sections and {created_counters} impact counters!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Visit /impact/ to see the Our Impact page with dynamic content.'
            )
        )
