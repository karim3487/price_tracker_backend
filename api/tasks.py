from celery import shared_task
import requests

from api.models import TrackedProduct
from price_tracker.settings import SCRAPER_API_URL


@shared_task
def run_scraper(product_url):
    response = requests.post(SCRAPER_API_URL, json={"url": product_url})
    return response.json()


@shared_task
def check_all_products():
    print("Checking all products...")
    for tracked in TrackedProduct.objects.filter(is_active=True):
        run_scraper.delay(tracked.product.url)
