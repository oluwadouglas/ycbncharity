from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def ugx(value):
    """
    Format a number as Uganda Shillings (UGX) currency.
    
    Example:
    {{ amount|ugx }}
    1000000 -> "UGX 1,000,000"
    2500000.50 -> "UGX 2,500,001" (rounded to nearest shilling)
    """
    if not value:
        return "UGX 0"
    
    try:
        # Convert to Decimal for proper handling
        amount = Decimal(str(value))
        
        # Round to nearest shilling (no decimal places for UGX)
        amount = amount.quantize(Decimal('1'))
        
        # Format with commas as thousands separator
        formatted = f"{amount:,}"
        
        return f"UGX {formatted}"
    
    except (ValueError, TypeError, InvalidOperation):
        return "UGX 0"

@register.filter
def ugx_short(value):
    """
    Format a number as Uganda Shillings with abbreviated format for large numbers.
    
    Example:
    {{ amount|ugx_short }}
    1000000 -> "UGX 1M"
    2500000 -> "UGX 2.5M"
    500000 -> "UGX 500K"
    1500 -> "UGX 1,500"
    """
    if not value:
        return "UGX 0"
    
    try:
        amount = float(value)
        
        if amount >= 1_000_000_000:  # Billions
            return f"UGX {amount/1_000_000_000:.1f}B"
        elif amount >= 1_000_000:  # Millions
            formatted = f"{amount/1_000_000:.1f}M"
            # Remove .0 for whole numbers
            formatted = formatted.replace('.0M', 'M')
            return f"UGX {formatted}"
        elif amount >= 1_000:  # Thousands
            formatted = f"{amount/1_000:.1f}K"
            # Remove .0 for whole numbers
            formatted = formatted.replace('.0K', 'K')
            return f"UGX {formatted}"
        else:
            # Format small amounts with commas
            return f"UGX {int(amount):,}"
    
    except (ValueError, TypeError):
        return "UGX 0"

@register.filter
def ugx_minimal(value):
    """
    Minimal UGX formatting - just the number with UGX prefix, no commas.
    
    Example:
    {{ amount|ugx_minimal }}
    1000000 -> "UGX 1000000"
    """
    if not value:
        return "UGX 0"
    
    try:
        amount = int(float(value))
        return f"UGX {amount}"
    except (ValueError, TypeError):
        return "UGX 0"
