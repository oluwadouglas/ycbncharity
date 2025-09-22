from django.core.management.base import BaseCommand
from charity.models import VoiceOfChange

class Command(BaseCommand):
    help = 'Create sample VoiceOfChange entries for testing the Voices of Change section'

    def handle(self, *args, **options):
        # Clear existing entries to avoid duplicates
        VoiceOfChange.objects.all().delete()
        
        sample_voices = [
            {
                'name': 'Aisha Nakato',
                'title': 'Leadership Program Graduate',
                'quote': 'Through the Youth Capacity Building Forum, I discovered my leadership potential. The skills I learned have helped me start my own community project that now serves over 200 young people in my district. I am grateful for the mentorship and support that transformed my life.'
            },
            {
                'name': 'Samuel Kiwanuka',
                'title': 'Digital Literacy Program Participant',
                'quote': 'Before joining YCBF, I had never touched a computer. Today, I run my own digital marketing business and teach other youth basic computer skills. The program opened doors I never knew existed and gave me confidence to pursue my dreams in technology.'
            },
            {
                'name': 'Grace Naluwemba',
                'title': 'Entrepreneurship Club Member',
                'quote': 'The entrepreneurship skills I gained through YCBF helped me launch my small agriculture business. Now I employ 5 other young people and we supply fresh produce to local markets. This organization truly empowers youth to become job creators, not just job seekers.'
            },
            {
                'name': 'David Ssekandi',
                'title': 'Community Outreach Volunteer',
                'quote': 'Being part of YCBF taught me the importance of giving back to the community. I now coordinate youth programs in my village and have helped establish 3 youth clubs in neighboring schools. The networking opportunities have been incredible.'
            },
            {
                'name': 'Faith Namukasa',
                'title': 'Skills Development Program Alumni',
                'quote': 'The vocational training I received through YCBF changed my family\'s life completely. I learned tailoring and fashion design, and now I have my own workshop with 10 employees. We even export our products to neighboring countries. Thank you YCBF!'
            }
        ]
        
        created_count = 0
        for voice_data in sample_voices:
            voice, created = VoiceOfChange.objects.get_or_create(
                name=voice_data['name'],
                defaults={
                    'title': voice_data['title'],
                    'quote': voice_data['quote']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created voice: {voice.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Voice already exists: {voice.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} new Voices of Change entries!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'You can now visit your homepage to see the "Voices of Change" section in action.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'To add images to these voices, go to Django Admin > Voice of changes and upload images.'
            )
        )
