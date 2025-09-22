#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ycbn_charity.settings')
django.setup()

from charity.models import Impact, ImpactCounter

def test_impact_data():
    print("=== Impact Data Test ===")
    
    # Check Impact sections
    impact_sections = Impact.objects.filter(is_active=True)
    print(f"Active Impact sections: {impact_sections.count()}")
    
    for section in impact_sections:
        print(f"\nSection: {section.title}")
        print(f"  Active: {section.is_active}")
        print(f"  Highlight 1 Number: '{section.highlight_1_number}'")
        print(f"  Highlight 1 Desc: '{section.highlight_1_description}'")
        print(f"  Highlight 2 Number: '{section.highlight_2_number}'")
        print(f"  Highlight 2 Desc: '{section.highlight_2_description}'")
        print(f"  Highlight 3 Number: '{section.highlight_3_number}'")
        print(f"  Highlight 3 Desc: '{section.highlight_3_description}'")
        
        # Check if any highlight fields are empty
        has_highlights = any([
            section.highlight_1_number.strip() if section.highlight_1_number else False,
            section.highlight_2_number.strip() if section.highlight_2_number else False,
            section.highlight_3_number.strip() if section.highlight_3_number else False,
        ])
        print(f"  Has highlight numbers: {has_highlights}")
    
    # Check Impact counters
    impact_counters = ImpactCounter.objects.filter(is_active=True)
    print(f"\nActive Impact counters: {impact_counters.count()}")
    
    for counter in impact_counters:
        print(f"Counter: {counter.title} - Target: {counter.target_number}")

if __name__ == '__main__':
    test_impact_data()
