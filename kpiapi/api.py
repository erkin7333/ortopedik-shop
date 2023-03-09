import requests
import json
from config.settings import ACCESS_TOKEN, X_TOKEN

code = {
    "warehouse_id": 6
}
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json;charset=UTF-8",
    "accessToken": ACCESS_TOKEN,
    "x-auth": X_TOKEN
}

response = requests.post("https://apps.kpi.com/services/api/v2/2/product_variants_zapier", json=code, headers=headers)
response_data = response.json()
print("SSSSSSSSSSSSSSSS=====================", len(response_data))
print("TTTTTTTTTTTTTTTTTTTTTTTTTTT==========", response_data)
if isinstance(response_data, list):
    data_product = [d['parent_number'] for d in response_data[:100]]
    print("RESPOSE===", data_product)
else:
    print("No products found.")
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
