from bs4 import BeautifulSoup
import requests
import re

page = requests.get('https://www.linkedin.com/jobs/search/?keywords=intern&location=Bengaluru%2C%20Karnataka%2C%20India')
# print(page.content)
soup = BeautifulSoup(page.content, features="lxml")
print(soup.find_all(attrs={"id": "ember137"}))
for x in soup.find_all(attrs={"class": "application-outlet"}):
    print(x)
