#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from ricecooker.config import LOGGER

from webmixer.exceptions import BrokenSourceException, UnscrapableSourceException
from webmixer.scrapers.pages.base import HTMLPageScraper

class FullscreenPageScraper(HTMLPageScraper):
    """
        Generates a fullscreen preview page based on a url with an X to go back
        For instance, to convert an image to a fullscreen preview:
            scraper = FullscreenPageScraper(image_url)    # Create scraper
            link_to_image_page = scraper.to_tag()         # Create <a> tag with link to fullscreen preview page
            link_to_image_page.append(copy_of_image_tag)  # Add image to tag
            image_tag.replaceWith(link_to_image_page)     # Replace original element with new linked image
    """

    @classmethod
    def test(self, url):
        _, ext = os.path.splitext(url.split('?')[0])
        return ext

    def create_preview_tag(self):
        _, ext = os.path.splitext(self.url.split('?')[0])
        ext = ext.lower()
        if ext == '.pdf':
            embed = self.create_tag('embed')
            embed['src'] = self.write_url(self.url, default_ext='.pdf', directory='files')
            return embed
        elif ext in ['.png', '.jpeg', '.jpg', '.gif', '.svg']:
            img = self.create_tag('img')
            img['src'] = self.write_url(self.url, default_ext='.png', directory='img')
            return img
        else:
            raise NotImplementedError('Fullscreen page has not been implemented for {} files'.format(ext))

    def process(self):
        # Create main html page
        html = '<h2><a onclick="window.history.back()"></a></h2><div/>'
        contents = BeautifulSoup(html, 'html5lib')
        contents.find('div').append(self.create_preview_tag())

        # Create styles
        style = self.create_tag('style')
        style.string = "body {font-family: Arial,Helvetica,sans-serif; background-color:black;padding: 24px;}" \
                        "a {font-weight: bold; cursor: pointer;}" \
                        "h2 {text-align: right;}" \
                        "img, embed { width:100%; } embed {height:calc(100vh - 40px);}"
        contents.find('head').append(style)

        # Add close svg
        svg_html = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="32" height="32">' \
                    '<path d="M0 0h24v24H0z" fill="none"/>' \
                    '<path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>' \
                    '</svg>'
        svg = BeautifulSoup(svg_html, 'html.parser').find('svg')
        contents.find('a').append(svg)

        return contents.prettify(formatter="minimal").encode('utf-8', 'ignore')

    def to_tag(self, **kwargs):
        link = self.create_tag('a')
        filename, _ext = os.path.splitext(self.get_filename(self.url))
        link['href'] = self.to_zip(filename='{}.html'.format(filename))
        self.mark_tag_to_skip(link)
        return link
