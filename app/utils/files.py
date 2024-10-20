import os
import requests
from urllib.parse import urlparse


class Files:

    @staticmethod
    def get_local_path(name: str, url: str) -> str:
        _, ext = os.path.splitext(urlparse(url).path)
        safe_name = name.replace(' ', '_').replace('/', '_')
        return os.path.join("downloaded_images", f"{safe_name}{ext}")

    @staticmethod
    def download_image(download_url: str, local_path: str) -> None:
        try:
            response = requests.get(url=download_url)
            response.raise_for_status()

            # write to local storage for now, can move to s3 in future
            with open(local_path, 'wb') as f:
                f.write(response.content)

        except Exception as e:
            print(f"Failed to download image from {download_url}. Reason: {e}")
