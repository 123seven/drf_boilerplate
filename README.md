# Local

    1. echo "from .base import *" > etc/settings/local.py
    2. add your configuration save to etc/settings/local.py
    
# Deployment

    1. add your configuration save to etc/settings/staging.py
    2. echo "DJANGO_SETTINGS_MODULE=etc.settings.staging" > .env
    3. docker-compose build 
    4. docker-compose up -d 

# Update
 
    1. sh update.sh