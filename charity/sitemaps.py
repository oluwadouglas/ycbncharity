from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # List of URL pattern names to include in the sitemap
        return [
            'charity:home',
            'charity:about',
            'charity:about_us',
            'charity:projects',
            'charity:programs',
            'charity:clubs',
            'charity:partner_schools',
            'charity:donations',
            'charity:impact',
            'charity:spotlight',
            'charity:articles',
            'charity:blog',
            'charity:contact',
            'charity:faq',
            'charity:gallery',
            'charity:pricing',
            'charity:volunteer',
            'charity:register',
            'login',  # Django auth login
        ]

    def location(self, item):
        return reverse(item)

# Exported sitemaps dict for project urls.py
sitemaps = {
    'static': StaticViewSitemap(),
}
