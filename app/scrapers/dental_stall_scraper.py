import os
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from schemas.schemas import ScrapeRequestSchema


class DentalStallScraper:

    @staticmethod
    def get_image_filename(name: str, url: str) -> str:
        _, ext = os.path.splitext(urlparse(url).path)
        safe_name = name.replace(' ', '_').replace('/', '_')
        return os.path.join("downloaded_images", f"{safe_name}{ext}")

    @staticmethod
    def download_image(url: str, save_path: str):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            with open(save_path, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Failed to download image from {url}. Reason: {e}")

    def scrape_catalogue(scrap_req: ScrapeRequestSchema):
        base_url = scrap_req.url
        product_data = []

        proxies = {"http": scrap_req.proxy_url,
                   "https": scrap_req.proxy_url} if scrap_req.proxy_url else None

        for page in range(1, scrap_req.page_limit + 1):
            url = base_url + str(page)
            response = requests.get(url, proxies=proxies)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract product details
            products = soup.find_all("div", class_="product-inner")

            for product in products:

                # Step 1: Grab the href link
                product_tag = product.find(
                    "h2", class_="woo-loop-product__title").find("a")['href']

                # Step 2: Extract the last part of the URL (product name)
                product_name_slug = product_tag.rstrip('/').split('/')[-1]

                # Step 3: Convert slug to title case
                name = product_name_slug.replace('-', ' ').title()

                price = product.find(
                    "span", class_="woocommerce-Price-amount amount").text
                match = re.findall(r"[-+]?\d*\.\d+|\d+", price)
                amount = 0
                if match:
                    amount = float(match[0])

                # Extract image URL
                image_tag = product.find(
                    "img", class_="attachment-woocommerce_thumbnail")
                image_url = image_tag.get(
                    "data-lazy-src") or image_tag.get("src")
                print(image_url)

                # Step 4: Download the image and save it locally
                image_filename = DentalStallScraper.get_image_filename(
                    name, image_url)
                print(f'image_filename--> {image_filename}')
                DentalStallScraper.download_image(image_url, image_filename)

                product_data.append(
                    {"name": name, "price": amount, "image": image_filename})

        return product_data
