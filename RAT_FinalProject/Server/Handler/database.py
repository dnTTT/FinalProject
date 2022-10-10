from pymongo import MongoClient
import os

client = MongoClient()


class Database(object):
    URI = "mongodb://localhost:27017"
    DATABASE = None
    COLLECTION = None

    @staticmethod
    def initialize():
        client = MongoClient(Database.URI)
        Database.DATABASE = client.Clients
        #Database.COLLECTION = Database.DATABASE["Clients_Collection"]

    @staticmethod
    def insert(collection, data):
        Database.COLLECTION = Database.DATABASE[collection]
        Database.COLLECTION.insert_one(data)

    @staticmethod
    def find(collection, query):
        Database.COLLECTION = Database.DATABASE[collection]
        return Database.COLLECTION.find(query)

    @staticmethod
    def new_connection(collection, data):
        find_query_host_ip = {"Hostname": data["Hostname"], "Ip_address": data["Ip_address"]}
        document = Database.find(collection, find_query_host_ip)


        #Database.insert(collection, data)
        for x in document:
            print(x)


#if __name__ == '__main__':
    #Database.initialize()
    #Database.insert("Clients_Collection", "sadaasd")

def create_enviroment_variables():
    os.environ["DATABASE_IP"] = "mongodb://localhost:27017"
    os.environ["DATABASLE_TABLE"] = "Clients"
