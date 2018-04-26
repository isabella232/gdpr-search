from django.core.management.base import BaseCommand
from django.conf import settings
from numeral.numeral import int2roman

from algoliasearch import algoliasearch

from gdpr.gdpr.models import Chapter, Article, Section, Recital

client = algoliasearch.Client(
    settings.ALGOLIA['APPLICATION_ID'],
    settings.ALGOLIA['API_KEY']
)
LANGUAGES = [
    'en',
    'hr',
    'it',
    'ro',
    'et',
    'cs',
    'el',
    'pl',
    'sk',
    'ga',
    'fi',
    'sl',
    'pt',
    'sv',
    'de',
    'fr',
    'mt'
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Indexing chapters')
        for language in LANGUAGES:
            index = client.init_index(f'dev_GDRPR_chapters_{language}')
            index.set_settings({
                'searchableAttributes': [
                    'label',
                    'unordered(name)'
                ]
            })
            index.add_objects(
                {
                    'objectID': chapter['id'],
                    **chapter
                }
                for chapter in Chapter.objects.language(language).values(
                    'id',
                    'index',
                    'label',
                    'name',
                )
            )
            for i in range(1, 20):
                index.save_synonym({
                    'objectID': int2roman(i, only_ascii=True),
                    'type': 'oneWaySynonym',
                    'input': str(i),
                    'synonyms': [
                        int2roman(i, only_ascii=True)
                    ]
                }, int2roman(i, only_ascii=True), False)
        self.stdout.write('Indexing articles')
        for language in LANGUAGES:
            index = client.init_index(f'dev_GDRPR_articles_{language}')
            index.set_settings({
                'searchableAttributes': [
                    'chapter__label',
                    'unordered(chapter__name)'
                    'label',
                    'unordered(name)',
                ]
            })
            index.add_objects(
                {
                    'objectID': article.id,
                    'id': article.id,
                    'index': article.index,
                    'label': article.label,
                    'name': article.name,
                    'chapter__index': article.chapter.index,
                    'chapter__label': article.chapter.label,
                    'chapter__name': article.chapter.name,
                }
                for article in Article.objects.language(language).select_related(
                    'chapter'
                ).all()
            )
            for i in range(1, 20):
                index.save_synonym({
                    'objectID': int2roman(i, only_ascii=True),
                    'type': 'oneWaySynonym',
                    'input': str(i),
                    'synonyms': [
                        int2roman(i, only_ascii=True)
                    ]
                }, int2roman(i, only_ascii=True), False)
        self.stdout.write('Indexing sections')
        for language in LANGUAGES:
            index = client.init_index(f'dev_GDRPR_sections_{language}')
            index.set_settings({
                'searchableAttributes': [
                    'chapter__label',
                    'unordered(chapter__name)',
                    'article__label',
                    'unordered(article__name)',
                    'unordered(content)',
                ]
            })
            index.add_objects(
                {
                    'objectID': section.id,
                    'id': section.id,
                    'index': section.index,
                    'label': section.label,
                    'content': section.content,
                    'article__index': section.article.index,
                    'article__label': section.article.label,
                    'article__name': section.article.name,
                    'chapter__index': section.article.chapter.index,
                    'chapter__label': section.article.chapter.label,
                    'chapter__name': section.article.chapter.name,
                }
                for section in Section.objects.language(language).select_related(
                    'article',
                    'article__chapter',
                ).all()
            )
            for i in range(1, 20):
                index.save_synonym({
                    'objectID': int2roman(i, only_ascii=True),
                    'type': 'oneWaySynonym',
                    'input': str(i),
                    'synonyms': [
                        int2roman(i, only_ascii=True)
                    ]
                }, int2roman(i, only_ascii=True), False)
        self.stdout.write('Indexing recitals')
        for language in LANGUAGES:
            index = client.init_index(f'dev_GDRPR_recitals_{language}')
            index.set_settings({
                'searchableAttributes': [
                    'unordered(text)'
                ],
                'attributesToSnippet': [
                    'text:15'
                ]
            })
            index.add_objects(
                {
                    'objectID': recital['id'],
                    **recital
                }
                for recital in Recital.objects.language(language).values(
                    'id',
                    'index',
                    'text'
                )
            )
