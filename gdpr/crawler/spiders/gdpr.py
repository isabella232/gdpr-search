# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose


LANGUAGES = [
    'BG',
    'ES',
    'CS',
    'DA',
    'DE',
    'ET',
    'EL',
    'EN',
    'FR',
    'GA',
    'HR',
    'IT',
    'LV',
    'LT',
    'HU',
    'MT',
    'NL',
    'PL',
    'PT',
    'RO',
    'SK',
    'SL',
    'FI',
    'SV',
]


class TakeFirstLoader(ItemLoader):
    default_item_class = dict
    default_output_processor = TakeFirst()

    content_out = Compose(
        lambda x: ' '.join(x)
    )


def load_section(section_selector, current_language, article_index, section_index, parent_section_index=None):
    section_loader = TakeFirstLoader(selector=section_selector)
    section_loader.add_value('type', 'section')
    section_loader.add_value('language', current_language)
    section_loader.add_value('article_index', article_index)
    section_loader.add_value('index', section_index)
    section_loader.add_value('parent_index', parent_section_index)
    section_loader.add_xpath('label', './tbody/tr/td[1]/p/text()')

    section_loader.add_xpath('content', './tbody/tr/td[2]/p/text()')
    section_loader.add_xpath('content', './text()|./span/text()')

    for subsection_index, subsection_selector in enumerate(section_selector.xpath('./tbody/tr/td[2]/table')):
        for subsection in load_section(
            subsection_selector,
            current_language,
            article_index,
            subsection_index,
            parent_section_index=section_index
        ):
            yield subsection

    yield section_loader.load_item()


class GdprinfoSpider(scrapy.Spider):
    name = 'gdpr'
    allowed_domains = [
        'eur-lex.europa.eu'
    ]

    def __init__(self, target, *args, **kwargs):
        self.target = target

        super().__init__(*args, **kwargs)

    def start_requests(self):
        for language in LANGUAGES:
            yield scrapy.Request(
                f'http://eur-lex.europa.eu/legal-content/{language}/TXT/HTML/?uri=CELEX:32016R0679&from=EN',
                callback=getattr(self, f'parse_{self.target}'),
                meta={
                    'language': language
                }
            )

    def parse_recitals(self, response):
        current_language = response.meta.get('language')

        recitals_selector = response.xpath(
            '//body/table[count(preceding-sibling::p[@class="ti-section-1"][span[@class="italic"]]) = 0][position()>1]'
        )
        for recital_selector in recitals_selector:
            recital_loader = TakeFirstLoader(selector=recital_selector)
            recital_loader.add_value('type', 'recital')
            recital_loader.add_value('language', current_language)

            recital_index = int(recital_selector.xpath(
                './tbody/tr/td[1]/p/text()'
            ).extract_first().replace('(', '').replace(')', ''))
            recital_loader.add_value(
                'index',
                recital_index
            )
            recital_loader.add_xpath(
                'content',
                './tbody/tr/td[2]/p/text()'
            )

            yield recital_loader.load_item()

    def parse_contents(self, response):
        current_language = response.meta.get('language')

        chapter_xpath = 'p[@class="ti-section-1"][span[@class="italic"]]'
        article_xpath = 'p[@class="sti-art"]'

        chapter_selectors = response.xpath(f'//{chapter_xpath}')
        total_chapters = len(chapter_selectors)
        article_index = 1

        for chapter_index, chapter_selector in enumerate(chapter_selectors, start=1):

            chapter_loader = TakeFirstLoader(selector=chapter_selector)
            chapter_loader.add_value('type', 'chapter')
            chapter_loader.add_value('language', current_language)
            chapter_loader.add_value('index', chapter_index)
            chapter_loader.add_xpath('label', './span/text()')
            chapter_loader.add_xpath('name', './following-sibling::p[1]/span/span/text()')
            yield chapter_loader.load_item()

            article_selectors = response.xpath(
                f'//{article_xpath}'
                f'[count(following-sibling::{chapter_xpath})={total_chapters - chapter_index}]'
                f'[count(preceding-sibling::{chapter_xpath})={chapter_index}]'
            )

            for article_selector in article_selectors:
                article_loader = TakeFirstLoader(selector=article_selector)
                article_loader.add_value('type', 'article')
                article_loader.add_value('language', current_language)
                article_loader.add_value('chapter_index', chapter_index)
                article_loader.add_value('index', article_index)
                article_loader.add_xpath('label', './preceding-sibling::p[@class="ti-art"][1]/text()')
                article_loader.add_xpath('name', './text()')
                yield article_loader.load_item()

                section_selectors = response.xpath(
                    f'//body/p[@class="normal"][count(preceding-sibling::{article_xpath}) = {article_index}]'
                    f'|'
                    f'//body/table[count(preceding-sibling::{article_xpath}) = {article_index}]'
                )

                for section_index, section_selector in enumerate(section_selectors):
                    for section in load_section(section_selector, current_language, article_index, section_index):
                        yield section

                article_index += 1
