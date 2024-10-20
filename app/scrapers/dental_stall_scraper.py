import re
import ast
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag
from schemas.schemas import ScrapeRequestSchema
from cache.mem_cache import MemcachedCache
from database.json_database import JSONDatabase
from utils.files import Files
from queue_manager import QueueManager


class DentalStallScraper:

    @staticmethod
    def __extract_name(product: Tag) -> str:
        product_tag = product.find(
            "h2", class_="woo-loop-product__title").find("a")['href']
        product_name_slug = product_tag.rstrip('/').split('/')[-1]
        return product_name_slug.replace('-', ' ').title()

    @staticmethod
    def __extract_price(product: Tag) -> float:
        price = product.find(
            "span", class_="woocommerce-Price-amount amount").text
        match = re.findall(r"[-+]?\d*\.\d+|\d+", price)
        amount = 0.0
        if match:
            amount = float(match[0])
        return amount

    @staticmethod
    def __extract_image_urls(product: Tag, name: str) -> tuple[str, str]:
        image_tag = product.find(
            "img", class_="attachment-woocommerce_thumbnail")
        image_url = image_tag.get("data-lazy-src") or image_tag.get("src")
        local_path = Files.get_local_path(name, image_url)
        return image_url, local_path

    @staticmethod
    def __decode_cache(cached_data: bytes) -> list:
        decoded_string = cached_data.decode('utf-8')
        json_compatible_string = decoded_string.replace("'", '"')
        return ast.literal_eval(json_compatible_string)

    @staticmethod
    def scrape_catalogue(scrap_req: ScrapeRequestSchema) -> list:
        base_url = scrap_req.url
        cache = MemcachedCache()
        product_data = []

        proxies = {"http": scrap_req.proxy_url,
                   "https": scrap_req.proxy_url} if scrap_req.proxy_url else None

        for page in range(1, scrap_req.page_limit + 1):
            url = base_url + str(page)
            retry_limit = 2

            # check cache and return the details from here
            cached_data = cache.get(url)
            if cached_data:
                print(f"Using cached data for page: {page}")
                product_list = DentalStallScraper.__decode_cache(
                    cached_data=cached_data)
                for data in product_list:
                    product_data.append(data)
                continue

            try:
                # if not in DB
                response = requests.get(url, proxies=proxies)
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract product details
                products = soup.find_all("div", class_="product-inner")

                for product in products:

                    name = DentalStallScraper.__extract_name(
                        product=product)
                    amount = DentalStallScraper.__extract_price(
                        product=product)
                    image_url, local_path = DentalStallScraper.__extract_image_urls(
                        product=product, name=name)

                    Files.download_image(
                        download_url=image_url, local_path=local_path)

                    cache.set(key=url, value=product_data)
                    product_data.append(
                        {"name": name, "price": amount, "image": local_path})
            except Exception as ex:
                raise ex

        # Save to DB and cache
        db = JSONDatabase()
        print(f'\n\n\n org data --> {product_data}')
        db.save_data(data=product_data)

        return product_data
