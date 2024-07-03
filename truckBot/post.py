import time
import os
import re
import django

from django.core.cache import cache
from django.contrib import messages

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
django.setup()

def posting_load(request, headless=True):
    pass    