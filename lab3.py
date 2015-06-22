# coding=utf-8
from BaseHTTPServer import HTTPServer
import json

from pysimplesoap.server import SoapDispatcher, SOAPHandler
from pymongo import MongoClient


def create(key, value):
    """
    Выполняет запрос Create к базе MongoDB используя PyMongo
    В базе будет создан новый объект {'key': key,'value': value}
    Создание происходит только в случае если объект с заданым key не присутствует в базе
    Аргументи:
        key - ключ объекта
        value - значение объекта
    """
    if db.count({'key': key}) == 0:
        db.insert({'key': key, 'value': value})
        return json.dumps({"isOk": True, "msg": "Object successfully created"})

    return json.dumps({"isOk": False, "msg": "Key already exists"})


def read(key):
    """
    Выполняет запрос Read к базе MongoDB используя PyMongo
    Аргументи:
        key - ключ объекта
    """
    if db.count({'key': key}) != 0:
        result = db.find_one({'key': key})
        result = {'key': result['key'], 'value': result['value']}
        return json.dumps({"isOk": True, "msg": result})

    return json.dumps({"isOk": False, "msg": "Key does not exists"})


def update(key, value):
    """
    Выполняет запрос Update к базе MongoDB используя PyMongo
    Модификация происходит только в случае если объект с заданым key присутствует в базе
    Аргументи:
        key - ключ объекта
        value - новое значение объекта
    """
    if db.count({'key': key}) != 0:
        db.update_one({'key': key}, {"$set": {'value': value}})
        return json.dumps({"isOk": True, "msg": "Object successfully updated"})

    return json.dumps({"isOk": False, "msg": "Key does not exists"})


def delete(key):
    """
    Выполняет запрос Delete к базе MongoDB используя PyMongo
    Аргументи:
        key - ключ объекта
    """
    if db.count({'key': key}) != 0:
        db.delete_one({'key': key})
        return json.dumps({"isOk": True, "msg": "Object successfully deleted"})

    return json.dumps({"isOk": False, "msg": "Key does not exists"})


dispatcher = SoapDispatcher('my_dispatcher')

dispatcher.register_function('Create', create, returns={'Result': str}, args={'key': str, 'value': str})
dispatcher.register_function('Read', read, returns={'Result': str}, args={'key': str})
dispatcher.register_function('Update', update, returns={'Result': str}, args={'key': str, 'value': str})
dispatcher.register_function('Delete', delete, returns={'Result': str}, args={'key': str})

# print "WSDL"
# print dispatcher.wsdl()
print "Connect to MongoDB..."
client = MongoClient()
db = client.test.table
print "Starting server... (localhost:8000)"
httpd = HTTPServer(("", 8000), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()