import requests
import json

#r = requests.get("http://127.0.0.1:5000/table/list")
#
# data = {
#     "collection": {
#             "data": [
#                 {"name": "table_name", "value": "players"}
#             ]
#         }
# }
# JSONData = json.dumps(data)
# r = requests.get("http://127.0.0.1:5000/table/showall", data=JSONData)
#
# print(r.content)


# data = {
#    "collection": {
#            "data": [
#               {"name": "table_name", "value": "games"},
#                {"name": "id_number", "value": 3}
#            ]
#        }
# }
#
# JSONData = json.dumps(data)
#
# r = requests.get("http://127.0.0.1:5000/table/showone/2", data=JSONData)
#
# print(r.content)


data = {
     "collection":  {
         "data":  [
             {"name": "table_name", "value": "games"},
             {"name": "name", "value": "Game's game"},
             {"name": "description", "value": "Loadsa stuff"},
        ]
    }
}

# data = {
#     "collection": {
#         "data": [
#             {"name": "table_name", "value": "players"},
#             {"name": "handle", "value": "Leeroy Jenkins"},
#             {"name": "first", "value": "Ben"},
#             {"name": "last", "value": "Schultz"},
#             {"name": "email", "value": "atleastihave@chicken.com"},
#             {"name": "passwd", "value": "raid"}
#         ]
#     }
# }
#
JSONData = json.dumps(data)
#r = requests.post("http://127.0.0.1:5000/table/post", data=JSONData)
r = requests.get("http://127.0.0.1:5000/table/post", data=JSONData)
#
print(r.content)