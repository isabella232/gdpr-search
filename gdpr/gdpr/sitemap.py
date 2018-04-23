from django.contrib.sitemaps import Sitemap

from .models import Article


class GdprSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.language('en').all()
