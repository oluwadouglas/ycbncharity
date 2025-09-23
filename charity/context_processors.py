from django.conf import settings
from django.templatetags.static import static

def _site_base_url():
    base = getattr(settings, 'SITE_BASE_URL', '').strip()
    if base.endswith('/'):
        base = base[:-1]
    return base or ''

def absolute_static(request, path: str) -> str:
    """Return absolute URL to a static asset for OG/Twitter images.
    Prefers SITE_BASE_URL if configured, else falls back to request scheme/host.
    """
    base = _site_base_url()
    if base:
        return f"{base}{static(path)}"
    return f"{request.scheme}://{request.get_host()}{static(path)}"


def seo_defaults(request):
    """Provide per-page SEO defaults for title, description, canonical, and OG image.
    Templates can override via blocks; these only serve as good defaults.
    """
    rm = getattr(request, 'resolver_match', None)
    view_name = rm.view_name if rm else ''

    # Build canonical using SITE_BASE_URL when available
    base = _site_base_url()
    canonical_url = f"{base}{request.path}" if base else request.build_absolute_uri()

    # Pick representative images already in your project
    # You can swap these to dedicated OG images later (e.g., assets/img/og/*.jpg)
    def og(p):
        return absolute_static(request, p)

    defaults = {
        'charity:home': {
            'page_title': 'YCBN Uganda — Youth Capacity Building Network',
            'meta_description': 'Empowering young people in Uganda through skills development, mentorship, and community projects.',
            'og_image': og('assets/img/hero1.jpg'),
        },
        'charity:about': {
            'page_title': 'About YCBN Uganda — Our Mission and Team',
            'meta_description': 'Learn about YCBN Uganda’s mission to empower youth through education, leadership, and community impact.',
            'og_image': og('assets/img/hero2.jpg'),
        },
        'charity:projects': {
            'page_title': 'Projects — YCBN Uganda Community Impact',
            'meta_description': 'Explore ongoing and past YCBN projects creating positive change in Ugandan communities.',
            'og_image': og('assets/img/hero3.jpg'),
        },
        'charity:programs': {
            'page_title': 'Programs — Skills and Mentorship by YCBN Uganda',
            'meta_description': 'Discover YCBN programs in skills development, mentorship, and youth leadership across Uganda.',
            'og_image': og('assets/img/hero2.jpg'),
        },
        'charity:blog': {
            'page_title': 'YCBN Blog — Insights and Stories from Uganda',
            'meta_description': 'Read updates, insights, and stories about youth empowerment and community work in Uganda.',
            'og_image': og('assets/img/hero3.jpg'),
        },
        'charity:articles': {
            'page_title': 'Articles — Youth Voices at YCBN Uganda',
            'meta_description': 'Community-written articles from YCBN members on leadership, skills, and impact across Uganda.',
            'og_image': og('assets/img/hero2.jpg'),
        },
        'charity:donate_now': {
            'page_title': 'Donate — Support YCBN Uganda',
            'meta_description': 'Support youth empowerment in Uganda. Donate securely to YCBN’s programs and projects.',
            'og_image': og('assets/img/hero3.jpg'),
        },
        'charity:donations': {
            'page_title': 'Our Campaigns — YCBN Uganda',
            'meta_description': 'See current campaigns and how your donation drives youth impact in Uganda.',
            'og_image': og('assets/img/hero3.jpg'),
        },
        'charity:impact': {
            'page_title': 'Our Impact — YCBN Uganda',
            'meta_description': 'Highlights of YCBN’s measurable impact empowering youth and communities in Uganda.',
            'og_image': og('assets/img/hero1.jpg'),
        },
        'charity:contact': {
            'page_title': 'Contact YCBN Uganda',
            'meta_description': 'Reach YCBN Uganda for partnerships, volunteering, and questions about our programs.',
            'og_image': og('assets/img/ycbn-logo.png'),
        },
    }

    data = defaults.get(view_name, {})

    # Default OG image (logo) as absolute URL
    default_logo = absolute_static(request, 'assets/img/ycbn-logo.png')

    return {
        # Only supply defaults if the view/template didn’t set them
        'page_title': data.get('page_title'),
        'meta_description': data.get('meta_description'),
        'canonical_url': canonical_url,
        'og_image': data.get('og_image'),
        'default_og_image': default_logo,
    }
