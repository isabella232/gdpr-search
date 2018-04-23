from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, View

from .models import Article, Chapter


def get_article_with_sections(article):
    article.sections_list = []
    for section in article.sections.language().filter(parent_index__isnull=True):
        section.subsections = article.sections.language().filter(parent_index=section.index)
        article.sections_list.append(section)

    return article


class IndexView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):

        article = get_article_with_sections(Article.objects.language().first())
        try:
            next_article = Article.objects.language().get(index=article.index+1)
        except ObjectDoesNotExist:
            next_article = None

        return super().get_context_data(
            chapters=Chapter.objects.language().all(),
            article=get_article_with_sections(Article.objects.language().first()),
            next_article=next_article,
            **kwargs
        )


class ArticleView(TemplateView):

    template_name = 'index.html'

    def get_article(self):
        slug = self.kwargs['slug']
        article = Article.objects.language().get(slug=slug)

        return get_article_with_sections(article)

    def get_context_data(self, **kwargs):

        article = self.get_article()

        try:
            next_article = Article.objects.language().get(index=article.index+1)
        except ObjectDoesNotExist:
            next_article = None

        return super().get_context_data(
            chapters=Chapter.objects.language().all(),
            article=self.get_article(),
            next_article=next_article,
            **kwargs
        )


class DefinitionsView(View):

    def get(self, *args, **kwargs):
        definitions = [
            {

            }
            for definition in Article.objects.language().filter(index)
        ]
