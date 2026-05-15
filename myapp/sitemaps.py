from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'index',
            'men',
            'women',
            'kids',
            'contact',
            'register',
            'login_page',
            'profile',
            'product_list',
            'cart_page',
        ]

    def location(self, item):
        return reverse(item)