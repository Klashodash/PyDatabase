from flask import Flask, request, jsonify
import DBcm
import json
import re

app = Flask(__name__)
# Database details
DBconfig = {'host': '127.0.0.1',
            'user': 'gamesadmin',
            'password': 'gamesadminpasswd',
            'database': 'GamesDB'}


# "SHOW TABLES"
# Receives a list table request
# Returns a JSON object list of all the tables in the database
@app.route('/table/list', methods=['GET'])
def listTable():

    with DBcm.UseDatabase(DBconfig) as cursor:
        _SQL = "SHOW TABLES"
        cursor.execute(_SQL)
        itemList = []
        tableList = cursor.fetchall()

        for row in tableList:
            item = {"data": [{"name": "tableName", "value": row[0]}]}
            itemList.append(item)

        JSONDictionary = {"version": "1.0",
                          "href": request.base_url,
                          "Items": itemList
                          }
        return jsonify(collection=JSONDictionary)

# "SELECT * FROM tablename"
# Receives a table name
# Returns all of its entries along with their URLs
@app.route('/table/showall', methods=['GET'])
def selectAllFrom():

    tableName = None
    itemList = []
    jsonData = json.loads(request.get_data().decode("utf-8"))
    data = jsonData["collection"]["data"]
    for c in data:
        if c["name"] == "table_name":
            tableName = c["value"]

    if tableName:
        with DBcm.UseDatabase(DBconfig) as cursor:
            query = """SELECT * FROM %s""" % tableName
            cursor.execute(query)
            result = cursor.fetchall()

            for row in result:
                dataList = []
                i = 0

                for desc in cursor.description:
                    dataList.append({"name": desc[0], "value": row[i]})
                    i += 1
                item = {"href": request.url_root + "table/showone/" + str(row[0]), "data": dataList}
                itemList.append(item)

            JSONDictionary = {"version": "1.0",
                              "href": request.base_url,
                              "Items": itemList
                              }

        return jsonify(collection=JSONDictionary)


# "INSERT INTO tableName VALUES data"
# Writes entries to a table
# Returns a series of links
@app.route('/table/post', methods=['GET', 'POST'])
def insert():

    tableName = None
    jsonData = json.loads(request.get_data().decode("utf-8"))
    data = jsonData["collection"]["data"]

    # Here lieth the POST section, dealing with write requests
    if request.method == 'POST':
        fieldsString = ""
        valuesString = ""
        i = len(data)

        for c in data:
            if c["name"] == "table_name":
                tableName = c["value"]
                i -= 1
            elif i == 1:
                fieldsString += c["name"]
                valuesString += "\'" + re.escape(c["value"]) + "\'"
                i -= 1
            else:
                fieldsString += c["name"] + ", "
                valuesString += "\'" + re.escape(c["value"]) + "\', "
                i -= 1

        if tableName:
            with DBcm.UseDatabase(DBconfig) as cursor:
                query = ("INSERT INTO %s (%s) VALUES (%s);" % (tableName, fieldsString, valuesString))
                cursor.execute(query)

            JSONDictionary = {"version": "1.0",
                                  "href": request.base_url,
                                  "Items": [],
                                  "links": [{"name": request.url_root + "table/showall/", "methods": ["Get"]},
                                            {"name": request.url_root + "table/showone/<itemId>", "methods": ["Get"]}]
                                  }

            return jsonify(collection=JSONDictionary)

    # Here lieth the GET section, dealing with describing specific tables
    else:
        for c in data:
            if c["name"] == "table_name":
                tableName = c["value"]

        if tableName:
            with DBcm.UseDatabase(DBconfig) as cursor:
                query = """DESCRIBE %s""" % tableName
                cursor.execute(query)
                result = cursor.fetchall()
                dataList = []

                for row in result:
                    dataList.append({"name": row[0], "value": ""})

                JSONDictionary = {"version": "1.0",
                                  "href": request.base_url,
                                  "Items": [],
                                  "links": [{"name": request.url_root + "table/showall/", "methods": ["Get"]},
                                    {"name": request.url_root + "table/post/", "methods": ["Get", "Post"]}],
                                  "template": {"data": dataList}
                                  }

            return jsonify(collection=JSONDictionary)


# "SELECT * FROM " tableName "WHERE ID=idNum"
# Shows an individual entry from a table
# Returns a series of links, along with the entry
@app.route('/table/showone/<itemId>', methods=['GET'])
def selectOneFrom(itemId):

    tableName = None
    itemList = []
    idNumber = itemId
    jsonData = json.loads(request.get_data().decode("utf-8"))
    data = jsonData["collection"]["data"]

    for c in data:
        if c["name"] == "table_name":
            tableName = c["value"]

    if tableName:
        with DBcm.UseDatabase(DBconfig) as cursor:
            query = ("SELECT * FROM %s WHERE id=%s;" % (tableName, idNumber))
            cursor.execute(query)
            result = cursor.fetchall()

            for row in result:
                dataList = []
                i = 0

                for desc in cursor.description:
                    dataList.append({"name": desc[0], "value": row[i]})
                    i += 1

                item = {"href": request.url, "data": dataList}
                itemList.append(item)

        JSONDictionary = {"version": "1.0",
                          "Items": itemList,
                          "links": [{"name": request.url_root + "table/showall/", "methods": ["Get"]},
                                    {"name": request.url_root + "table/post/", "methods": ["Get", "Post"]}]
                          }

    return jsonify(collection=JSONDictionary)


if __name__ == '__main__':
    app.run()
