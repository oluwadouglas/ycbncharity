"""
Script to create sample ImpactCounter data for the home page counter section.
"""

from charity.models import ImpactCounter

# Sample data for impact counters
counters_data = [
    {
        'title': 'Young Leaders Trained',
        'counter_type': 'people',
        'target_number': 750,
        'suffix': '+',
        'prefix': '',
        'icon_class': 'fas fa-users',
        'color_theme': 'primary',
        'order': 1,
    },
    {
        'title': 'Community Projects',
        'counter_type': 'projects',
        'target_number': 125,
        'suffix': '+',
        'prefix': '',
        'icon_class': 'fas fa-project-diagram',
        'color_theme': 'success',
        'order': 2,
    },
    {
        'title': 'Partner Organizations',
        'counter_type': 'communities',
        'target_number': 35,
        'suffix': '+',
        'prefix': '',
        'icon_class': 'fas fa-handshake',
        'color_theme': 'primary',
        'order': 3,
    },
    {
        'title': 'Districts Reached',
        'counter_type': 'communities',
        'target_number': 18,
        'suffix': '+',
        'prefix': '',
        'icon_class': 'fas fa-map-marker-alt',
        'color_theme': 'success',
        'order': 4,
    },
]

# Create the counters
created_count = 0
total_count = 0

for counter_info in counters_data:
    counter, created = ImpactCounter.objects.get_or_create(
        title=counter_info['title'],
        defaults=counter_info
    )
    total_count += 1
    if created:
        created_count += 1
        print(f"✅ Created: {counter.title} - {counter.prefix}{counter.target_number}{counter.suffix}")
    else:
        print(f"⚡ Already exists: {counter.title} - {counter.prefix}{counter.target_number}{counter.suffix}")

print(f"\n🎉 Created {created_count} new counters out of {total_count} total")
print(f"📊 Active ImpactCounters count: {ImpactCounter.objects.filter(is_active=True).count()}")
print("Done! Your counter section should now display real data instead of NaN.")
