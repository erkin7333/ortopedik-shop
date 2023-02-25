import requests
import json
from main.views import Product




products = Product.objects.all()

# Retrieve sales code from the database and API
for product in products:
    db_sales_code = product.vendor_code
    print("DDDDDDDDDDDD", db_sales_code)
    code = {
        "limit": 10,
        "start": 0
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;charset=UTF-8",
        "accessToken": "2A390F47-F3A7-4E59-9227-8BA6D41E0262",
        "x-auth": "PAID$92792$CE708F467B82D26F"
    }

    response = requests.post("https://apps.kpi.com/services/api/v2/2/products_zapier", json=code, headers=headers)
    api_sales_code = requests.get(response).json()['number']

    # Compare sales codes and display if they are the same
    if db_sales_code == api_sales_code:
        print(f"{product.name}: {db_sales_code} (same as API)")
    else:
        print(f"{product.name}: {db_sales_code} (different from API: {api_sales_code})")























# response_data = response.json()
# print("SSSSSSSSSSSSSSSS", response_data)
# if isinstance(response_data, list):
#     data_product = [d['number'] for d in response_data[:10]]
#     print("RESPOSE===", data_product)
# elif isinstance(response_data, dict):
#     data_product = response_data.get("number")
#     print("RESPOSE===", data_product)

# sales_codes = {}
# if response.ok:
#     products = response.json()
#     print("MAXSULOTLAR========", products)
#     for product in products:
#         sales_codes[product['id']] = product['sales_codes']
#         print("KODE", sales_codes)


# response = requests.get("https://apps.kpi.com/services/api/v2/2/products_zapier")
# if response.status_code == 200:
#     products = response.json()
#     print("DDDDDDDDDDDDDDDDDDDD")
# else:
#     print("FFFFFFFFFFFff", None)