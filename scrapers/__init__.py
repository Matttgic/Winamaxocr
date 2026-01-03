"""
Package de scrapers pour Winamax
"""
from .selenium_scraper import SeleniumScraper
from .playwright_scraper import PlaywrightScraper
from .ocr_scraper import OCRScraper

__all__ = ['SeleniumScraper', 'PlaywrightScraper', 'OCRScraper']
