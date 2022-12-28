import unittest

from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['test_database']


def insert_client(ip_address, mac_address, port):
    result = db.users.insert_one({'IpAddress': ip_address, 'MacAddress': mac_address, 'Port': port})
    return result.inserted_id


def get_client(client_id):
    client = db.users.find_one({'_id': client_id})
    return client


def update_client(client_id, ip_address, mac_address, port):
    result = db.users.update_one({'_id': client_id},
                           {'$set': {'IpAddress': ip_address, 'MacAddress': mac_address, 'Port': port}})

def delete_client(client_id):
    result = db.users.delete_one({'_id': client_id})

def count_documents():
    result = db.users.count_documents({})
    return result

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Clear collection before starting the test
        db.users.delete_many({})

    def test_insert_client(self):
        # Test that a client can be inserted into the database
        client_id = insert_client('192.168.2.100', 'FD:EW:DF:SD:ER:RT:FG:DF', '65432')
        self.assertIsInstance(client_id, ObjectId)

        client = get_client(client_id)
        self.assertEqual(client,
                         {'_id': client_id, 'IpAddress': '192.168.2.100', 'MacAddress': 'FD:EW:DF:SD:ER:RT:FG:DF',
                          'Port': '65432'})

    def test_get_client(self):
        # Test that a client can be retrieved from the database
        client_id = insert_client('192.168.2.100', 'FD:EA:DF:ED:ER:RT:FG:DF', '65431')

        client = get_client(client_id)
        self.assertEqual(client,
                         {'_id': client_id, 'IpAddress': '192.168.2.100', 'MacAddress': 'FD:EA:DF:ED:ER:RT:FG:DF',
                          'Port': '65431'})

    def test_update_client(self):
        client_id = insert_client('192.168.2.100', 'FD:EW:DF:SD:ER:RT:FG:DF', '65432')
        update_client(client_id, '192.168.2.100', 'FD:EA:DF:ED:ER:RT:FG:DF', '9999')
        # Read the updated document back from the collection
        doc = get_client(client_id)
        # Check that the document has the expected contents
        self.assertEqual(doc, {'IpAddress': '192.168.2.100', 'MacAddress': 'FD:EA:DF:ED:ER:RT:FG:DF', 'Port': '9999',
                               '_id': client_id})

    def test_delete(self):
        client_id = insert_client('192.168.2.100', 'FD:EW:DF:SD:ER:RT:FG:DF', '65432')
        # Delete the document
        delete_client(client_id)
        number_of_documents = count_documents()
        # Check that the document was deleted
        self.assertEqual(number_of_documents, 0)


if __name__ == '__main__':
    unittest.main()
