
# https://github.com/mozilla/geckodriver/releases
from selenium import webdriver

browser = webdriver.Firefox(executable_path='E:\\books\\geckodriver-v0.30.0-win64\\geckodriver.exe')
browser.get('http://localhost:8000')

assert 'Django' in browser.title