import aiohttp
from config import settings
import requests
from main.models import Products


def cron_job():
    code = {
        "filters": [
            {
                "filterCodeName": "warehouseId",
                "items": [
                    {
                        "id": 6
                    }
                ]
            }
        ],
        "limit": 5,
        "start": 0
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "accessToken": settings.ACCESS_TOKEN,
        "x-auth": settings.X_TOKEN
    }
    response = requests.post("https://apps.kpi.com/services/api/v3/product/list", json=code, headers=headers)
    response_data = response.json()
    products = response_data.get('data', {}).get('items', [])
    if isinstance(products, list):
        data_id = [d['id'] for d in products]
        data_number = [d['number'] for d in products]
        sellingPrice = [d['sellingPrice'] for d in products]
        p_salesAccount = [d['inventoryStockInformation'] for d in products]
        qtyOnHand_list = []
        for i in p_salesAccount:
            for j in i['productLocations']:
                if j['warehouse']['id'] == 6:
                    if isinstance(j, dict):
                        qtyOnHand_list.append(j['qtyOnHand'])
        for i in range(len(data_id)):
            product, created = Products.objects.get_or_create(
                k_id=data_id[i],
                defaults={
                    'number': data_number[i],
                    'price': sellingPrice[i],
                    'p_quantity': qtyOnHand_list[i],
                    # ... other fields ...
                }
            )
            if not created:
                product.number = data_number[i]
                product.price = sellingPrice[i]
                product.p_quantity = qtyOnHand_list[i]
                product.save()
