import os

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'token')
    ADMINS = [int(i) for i in os.getenv('ADMINS', '[123345678, 8654321]').strip('[]').split(',')]
    DB_NAME = './instance/data.db'
    JSON_DOCS = ''