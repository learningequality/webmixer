
from setuptools import find_packages, setup

long_description = open('README.md').read()

requirements = [
    "pycountry==17.5.14",
]

setup(
    name="webmixer",
    packages = find_packages(),
    version="0.0.0",
    description="Library for scraping urls and downloading them as files",
    long_description=long_description,
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
    author="Jordan Yoshihara",
    author_email="jordan@learningequality.org",
)
