import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv('/api/.env')

db = MongoClient(host=os.getenv('mongodb_host'),
                 port=int(os.getenv('mongodb_port')),
                 username=os.getenv('mongodb_root_username'),
                 password=os.getenv('mongodb_root_password'))[os.getenv('mongodb_db_name')]
