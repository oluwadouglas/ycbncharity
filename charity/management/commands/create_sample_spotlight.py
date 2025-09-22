from django.core.management.base import BaseCommand
from charity.models import SpotlightCategory, SpotlightItem, SpotlightStats
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create sample Spotlight categories, items, and stats for YCBF'

    def handle(self, *args, **options):
        # Clear existing entries to avoid duplicates
        SpotlightItem.objects.all().delete()
        SpotlightCategory.objects.all().delete()
        SpotlightStats.objects.all().delete()
        
        # Create Spotlight items
        spotlight_items = [
            {
                'title': 'Sarah\'s Digital Transformation Success',
                'subtitle': 'From Village Girl to Tech Entrepreneur',
                'category': 'success_story',
                'featured_image_alt': 'Sarah working on her computer at her tech startup',
                'excerpt': 'Meet Sarah Nakato, a young woman from rural Masaka who transformed her life through YCBF\'s Digital Literacy Program. From never touching a computer to running her own tech consultancy, Sarah\'s journey is truly inspiring.',
                'content': '''
                <p>Sarah Nakato was just 19 when she first heard about the Youth Center for Better Future's Digital Literacy Program in her village of Masaka. Like many young people in rural Uganda, Sarah had limited exposure to technology and computers seemed like distant, unreachable tools.</p>
                
                <p>"I remember the first day I walked into the digital learning center," Sarah recalls. "I was scared to even touch the keyboard. I thought I would break something expensive that the community couldn't afford to replace."</p>
                
                <h3>The Journey Begins</h3>
                <p>Under the patient guidance of YCBF mentors, Sarah slowly built confidence with basic computer skills. She learned to navigate operating systems, use word processing software, and understand internet basics. What started as fear soon transformed into fascination.</p>
                
                <p>"The mentors never made me feel stupid for asking basic questions," Sarah explains. "They celebrated every small victory, from my first successful email to creating my first presentation."</p>
                
                <h3>Building Skills and Confidence</h3>
                <p>After completing the basic program, Sarah enrolled in advanced courses covering web design, digital marketing, and business applications. She spent countless hours practicing, often staying late at the center to perfect her skills.</p>
                
                <p>Her breakthrough came when she created a website for a local farming cooperative, helping them connect with buyers in Kampala. The project was so successful that word spread throughout the region.</p>
                
                <h3>From Student to Entrepreneur</h3>
                <p>Today, just two years later, Sarah runs "Digital Solutions Masaka," a tech consultancy that helps local businesses establish their online presence. She employs three other young people from her community and has served over 50 clients across central Uganda.</p>
                
                <p>"YCBF didn't just teach me computer skills," Sarah reflects. "They taught me that with the right training and determination, any young person can create opportunities, not just wait for them."</p>
                
                <p>Sarah's story exemplifies the transformative power of digital literacy training and the ripple effect it creates in communities across Uganda.</p>
                ''',
                'author': 'YCBF Communications Team',
                'publication_date': timezone.now() - timedelta(days=10),
                'tags': 'success story, digital literacy, entrepreneurship, women empowerment, rural development',
                'is_featured': True,
                'is_published': True,
                'order': 1
            },
            {
                'title': 'Youth Leadership Summit 2024',
                'subtitle': 'Bringing Together 200 Young Leaders from Across Uganda',
                'category': 'event',
                'featured_image_alt': 'Group photo of young leaders at the YCBF Leadership Summit',
                'excerpt': 'The annual Youth Leadership Summit brought together 200 exceptional young leaders from 12 districts for three days of intensive training, networking, and collaborative project planning.',
                'content': '''
                <p>The Youth Center for Better Future's 2024 Leadership Summit was our most impactful event yet, bringing together 200 emerging leaders aged 18-25 from across Uganda for three transformative days of learning and collaboration.</p>
                
                <h3>A Gathering of Change-Makers</h3>
                <p>Held at the Kampala Conference Center, the summit attracted participants from 12 districts, each selected for their demonstrated commitment to community development and leadership potential. The diverse group included students, young professionals, community organizers, and social entrepreneurs.</p>
                
                <h3>Comprehensive Leadership Training</h3>
                <p>The program featured workshops on:</p>
                <ul>
                    <li>Transformational Leadership in the 21st Century</li>
                    <li>Project Management for Community Impact</li>
                    <li>Digital Tools for Social Change</li>
                    <li>Financial Literacy and Resource Mobilization</li>
                    <li>Communication and Public Speaking</li>
                    <li>Building Sustainable Partnerships</li>
                </ul>
                
                <h3>Notable Speakers and Mentors</h3>
                <p>The summit featured inspirational presentations from prominent Ugandan leaders including:</p>
                <ul>
                    <li>Hon. Jessica Alupo, Vice President of Uganda</li>
                    <li>Dr. Monica Musenero, Minister of Science, Technology and Innovation</li>
                    <li>Rebecca Kadaga, Former Speaker of Parliament</li>
                    <li>Successful young entrepreneurs and YCBF alumni</li>
                </ul>
                
                <h3>Collaborative Project Planning</h3>
                <p>A highlight of the summit was the collaborative project planning session, where participants formed cross-district teams to design community impact initiatives. Five standout projects received seed funding of UGX 2,000,000 each to kickstart implementation.</p>
                
                <h3>Building a Network for Change</h3>
                <p>"The connections made at this summit will last a lifetime," said participant Grace Namukasa from Gulu. "We're not just individuals working in isolation anymore – we're part of a movement for positive change in Uganda."</p>
                
                <p>The summit concluded with participants committing to the "2024 Leadership Pledge," promising to implement at least one community project within six months and mentor two other young people in their communities.</p>
                ''',
                'author': 'YCBF Events Team',
                'publication_date': timezone.now() - timedelta(days=25),
                'tags': 'leadership, summit, youth development, networking, capacity building',
                'is_featured': True,
                'is_published': True,
                'order': 2
            },
            {
                'title': 'Digital Learning Centers Expansion',
                'subtitle': 'Opening 10 New Centers Across Remote Communities',
                'category': 'program_update',
                'featured_image_alt': 'New digital learning center with computers and students',
                'excerpt': 'YCBF is proud to announce the opening of 10 new digital learning centers in remote communities, bringing technology access to over 2,000 additional young people.',
                'content': '''
                <p>The Youth Center for Better Future is excited to announce a major expansion of our Digital Learning Centers program, with 10 new facilities now operational across remote communities in Uganda.</p>
                
                <h3>Bridging the Digital Divide</h3>
                <p>These new centers, established in partnership with local schools and community organizations, are strategically located in areas previously underserved by technology infrastructure. Each center features:</p>
                <ul>
                    <li>20 modern desktop computers with internet connectivity</li>
                    <li>Backup solar power systems for reliable operation</li>
                    <li>Dedicated learning spaces for group activities</li>
                    <li>Resource libraries with digital literacy materials</li>
                    <li>Video conferencing facilities for remote mentoring</li>
                </ul>
                
                <h3>Community Partnership Model</h3>
                <p>The success of this expansion is built on strong partnerships with local communities. Each center operates through collaboration with:</p>
                <ul>
                    <li>Local schools providing space and basic infrastructure</li>
                    <li>Community leaders ensuring program sustainability</li>
                    <li>Parent-teacher associations supporting student participation</li>
                    <li>Local government providing security and oversight</li>
                </ul>
                
                <h3>New Locations Include:</h3>
                <ul>
                    <li>Pakwach District - Serving 3 sub-counties</li>
                    <li>Kaberamaido District - Reaching pastoral communities</li>
                    <li>Kisoro District - Supporting mountain communities</li>
                    <li>Bundibugyo District - Crossing cultural boundaries</li>
                    <li>Kotido District - Empowering youth in Karamoja</li>
                    <li>And 5 additional strategic locations</li>
                </ul>
                
                <h3>Trained Local Instructors</h3>
                <p>To ensure quality programming, YCBF has trained 30 local instructors through an intensive 2-week certification program. These community-based educators will provide ongoing training and support, ensuring programs remain relevant to local needs.</p>
                
                <h3>Expected Impact</h3>
                <p>Over the next 12 months, these centers are projected to:</p>
                <ul>
                    <li>Train 2,000+ youth in basic digital literacy</li>
                    <li>Provide advanced certification courses to 500+ participants</li>
                    <li>Support 100+ community-based projects</li>
                    <li>Create pathways to digital employment for 200+ youth</li>
                </ul>
                
                <p>"This expansion represents our commitment to ensuring no young person is left behind in Uganda's digital transformation," said YCBF Program Director, James Mukasa.</p>
                ''',
                'author': 'YCBF Program Team',
                'publication_date': timezone.now() - timedelta(days=5),
                'tags': 'digital literacy, expansion, community partnerships, technology access, rural development',
                'is_featured': True,
                'is_published': True,
                'order': 3
            },
            {
                'title': 'Meet Joseph: From Street Life to Community Leader',
                'subtitle': 'A Former Street Child\'s Journey to Becoming a Youth Advocate',
                'category': 'success_story',
                'featured_image_alt': 'Joseph speaking at a community meeting',
                'excerpt': 'Joseph Opio\'s transformation from street child to community advocate demonstrates the life-changing impact of YCBF\'s comprehensive youth programs and unwavering mentorship.',
                'content': '''
                <p>At 16, Joseph Opio was living on the streets of Kampala, surviving day to day with little hope for the future. Today, at 22, he serves as a community youth advocate and runs programs helping other vulnerable young people. His journey with the Youth Center for Better Future has been nothing short of remarkable.</p>
                
                <h3>Life on the Streets</h3>
                <p>Joseph's story began in hardship. After losing both parents to illness, he found himself alone and homeless in Uganda's capital city. "I spent three years on the streets," Joseph recalls. "I did whatever I could to survive – carrying bags at the taxi park, washing cars, sometimes going days without food."</p>
                
                <p>The turning point came when a YCBF outreach worker approached him during one of the organization's street engagement programs. "I was suspicious at first," Joseph admits. "Too many people had made promises they couldn't keep."</p>
                
                <h3>Finding Hope at YCBF</h3>
                <p>Despite his initial skepticism, Joseph accepted an invitation to visit the YCBF center. What he found was different from anything he had experienced – a place where he was treated with dignity and respect, regardless of his circumstances.</p>
                
                <p>"The mentors at YCBF didn't judge me for my past," Joseph explains. "They saw potential in me that I couldn't see in myself. They helped me believe that change was possible."</p>
                
                <h3>Education and Skill Development</h3>
                <p>Joseph enrolled in YCBF's comprehensive support program, which included:</p>
                <ul>
                    <li>Basic literacy and numeracy classes</li>
                    <li>Life skills training and counseling support</li>
                    <li>Digital literacy and computer skills</li>
                    <li>Leadership development workshops</li>
                    <li>Vocational training in graphic design</li>
                </ul>
                
                <p>The program also provided temporary accommodation and meals, allowing Joseph to focus entirely on his education and personal development.</p>
                
                <h3>Giving Back to the Community</h3>
                <p>As Joseph's skills and confidence grew, he began volunteering with YCBF's outreach programs, using his experience to connect with other street youth. His authentic approach and personal story resonated with young people who were struggling with similar challenges.</p>
                
                <p>"Having been there myself, I understand the fear, the hopelessness, the mistrust," Joseph explains. "When I tell them that change is possible, they believe me because they can see the evidence standing in front of them."</p>
                
                <h3>Leading Change Today</h3>
                <p>Today, Joseph coordinates YCBF's Street Youth Engagement Program, reaching out to vulnerable young people across Kampala. He has helped over 150 street youth access education and support services, with 80% successfully transitioning to stable housing and education or employment.</p>
                
                <p>Joseph also runs his own graphic design business and is pursuing a degree in social work through evening classes, funded by a YCBF scholarship program.</p>
                
                <h3>A Message of Hope</h3>
                <p>"My message to any young person facing challenges is simple: your current situation is not your final destination," Joseph says. "With the right support, determination, and belief in yourself, you can overcome anything and become the person you're meant to be."</p>
                
                <p>Joseph's story embodies YCBF's core belief that every young person, regardless of their circumstances, has the potential to create positive change in their life and community.</p>
                ''',
                'author': 'YCBF Communications Team',
                'publication_date': timezone.now() - timedelta(days=15),
                'tags': 'success story, street youth, transformation, community leadership, mentorship',
                'is_featured': False,
                'is_published': True,
                'order': 4
            },
            {
                'title': 'Partnership with Ministry of Education',
                'subtitle': 'Integrating Digital Literacy into National Curriculum',
                'category': 'partnership',
                'featured_image_alt': 'YCBF team meeting with Ministry of Education officials',
                'excerpt': 'YCBF has signed a groundbreaking partnership with the Ministry of Education to integrate digital literacy training into the national secondary school curriculum across Uganda.',
                'content': '''
                <p>The Youth Center for Better Future is proud to announce a landmark partnership with Uganda's Ministry of Education and Sports to integrate comprehensive digital literacy training into the national secondary school curriculum.</p>
                
                <h3>A National Impact Initiative</h3>
                <p>This partnership represents the largest expansion of YCBF's impact, with the potential to reach over 500,000 secondary school students across Uganda over the next five years. The program will be implemented in phases, starting with 100 pilot schools in 2024.</p>
                
                <h3>Curriculum Integration Details</h3>
                <p>The integrated curriculum will include:</p>
                <ul>
                    <li>Basic computer skills and digital literacy (S1-S2)</li>
                    <li>Internet safety and digital citizenship (S1-S4)</li>
                    <li>Introduction to programming and web development (S3-S4)</li>
                    <li>Digital entrepreneurship and online business skills (S4-S6)</li>
                    <li>Advanced digital tools for academic research (S5-S6)</li>
                </ul>
                
                <h3>Teacher Training Program</h3>
                <p>Recognizing that successful implementation requires well-trained educators, YCBF will lead a comprehensive teacher training program:</p>
                <ul>
                    <li>2-week intensive digital literacy training for teachers</li>
                    <li>Ongoing professional development workshops</li>
                    <li>Online resource library and support materials</li>
                    <li>Peer mentoring networks among trained teachers</li>
                    <li>Annual refresher courses on emerging technologies</li>
                </ul>
                
                <h3>Infrastructure Development</h3>
                <p>The partnership includes significant infrastructure development:</p>
                <ul>
                    <li>Establishment of digital learning labs in 100 schools</li>
                    <li>Provision of computers and internet connectivity</li>
                    <li>Solar power backup systems for reliable operation</li>
                    <li>Technical support and maintenance programs</li>
                </ul>
                
                <h3>Phased Implementation Plan</h3>
                <p><strong>Phase 1 (2024):</strong> Pilot program in 100 schools across 10 districts</p>
                <p><strong>Phase 2 (2025):</strong> Expansion to 300 additional schools</p>
                <p><strong>Phase 3 (2026-2028):</strong> National rollout to all secondary schools</p>
                
                <h3>Expected Outcomes</h3>
                <p>This partnership is projected to:</p>
                <ul>
                    <li>Improve digital literacy rates among Ugandan youth by 400%</li>
                    <li>Increase secondary school technology integration scores</li>
                    <li>Create pathways to technology careers for 50,000+ students</li>
                    <li>Support Uganda's digital transformation agenda</li>
                    <li>Reduce the urban-rural digital divide</li>
                </ul>
                
                <h3>Government and Community Support</h3>
                <p>"This partnership aligns perfectly with our national development goals," said Hon. Janet Museveni, Minister of Education and Sports. "By integrating digital literacy into our curriculum, we're preparing our young people for the jobs of tomorrow."</p>
                
                <p>Local community leaders have also expressed strong support, with District Education Officers committing to provide local oversight and community engagement.</p>
                
                <h3>Funding and Sustainability</h3>
                <p>The initiative is supported by a consortium of partners including the World Bank, USAID, and several private sector technology companies. A sustainability plan ensures continued operation beyond the initial implementation period.</p>
                
                <p>"This partnership represents the scale of impact possible when government, NGOs, and communities work together toward a common goal," said YCBF Executive Director, Mary Namubiru.</p>
                ''',
                'author': 'YCBF Policy Team',
                'publication_date': timezone.now() - timedelta(days=30),
                'tags': 'partnership, government, education, curriculum integration, policy, national impact',
                'is_featured': False,
                'is_published': True,
                'order': 5
            },
            {
                'title': 'Girls in Tech Initiative Graduates First Cohort',
                'subtitle': '50 Young Women Complete Advanced Programming Bootcamp',
                'category': 'program_update',
                'featured_image_alt': 'Female students working on coding projects at YCBF',
                'excerpt': 'The YCBF Girls in Tech Initiative celebrates the graduation of 50 young women who completed an intensive 6-month programming bootcamp, with 90% already securing technology internships or jobs.',
                'content': '''
                <p>The Youth Center for Better Future's Girls in Tech Initiative reached a major milestone with the graduation of its first cohort of 50 young women who completed an intensive 6-month programming bootcamp. The program addresses the significant gender gap in Uganda's technology sector while creating new opportunities for female youth.</p>
                
                <h3>Breaking Barriers in Technology</h3>
                <p>The Girls in Tech Initiative was launched to address the stark underrepresentation of women in Uganda's growing technology sector. With women comprising less than 20% of technology professionals in the country, the program aims to change this narrative by providing comprehensive technical training and career support.</p>
                
                <h3>Comprehensive Technical Curriculum</h3>
                <p>The 6-month bootcamp covered:</p>
                <ul>
                    <li>Fundamentals of programming (Python, JavaScript)</li>
                    <li>Web development (HTML, CSS, React)</li>
                    <li>Mobile app development basics</li>
                    <li>Database design and management</li>
                    <li>User experience (UX) design principles</li>
                    <li>Project management and agile methodologies</li>
                    <li>Professional development and workplace skills</li>
                </ul>
                
                <h3>Mentorship and Support Network</h3>
                <p>Each participant was paired with a female technology professional who provided:</p>
                <ul>
                    <li>Weekly one-on-one mentoring sessions</li>
                    <li>Career guidance and goal setting</li>
                    <li>Technical project reviews and feedback</li>
                    <li>Professional networking introductions</li>
                    <li>Industry insights and trends discussion</li>
                </ul>
                
                <h3>Real-World Project Experience</h3>
                <p>Students worked on actual client projects, including:</p>
                <ul>
                    <li>E-commerce website for local women's cooperatives</li>
                    <li>Mobile app for community health tracking</li>
                    <li>School management system for rural primary schools</li>
                    <li>Digital marketplace for agricultural products</li>
                </ul>
                
                <h3>Outstanding Employment Outcomes</h3>
                <p>The program's success is evident in post-graduation outcomes:</p>
                <ul>
                    <li>90% of graduates secured tech internships or full-time positions</li>
                    <li>Average starting salary 300% higher than pre-program earnings</li>
                    <li>15 graduates started their own tech consultancies</li>
                    <li>10 graduates enrolled in computer science degree programs</li>
                    <li>100% report increased confidence in technical abilities</li>
                </ul>
                
                <h3>Graduate Success Stories</h3>
                <p><strong>Grace Akello</strong> landed a software developer position at a prominent Kampala tech company: "The bootcamp didn't just teach me to code – it taught me to think like a technologist and solve complex problems."</p>
                
                <p><strong>Patricia Namutebi</strong> launched her own web design business: "I'm now financially independent and employing two other young women. The ripple effect is already happening."</p>
                
                <h3>Industry Partnership Support</h3>
                <p>The program's success was supported by partnerships with leading technology companies:</p>
                <ul>
                    <li>MTN Uganda – Provided internship opportunities</li>
                    <li>Andela Uganda – Technical mentorship and curriculum support</li>
                    <li>Refactory – Advanced training modules</li>
                    <li>OutBox Uganda – Entrepreneurship workshops</li>
                </ul>
                
                <h3>Expanding the Initiative</h3>
                <p>Based on the overwhelming success of the first cohort, YCBF is expanding the Girls in Tech Initiative:</p>
                <ul>
                    <li>Second cohort of 75 participants launching in January 2025</li>
                    <li>Addition of specialized tracks in cybersecurity and data science</li>
                    <li>Partnership with universities for degree pathway options</li>
                    <li>Expansion to include participants from rural districts</li>
                </ul>
                
                <h3>Creating Lasting Change</h3>
                <p>"This program proves that with the right support and opportunities, young women can excel in technology fields," said Program Coordinator, Sarah Zawedde. "Our graduates are not just finding jobs – they're becoming leaders and change-makers in the tech sector."</p>
                
                <p>The Girls in Tech Initiative represents YCBF's commitment to creating inclusive opportunities that address both skills gaps and gender inequality in Uganda's technology ecosystem.</p>
                ''',
                'author': 'YCBF Programs Team',
                'publication_date': timezone.now() - timedelta(days=12),
                'tags': 'girls in tech, programming, bootcamp, gender equality, women empowerment, career development',
                'is_featured': True,
                'is_published': True,
                'order': 6
            }
        ]
        
        # Create Spotlight items
        created_items = 0
        for item_data in spotlight_items:
            item, created = Spotlight.objects.get_or_create(
                title=item_data['title'],
                defaults=item_data
            )
            if created:
                created_items += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created spotlight item: {item.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Spotlight item already exists: {item.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_items} spotlight items!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Visit /spotlight/ to see the Spotlight page with dynamic content.'
            )
        )
