from src.exceptions import PageIdNotFoundError
from src.repository.BookRepository import BookRepository
from src.services.corte_ingles.CorteInglesWebScrapingService import CorteInglesWebScrapingService
from config import settings
import pathlib


class BookRaptorScraper(object):

    conn = None

    def __init__(self):
        # Connect to the Database
        # TODO: Pending to handler the connection with the db
        conn = 'connection'
        self.conn = conn


    def start(self):
        corte_ingles_scrap = CorteInglesWebScrapingService()
        repository = BookRepository(self.conn)
        for page_id in range(1, 416):
            try:
                corte_ingles_url = settings.CORTE_INGLES_URL \
                                   + settings.CORTE_INGLES_CATEGORY \
                                   + str(page_id) \
                                   + settings.CORTE_INGLES_LANGUAGE

                corte_ingles_scrap.execute(corte_ingles_url)

                #TODO: Luis, pending to add more scrapy services

                print('Page %d processed' % page_id)

            except PageIdNotFoundError as e:
                print('Page %d not found' % page_id)
            except Exception as e:
                print('An error ocurred while scraping Page Id %d. %s ' % (page_id, e.args[0]))


def main():
    scraper = BookRaptorScraper()
    scraper.start()


if __name__ == '__main__':
    main()
