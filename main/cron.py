import aiohttp
from config import settings
import requests
from main.models import Products

def cron_job():
    code = {
        "limit": 100,
        "start": 0,
        "filters": {
            "warehouse_id": {"eq": 6}
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "accessToken": settings.ACCESS_TOKEN,
        "x-auth": settings.X_TOKEN
    }
    response = requests.post("https://apps.kpi.com/services/api/v2/2/products_zapier", json=code, headers=headers)
    print("API======", response.status_code)
    print("KPI=======", response.content)
    products = response.json()
    for product_data in products:
        product, created = Products.objects.get_or_create(
            k_id=product_data['id'],
            defaults={
                'k_id': product_data['id'],
                'number': product_data['number'],
                'p_quantity': product_data['quantity'],
                # ... other fields ...
            }
        )
        if not created:
            product.k_id = product_data['id']
            product.number = product_data['number']
            product.p_quantity = product_data['quantity']
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
