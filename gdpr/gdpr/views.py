import json

from django.utils.functional import cached_property
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

from .models import Article, Chapter, Definition


def get_definitions(article):
    return json.dumps({
        definition_object.term: definition_object.definition.content
        for definition_object in Definition.objects.filter(
            language_code=article.language_code
        )
    })


def get_article_with_sections(article):
    article.sections_list = []
    for section in article.sections.filter(parent_index__isnull=True):
        section.subsections = article.sections.filter(parent_index=section.index)
        article.sections_list.append(section)

    return article


class IndexView(TemplateView):

    template_name = 'index.html'

    @cached_property
    def article(self):
        return get_article_with_sections(
            Article.objects.language().prefetch_related('chapter', 'sections').first()
        )

    def get_context_data(self, **kwargs):

        try:
            next_article = Article.objects.language().get(index=self.article.index+1)
        except ObjectDoesNotExist:
            next_article = None

        return super().get_context_data(
            chapters=Chapter.objects.language().prefetch_related('articles').all(),
            article=self.article,
            next_article=next_article,
            definitions=get_definitions(self.article),
            **kwargs
        )


class ArticleView(TemplateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return '_article.html'
        else:
            return 'index.html'

    @cached_property
    def article(self):
        index = self.kwargs['id']
        article = Article.objects.language().prefetch_related(
            'chapter',
            'sections'
        ).get(index=index)

        return get_article_with_sections(article)

    def get_context_data(self, **kwargs):

        try:
            next_article = Article.objects.language().get(index=self.article.index+1)
        except ObjectDoesNotExist:
            next_article = None

        return super().get_context_data(
            chapters=Chapter.objects.language().all(),
            article=self.article,
            next_article=next_article,
            definitions=get_definitions(self.article),
            **kwargs
        )
