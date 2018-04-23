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
            Chapter.objects.language(language).create(
                index=item['index'],
                label=item['label'],
                name=item['name'],
            )
        if item['type'] == 'article':
            chapter = Chapter.objects.language(language).get(
                index=item['chapter_index']
            )
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
            Section.objects.language(language).create(
                article_id=article.id,
                index=item['index'],
                parent_index=item.get('parent_index'),
                label=item.get('label'),
                content=item.get('content'),
            )
        if item['type'] == 'recital':
            Recital.objects.language(language).create(
                index=item['index'],
                text=item['content']
            )
        return item
