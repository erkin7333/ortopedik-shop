import aiohttp
from config import settings
import requests
from main.models import Products


def cron_job():
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "accessToken": settings.ACCESS_TOKEN,
        "x-auth": settings.X_TOKEN
    }
    response = requests.post("https://apps.kpi.com/services/api/v2/2/product_variants_zapier?warehouse_id=6",
                             headers=headers)
    products = response.json()
    for product_data in products:
        data_id = [d['id'] for d in product_data]
        data_number = [d['sku_number'] for d in product_data]
        data_quantity = [q['quantity'] for q in product_data]
        product, created = Products.objects.get_or_create(
            k_id=data_id,
            defaults={
                'number': data_number,
                'p_quantity': data_quantity,
                # ... other fields ...
            }
        )
        if not created:
            product.k_id = data_id
            product.number = data_number
            product.p_quantity = data_quantity
            product.save()


# path('django_crontab/', include('crontab.urls'))


async def get_api_date(limit=1000, strat=0):
    """API dan ma'lumotlarni olish uchun async funktsiyasi"""

    code = {
        "limit": limit,
        "start": strat
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "accessToken": settings.ACCESS_TOKEN,
        "x-auth": settings.X_TOKEN
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f"https://apps.kpi.com/services/api/v2/2/products/", json=code) as response:
            api_product = await response.json()
    return api_product
