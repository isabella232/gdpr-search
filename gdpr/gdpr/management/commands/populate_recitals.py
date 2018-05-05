from django.core.management.base import BaseCommand
from django.conf import settings

from gdpr.gdpr.models import Article, Recital


class Command(BaseCommand):
    def handle(self, *args, **options):

        english_recitals = list(Recital.objects.language('en').all())

        for language in settings.LANGUAGES:
            language_code = language[0]

            if language_code == 'en':
                continue

            for english_recital in english_recitals:
                recital = Recital.objects.language(language_code).get(index=english_recital.index)
                english_linked_articles_indexes = list(english_recital.articles.language('en').values_list(
                    'index',
                    flat=True
                ))
                for article_to_add in Article.objects.language(language_code).filter(index__in=english_linked_articles_indexes):
                    recital.articles.add(article_to_add)