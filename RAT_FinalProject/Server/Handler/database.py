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
    def delete(collection, uid):
        Database.COLLECTION = Database.DATABASE[collection]
        Database.COLLECTION.delete_one({'_id': uid})

    @staticmethod
    def find(collection, query):
        Database.COLLECTION = Database.DATABASE[collection]
        length = Database.COLLECTION.count_documents(query)
        return length, Database.COLLECTION.find(query)

    @staticmethod
    def update(filter, data):
        new_data = {"$set": data}
        Database.COLLECTION.update_one(filter, new_data)

    @staticmethod
    def get_all(collection):
        Database.COLLECTION = Database.DATABASE[collection]
        return Database.COLLECTION.find()

    @staticmethod
    def new_update_connection(collection, data):
        if data["_id"] != None:
            find_query_host_ip = {"_id": data["_id"]}
            length, documents = Database.find(collection, find_query_host_ip)
            if length > 0:
                Database.update(find_query_host_ip, data)
            else:
                Database.insert(collection, data)
        else:
            del data["_id"]
            Database.insert(collection, data)


#if __name__ == '__main__':
    #Database.initialize()
    #Database.insert("Clients_Collection", "sadaasd")

def create_enviroment_variables():
    os.environ["DATABASE_IP"] = "mongodb://localhost:27017"
    os.environ["DATABASLE_TABLE"] = "Clients"
