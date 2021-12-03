import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv('.env')

print(os.getenv('mongodb_host'), int(os.getenv('mongodb_port')))

db = MongoClient(os.getenv('mongodb_host'),
                 port=int(os.getenv('mongodb_port')),
                 username=os.getenv('mongodb_username'),
                 password=os.getenv('mongodb_password'))[os.getenv('mongodb_name')]
