#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import shutil

from webmixer.reporting import session_reporter
from webmixer.utils import create_tag, create_copy_link_message, generate_filename, get_absolute_url

class BasicScraper(object):
    directory = None             # Directory to write files to
    color = 'rgb(153, 97, 137)'  # Color for error messages
    locale = 'en'                # Language to use when writing error messages
    default_ext = None           # Extension to default to for extracted files

    def __init__(self, url, zipper=None, triaged=None, locale=None, base_url=None):
        """
            url (str): URL to read from
            zipper (optional ricecooker.utils.html_writer): zip to write to
            triaged ([str]): list of already parsed URLs
            locale (str): locale code for content locale
            base_url (str): If url is relative, the root the path is relative to
        """
        self.url = url
        self.rel_url = url
        self.base_url = base_url
        self.triaged = triaged or {}
        if locale:
            self.locale = locale
        if self.base_url:
            self.url = self.base_url + self.url
        self.zipper = zipper

    def create_tag(self, tag):
        """
            Returns a BeautifulSoup tag
            Args:
                tag (str): tag name to create (e.g. 'p')
        """
        return create_tag(tag)

    def get_filename(self, link, default_ext=None):
        """
            Returns a filename (str) to use for extracted files
            Args:
                link (str): URL that has been scraped
                default_ext (optional str): if the link doesn't have an extension, use this extension
        """
        return generate_filename(link, default_ext=default_ext or self.default_ext)

    def mark_tag_to_skip(self, tag):
        """
            Mark tag to skip during scraping
            Args:
                tag (str): tag to mark
        """
        # Some tags, e.g. script tags with JS content, can have attrs be None
        if not tag.attrs:
            tag.attrs = {}
        tag['class'] = tag.get('class') or [] + ['skip-scrape']

    def write_url(self, link, url=None, default_ext=None, filename=None, directory=None):
        """
            Writes a url to zip
            Args:
                filepath (str): path to local file
                directory (str): directory to write to zip
                url (optional str): URL used for handling relative URLs
                default_ext (optional str): if the link doesn't have an extension, use this extension
                filename (optional str): name for file to write to zip
                directory (optional str): directory to write file to zip
            Returns filepath within zip
        """
        filename = filename or self.get_filename(link, default_ext=default_ext)
        if self.zipper:
            return self.zipper.write_url(get_absolute_url(url or self.url, link), filename, directory=directory or self.directory)
        full_path = filename if not directory else os.path.join(directory, filename)
        return full_path

    def write_contents(self, filename, contents, directory=None):
        """
            Writes contents to a zip
            Args:
                filename (str): filename for contents
                contents (bytes): contents to write to zip
                directory (str): directory to write to zip
            Returns filepath within zip
        """
        if self.zipper:
            return self.zipper.write_contents(filename, contents, directory=directory or self.directory)

        full_path = filename if not directory else os.path.join(directory, filename)
        f = open(full_path, mode="wb")
        f.write(contents)
        f.close()
        return full_path

    def write_file(self, filepath, directory=None):
        """
            Writes a local file to the zip
            Args:
                filepath (str): path to local file
                directory (str): directory to write to zip
            Returns filepath within zip
        """
        if self.zipper:
            return self.zipper.write_file(filepath, os.path.basename(filepath), directory=directory or self.directory)

        shutil.copy(filepath, directory)


    def create_broken_link_message(self, link):
        """
        Returns a div tag with a link to copy/paste into browser
            Args:
                link (str): link to copy/paste
        """
        return create_copy_link_message(link, locale=self.locale, color=self.color, broken=True)

    def create_copy_link_message(self, link, partially_scrapable=False):
        """
            Returns a div tag with a link to copy/paste into browser
            Args:
                link (str): link to copy/paste
                partially_scrapable (bool): link was mostly scraped, but doesn't include everything from original site
        """
        return create_copy_link_message(link, locale=self.locale, color=self.color, partially_scrapable=partially_scrapable)
