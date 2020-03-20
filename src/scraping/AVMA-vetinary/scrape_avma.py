from bs4 import BeautifulSoup, NavigableString, CData, Tag
from urllib import request, response, error, parse
from urllib.request import urlopen

def scrape():
  url = "https://www.avma.org/resources-tools/animal-health-and-welfare/covid-19"
  html = urlopen(url)
  soup = BeautifulSoup(html, "lxml")
  print(soup.text)

def main():
  scrape()

if __name__ == '__main__':
  main()
