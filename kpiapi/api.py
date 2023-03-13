import requests
import json
from config.settings import ACCESS_TOKEN, X_TOKEN


headers = {
    "Content-Type": "application/json",
    "Accept": "application/json;charset=UTF-8",
    "accessToken": ACCESS_TOKEN,
    "x-auth": X_TOKEN
}

response = requests.post("https://apps.kpi.com/services/api/v2/2/product_variants_zapier?warehouse_id=6",
                         headers=headers)
response_data = response.json()
print("SSSSSSSSSSSSSSSS=====================", len(response_data))
print("SSSSSSSSSSSSSSSS=====================", response_data)
if isinstance(response_data, list):
    data_id = [d['id'] for d in response_data[:102]]
    print("MAXSULOT ID===", data_id)
    print("MAXSULOT ID SONI===", len(data_id))
    data_number = [d['sku_number'] for d in response_data[:102]]
    print("MAXSULOT SOTUV CODI=====", data_number)
    print("MAXSULOT SOTUV CODI SONI====", len(data_number))
    data_quantity = [q['quantity'] for q in response_data[:102]]
    print("MAXSULOT SONI======", data_quantity)
else:
    print("Malumot yoq")

# import requests
#
# code = {
#     "limit": 1000,
#     "start": 0
# }
# headers = {
#     "Content-Type": "application/json",
#     "Accept": "application/json;charset=UTF-8",
#     "accessToken": ACCESS_TOKEN,
#     "x-auth": X_TOKEN
# }
#
# response = requests.post("https://apps.kpi.com/services/api/v2/2/products", json=code, headers=headers)
# response_data = response.json()
# print("BIRINCHI QADAM======", response_data)
#
# products = response_data.get('data', {}).get('list', [])
# print("PRODUCT LIST======", products)
# filtered_products = []
#
# for product in products:
#     for stock_item in product.get('inventory_stock_item_list', []):
#         print("KKKKKKKKKKK=======", stock_item)
#         if stock_item.get('warehouse', {}).get('warehouse_id') == 6:
#             filtered_products.append(product)
#             break
# if isinstance(filtered_products, list):
#     data_product = [d['number'] for d in filtered_products[:324]]
#     print("MAXSULOT SOTUV CODI===", data_product)
#
# print("FILTER QILINGAN MAXSULOTLAR=======", len(filtered_products))


# code = {
#     "limit": 150,
#     "start": 0
# }
# headers = {
#     "Content-Type": "application/json",
#     "Accept": "application/json;charset=UTF-8",
#     "accessToken": ACCESS_TOKEN,
#     "x-auth": X_TOKEN
# }
#
# response = requests.post("https://apps.kpi.com/services/api/v2/2/products", json=code, headers=headers)
# response_data = response.json()
# print("BIRINCHI QADAM======", response_data)
# products = json.loads(response_data)
# filtered_products = []
#
# for product in products:
#     for stoct_item in product['inventory_stock_item_list']:
#         if stoct_item['warehouse']['warehouse_id'] == 6:
#             filtered_products.append(product)
#             break
# print("FILTER QILINGAN MAXSULOTLAR=======", filtered_products)


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


#
# data_product = [d['parent_id'] for d in response_data[:102]]
#   print("MAXSULOT KATEGORIYA ID===", data_product)
#   print("MAXSULOT KATEGORIYA SONI===", len(data_product))
#   data_number = [d['parent_number'] for d in response_data[:102]]
#   print("MAXSULOT KATEGORIYA SOTUV CODI===", data_number)
#   print("MAXSULOT KATEGORIYA SOTUV CODI SONI===", len(data_number))
