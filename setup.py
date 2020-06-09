
from setuptools import find_packages, setup

readme = open('README.md').read()

with open('docs/history.rst') as history_file:
    history = history_file.read()

# Read requirements from requirements.txt
requirements_raw = open('requirements.txt').readlines()
requirements = [l.strip() for l in requirements_raw if l.strip() and not l.startswith('#')]


setup(
    name="webmixer",
    packages = find_packages(),
    version="0.0.1",
    description="Library for scraping urls and downloading them as files",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    license="MIT",
    url="https://github.com/learningequality/webmixer",
    download_url="https://github.com/learningequality/webmixer/releases",
    keywords="scrapers webmixer web-mixer mixer scraper",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    author="Learning Equality",
    author_email='dev@learningequality.org',
)
