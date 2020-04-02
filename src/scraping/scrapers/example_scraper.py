from covid_scraping import Scraper
from covid_scraping import Conversion, test_jsonlines

class ExampleScraper(Scraper):
    """Scrapers a website for FAQs and stores the output to a file"""
    def scrape(self):
        converter = Conversion(self.filename, self.path)
        # Put the code here that makes the 
        for exampleNums in range(10):
            converter.addExample({ 
                'sourceUrl': 'example.com',
                'sourceName': "example",
                "sourceDate": 1585777414.515401,
                "lastUpdateTime": 1585777414.515401,
                "needUpdate": True,
                "typeOfInfo": "QA",
                "isAnnotated": False,
                "responseAuthority": "",
                "question": '<a href="example.com/dir1">What is COVID-19?</a>',
                "answer": '<p><a href="example.com/dir2">Coronaviruses</a> are a large family of viruses.</p>',
                "hasAnswer": True,
                "targetEducationLevel": "NA",
                "topic": ['topic1', 'topic2'],
                "extraData": {'hello': 'goodbye'},
                "targetLocation": "US",
                "language": 'en',
            })
        # This write() will fail because the path doesnt exist
        return converter.write()

   
def main():

    scraper = ExampleScraper("./", "example")
    scraper.scrape()

if __name__ == '__main__':
    main()


 
