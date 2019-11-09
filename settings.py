from dotenv import load_dotenv
import os

API_KEY = os.getenv('API_KEY')


"""try:
    API_KEY = os.getenv('API_KEY')
except environ.compat.ImproperlyConfigured:
    API_KEY = os.environ.get('API_KEY')"""
