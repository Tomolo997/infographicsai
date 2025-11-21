import os
from dotenv import load_dotenv

# Load the .env file if it exists
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)

# Determine the environment
environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
else:
    from .development import *