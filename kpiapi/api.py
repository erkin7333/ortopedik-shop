import requests
import json
from config.settings import ACCESS_TOKEN, X_TOKEN

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer id_token'
}

response = requests.get('https://prodapi.shipox.com/api/v1/service_types', headers=headers)

print(response.status_code)
print(response.headers)
print(response.json())

# code = {
#     "filters": [
#         {
#             "filterCodeName": "warehouseId",
#             "items": [
#                 {
#                     "id": 6
#                 }
#             ]
#         }
#     ],
#     "limit": 60,
#     "start": 0
# }
#
# headers = {
#     "Content-Type": "application/json",
#     "Accept": "application/json;charset=UTF-8",
#     "accessToken": ACCESS_TOKEN,
#     "x-auth": X_TOKEN
# }
#
# response = requests.post("https://apps.kpi.com/services/api/v3/product/list", json=code, headers=headers)
# response_data = response.json()
# products = response_data.get('data', {}).get('items', [])
# print("SSSSSSSSSSSSSSSS=====================", len(products))
# if isinstance(products, list):
#     data_id = [d['id'] for d in products[:100]]
#     print("MAXSULOT idsi===", data_id)
#     data_number = [d['number'] for d in products[:100]]
#     print("MAXSULOT NUMBER===", data_number)
#     p_salesAccount = [d['inventoryStockInformation'] for d in products[:100]]
#     qtyOnHand_list = []
#     for i in p_salesAccount:
#         for j in i['productLocations']:
#             if j['warehouse']['id'] == 6:
#                 if isinstance(j, dict):  # check if j is a dictionary
#                     qtyOnHand_list.append(j['qtyOnHand'])
#     print(qtyOnHand_list)


# qty_on_hand = []
# for pro in p_salesAccount:
#     product_qtyOnHand = pro.get('productLocations', [])
#     data_quantity = [d['qtyOnHand'] for d in product_qtyOnHand[:100]]
#     product_warehouse = [f['warehouse'] for f in product_qtyOnHand[:10]]
#     deff = [s["id"] for s in product_warehouse[:10]]
#     print("YYYYYYYYYYYYYYYYY", deff)
#     print("FFFFFFFFFFFFFFFFFFFFFFFFFF=====", product_warehouse)
# print("SDFGHFSASDFG====", p_salesAccount)

# if product_warehouse.get("id") == 6:
#     print("TTTTTTTTTTTTTt", product_warehouse)
#     print("MAXSULOT SONI===", data_quantity)
#     for location in data_quantity:
#         if location.get('warehouse', {}).get('id') == 6:
#             qty_on_hand.append(location.get('qtyOnHand', 0))
#     print("ZAYBALEEEE======", qty_on_hand, type(qty_on_hand))
#     print("XULLAS SHUDA=====", product_qtyOnHand)


# data_id = [d['id'] for d in products[:100]]
# print("MAXSULOT idsi===", data_id)
# data_number = [d['number'] for d in products[:100]]
# print("MAXSULOT NUMBER===", data_number)

# elif isinstance(products, dict):
#     data_id = [d['id'] for d in products[:100]]
#     print("MAXSULOT idsi===", data_id)
#     data_number = [d['number'] for d in products[:100]]
#     print("MAXSULOT NUMBER===", data_number)
#     data_quantity = [d['qtyOnHand'] for d in products[:100]]
#     print("MAXSULOT SONI===", data_quantity)

# if isinstance(products, list):
#     data_id = [d['id'] for d in products[:100]]
#     print("MAXSULOT ID===", data_id)
#     print("MAXSULOT ID SONI===", len(data_id))
#     data_number = [d['number'] for d in products[:100]]
#     print("MAXSULOT SOTUV CODI=====", data_number)
#     print("MAXSULOT SOTUV CODI SONI====", len(data_number))
#     data_quantity = [q['quantity'] for q in products[:100]]
#     print("MAXSULOT SONI======", data_quantity)
# else:
#     print("Malumot yoq")

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
