from django.core.management.base import BaseCommand
from charity.models import Mentor

class Command(BaseCommand):
    help = 'Create sample Mentor entries for testing the mentors section'

    def handle(self, *args, **options):
        # Clear existing entries to avoid duplicates
        Mentor.objects.all().delete()
        
        sample_mentors = [
            {
                'name': 'Dr. Sarah Nakamura',
                'title': 'Leadership Development Expert',
                'description': 'With over 15 years of experience in youth development, Dr. Nakamura specializes in leadership training and capacity building. She has mentored over 500 young leaders across East Africa.',
                'social_links': {
                    'linkedin': 'https://linkedin.com/in/sarah-nakamura',
                    'twitter': 'https://twitter.com/sarahnakamura',
                    'whatsapp': 'https://wa.me/256700123456'
                }
            },
            {
                'name': 'James Mukasa',
                'title': 'Entrepreneurship & Business Coach',
                'description': 'A successful entrepreneur and business coach who has helped establish over 100 youth-led enterprises. James provides practical guidance on business development and financial literacy.',
                'social_links': {
                    'linkedin': 'https://linkedin.com/in/james-mukasa',
                    'facebook': 'https://facebook.com/jamesmukasa',
                    'whatsapp': 'https://wa.me/256700123457'
                }
            },
            {
                'name': 'Grace Akello',
                'title': 'Digital Skills & Technology Mentor',
                'description': 'A tech industry veteran with expertise in digital literacy, coding, and technology innovation. Grace leads our digital skills programs and mentors young tech enthusiasts.',
                'social_links': {
                    'linkedin': 'https://linkedin.com/in/grace-akello',
                    'twitter': 'https://twitter.com/graceakello',
                    'instagram': 'https://instagram.com/graceakello'
                }
            },
            {
                'name': 'Robert Ssemwogerere',
                'title': 'Community Development Specialist',
                'description': 'An expert in community engagement and project management, Robert guides youth in developing impactful community projects and social initiatives.',
                'social_links': {
                    'facebook': 'https://facebook.com/robert.ssemwogerere',
                    'whatsapp': 'https://wa.me/256700123458'
                }
            },
            {
                'name': 'Dr. Mary Nalwanga',
                'title': 'Education & Career Guidance Counselor',
                'description': 'A seasoned education specialist who provides academic and career guidance to young people. She helps youth identify their strengths and chart their career paths.',
                'social_links': {
                    'linkedin': 'https://linkedin.com/in/mary-nalwanga',
                    'facebook': 'https://facebook.com/marynalwanga'
                }
            },
            {
                'name': 'Peter Wamala',
                'title': 'Creative Arts & Media Mentor',
                'description': 'A creative professional with experience in media, arts, and communications. Peter mentors young creatives and helps them develop their artistic talents.',
                'social_links': {
                    'instagram': 'https://instagram.com/peterwamala',
                    'twitter': 'https://twitter.com/peterwamala',
                    'facebook': 'https://facebook.com/peterwamala'
                }
            }
        ]
        
        created_count = 0
        for mentor_data in sample_mentors:
            mentor, created = Mentor.objects.get_or_create(
                name=mentor_data['name'],
                defaults={
                    'title': mentor_data['title'],
                    'description': mentor_data['description'],
                    'social_links': mentor_data['social_links']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created mentor: {mentor.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Mentor already exists: {mentor.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} new Mentor entries!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'You can now visit your homepage to see the "Our Mentors" section in action.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'To add images to these mentors, go to Django Admin > Mentors and upload images.'
            )
        )
