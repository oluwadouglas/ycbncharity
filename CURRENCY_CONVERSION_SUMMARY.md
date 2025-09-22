# YCBF Currency Conversion Summary

## Changes Made
Changed donation currency display from **USD ($)** to **Uganda Shillings (UGX)**

## Files Modified

### 1. New Template Tags Created
- `charity/templatetags/__init__.py` - Template tags package initialization
- `charity/templatetags/currency_filters.py` - Custom currency formatting filters

### 2. Template Files Updated
- `templates/charity/donation.html` - Main donations listing page
- `templates/charity/donation-details.html` - Individual donation details page
- `templates/charity/temp_swap.html` - Homepage template with donation section

## Currency Filters Available

### `ugx` Filter
Formats numbers as Uganda Shillings with proper comma separation.
- Example: `{{ 250000|ugx }}` → "UGX 250,000"
- Example: `{{ 2500000.50|ugx }}` → "UGX 2,500,001" (rounded to nearest shilling)

### `ugx_short` Filter  
Formats large numbers with abbreviated notation.
- Example: `{{ 250000|ugx_short }}` → "UGX 250K"
- Example: `{{ 2500000|ugx_short }}` → "UGX 2.5M" 
- Example: `{{ 230000000|ugx_short }}` → "UGX 230M"

### `ugx_minimal` Filter
Simple UGX formatting without comma separators.
- Example: `{{ 250000|ugx_minimal }}` → "UGX 250000"

## Usage in Templates

### Before (USD):
```html
<span class="donation-card_raise">Raised <span class="donation-card_raise-number">${{ item.raised_amount }}</span></span>
<span class="donation-card_goal">Goal <span class="donation-card_goal-number">${{ item.goal_amount }}</span></span>
```

### After (UGX):
```html
{% load currency_filters %}
<span class="donation-card_raise">Raised <span class="donation-card_raise-number">{{ item.raised_amount|ugx_short }}</span></span>
<span class="donation-card_goal">Goal <span class="donation-card_goal-number">{{ item.goal_amount|ugx_short }}</span></span>
```

## Example Outputs

Based on your example values:
- **Raised: $250000.00** → **Raised: UGX 250K**
- **Goal: $230000000.00** → **Goal: UGX 230M**

For more detailed display:
- **Raised: $250000.00** → **Raised: UGX 250,000**
- **Goal: $230000000.00** → **Goal: UGX 230,000,000**

## Notes
- All currency values are now displayed in Uganda Shillings (UGX)
- The system automatically formats large numbers with K (thousands) and M (millions) for better readability
- Decimal places are rounded to the nearest shilling since UGX typically doesn't use decimals
- The database values remain unchanged - only the display format has been updated
