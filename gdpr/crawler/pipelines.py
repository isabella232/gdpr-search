# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.core.exceptions import ObjectDoesNotExist

from gdpr.gdpr.models import Chapter, Article, Section, Recital


class GdprPipeline(object):
    def process_item(self, item, spider):
        language = item['language'].lower()
        if item['type'] == 'chapter':
            try:
                chapter = Chapter.objects.language(language).get(index=item['index'])
                chapter.label = item['label']
                chapter.name = item['name']
                chapter.save()
            except ObjectDoesNotExist:
                Chapter.objects.language(language).create(
                    index=item['index'],
                    name=item['name'],
                    label=item['label']
                )

        if item['type'] == 'article':
            chapter = Chapter.objects.language(language).get(
                index=item['chapter_index']
            )
            try:
                article = Article.objects.language(language).get(
                    chapter_id=chapter.id,
                    index=item['index']
                )
                article.label = item['label']
                article.name = item['name']
                article.save()
            except ObjectDoesNotExist:
                Article.objects.language(language).create(
                    chapter_id=chapter.id,
                    index=item['index'],
                    label=item['label'],
                    name=item['name'],
                )

        if item['type'] == 'section':
            article = Article.objects.language(language).get(
                index=item['article_index']
            )
            try:
                section = Section.objects.language(language).get(
                    article_id=article.id,
                    index=item['index'],
                    parent_index=item.get('parent_index'),
                )
                section.label = item.get('label')
                section.content = item.get('content')
                section.save()
            except ObjectDoesNotExist:
                Section.objects.language(language).create(
                    article_id=article.id,
                    index=item['index'],
                    parent_index=item.get('parent_index'),
                    label=item.get('label'),
                    content=item.get('content'),
                )

        if item['type'] == 'recital':
            try:
                recital = Recital.objects.language(language).get(
                    index=item['index'],
                )
                recital.text = item['content']
                recital.save()
            except ObjectDoesNotExist:
                Recital.objects.language(language).create(
                    index=item['index'],
                    text=item['content']
                )
        return item
