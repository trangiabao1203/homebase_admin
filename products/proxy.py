import requests
import logging
from decouple import config
from .models import Product

API_HOST = config('API_HOST')
API_ENDPOINT = f'{API_HOST}/products'

class ProductProxy(Product):
    class Meta:
        proxy = True
        verbose_name = "Product"

    @staticmethod
    def handle_response(response):
        try:
            data = response.json()
            if 200 <= response.status_code < 300:
                if 'data' in data:
                    return data['data']
                return None
            else:
                logging.error(f"API Error: {data.get('message', 'Unknown error')}")
                print(data)
                return None
        except ValueError as e:
            logging.error(f"JSON decoding failed: {e}")
            return None

    @classmethod
    def get_list(cls):
        response = requests.get(f'{API_ENDPOINT}')
        data = ProductProxy.handle_response(response)
        items = []
        if data and 'items' in data and isinstance(data['items'], list):
            items = [cls(**prod) for prod in data['items']]
        return {
            "items": items,
            "total": data['totalItems']
        }

    @classmethod
    def get_by_id(cls, product_id):
        response = requests.get(f'{API_ENDPOINT}/{product_id}')
        data = ProductProxy.handle_response(response)
        if data:
            return Product(**data)
        return None

    @classmethod
    def save(cls, change):
        headers = {'Content-Type': 'application/json'}
        try:
            if hasattr(change, 'id') and change.id:
                response = requests.put(f'{API_ENDPOINT}/{change.id}', json=change.to_dict(), headers=headers)
            else:
                response = requests.post(f'{API_ENDPOINT}', json=change.to_dict(), headers=headers)
            data = ProductProxy.handle_response(response)
            if data:
                return Product(**data)
            return None
        except requests.RequestException as e:
            logging.error(f"Network error: {e}")
            return None

    @classmethod
    def delete(cls, change):
        try:
            if hasattr(change, 'id') and change.id:
                response = requests.delete(f'{API_ENDPOINT}/{change.id}')
                data = ProductProxy.handle_response(response)
                return None
            else:
                logging.warning("Product does not have an ID.")
                return None
        except requests.RequestException as e:
            logging.error(f"Network error: {e}")
            return None
