import json

import requests
from lxml import etree
import re
import html
import shutil
from bs4 import BeautifulSoup
from config import settings
from src.exceptions import PageIdNotFoundError
from src.exceptions import PageDetailNotFoundError
from src.model.Book import Book


class CorteInglesWebScrapingService:

    def __init__(self):
        self.MAX_ATTEMPS = 10

        self.ISBN = 'ISBN:'
        self.PUBLICATION_DATE = 'Fecha de Lanzamiento:'
        self.EDITORIAL = 'Editorial:'
        self.FORMAT_BINDING = 'Formato de encuadernación:'
        self.PAGES_NUMBER = 'Número de páginas:'
        self.DIMENTIONS = 'Dimensiones:'
        self.LANGUAGE = 'Idioma:'
        self.COLLECTION = 'Colección:'
        self.SINOPSIS = 'Prelectura del libro:'
        self.GENERE = 'Género:'
        self.SUB_GENERE = 'Subgénero:'

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "es-ES,es;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "txzIlGC0bC/F/LKDl3NH79In40uJqv41OJ4Mj0sZPArPZpvj0VXrhINjVuxBm864JWors; _gid=GA1.2.135615697.1590563291; FECISA_T7=!3WlZjKBtVKzC8yg0ZC+zbRaBPjrfUxWaoizg0xhlMbKrtdzbsSeXpPMg81YOYPJ/nvDT2Wv2Kg==; locale=es_ES; site=eciStore; es=1; _uetsid=2248d20d-ac93-7a36-328b-87ddbd7ff67e; qb_permanent=o8fcmj5wev4-0k81yhvkg-3dj4ho0:19:9:2:4:0::1:2:79.9:Bedl9M:BezhaQ:BedmEX:BedmEX::::barcelona:11259:spain:ES:::unknown:unknown:barcelona:11419:migrated|1590563292283:EggD==B=CDMk=On::XJVCCGv:XJU9cQO:0:0:0::0:0:.elcorteingles.es:0; qb_session=9:1:81::0:XJU9cQO:0:0:0:0:.elcorteingles.es; rr_rcs=eF4FwbENgDAMBMAmFbu8ZMfvBG_AHImDREEH",
            "Host": "www.elcorteingles.es",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }


    def execute(self, web_scraping_url):
        try:
            book_store_page = requests.get(url=web_scraping_url, headers=self.headers, stream=True)
            books = []
            f = open("books.json", "a+")

            if book_store_page.status_code != 200:
                raise PageIdNotFoundError

            main_tree = etree.HTML(book_store_page.text).xpath('//div[@class="info"]')

            for i in range(0, len(main_tree)):
                url_to_book_detail = main_tree[0].xpath('//div[@class="product-name"]//a[@href]')[i].attrib['href']

                detail_tree = self.get_book_detail_page_data(url_to_book_detail)
                if detail_tree is not None:
                    book_title = detail_tree.xpath('//div[@id="product-info"]/h2/text()')[0]
                    book_author = detail_tree.xpath('//div[@id="product-info"]//div[@id="leisure-box"]//dd/a/text()')[0] \
                        if len(detail_tree.xpath('//div[@id="product-info"]//div[@id="leisure-box"]//dd/a/text()')) > 0 \
                        else 'Desconocido'
                    book_price = detail_tree.xpath('//div[@id="product-info"]//span[@itemprop="price"]/text()')[0]

                    book_dynamic_field_list = detail_tree.xpath('//div[@id="media-info"]//dt/text()')
                    book_dynamic_content_list = detail_tree.xpath('//div[@id="media-info"]//dd')
                    book_dynamic_content = {}

                    for j in range(0, len(book_dynamic_field_list)):
                        book_dynamic_content[book_dynamic_field_list[j].replace(':', '').replace(' ', '')] = book_dynamic_content_list[j].text

                    book_description_html = etree.tostring(detail_tree.xpath('//div[@id="description"]//div[@class="description-container"]')[0]) \
                        if len(detail_tree.xpath('//div[@id="description"]//div[@class="description-container"]')) > 0 \
                        else ''

                    book_description_soup = BeautifulSoup(book_description_html, "html.parser")
                    book_description = book_description_soup.get_text()

                    book = Book(i)
                    book.set_book_title(book_title)
                    book.set_author(book_author)
                    book.set_price(book_price)
                    book.set_description(book_description)
                    book.set_dynamic_content(book_dynamic_content)
                    books.append(book)
                    jsonStr = json.dumps(book.__dict__)

                    f.write(jsonStr + "\n")
                    print(i, ' book processed')
                else:
                    print(i, ' book escaped')

            # TODO: Lluis,
            # Quitar la escritura del fichero, y llamar a
            # BookRepository.persist(books) para introducir en el Elastic una lista con 24 libros (libros por pagina),
            # puedes utilizar la lista de libros en <books>, o si te es más facil persiste los libros uno a uno, como veas!
            f.close()


        except PageIdNotFoundError as e:
            raise PageIdNotFoundError
        except Exception as e:
            raise Exception(e)

    def get_book_detail_page_data(self, url):
        i = 0
        while i < self.MAX_ATTEMPS:
            book_detail_page = \
                requests.get(url=settings.CORTE_INGLES_URL + url, headers=self.headers, stream=True,
                             allow_redirects=False)

            if book_detail_page.status_code != 200:
                print('Something went wrong loading detail-page, code:%d' % book_detail_page.status_code)
                print(book_detail_page.url)
                i += 1
            else:
                detail_soup = BeautifulSoup(book_detail_page.text, 'html.parser')
                product_info_soup = detail_soup.find("div", {"id": "product-info"})
                return etree.HTML(str(product_info_soup))
        return None