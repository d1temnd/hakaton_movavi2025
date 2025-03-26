import os

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN', '<token>')
    ADMINS = [int(i) for i in os.getenv('ADMINS_id', '[<first_id>, <second_id>]').strip('[]').split(',')]
    DB_NAME = './instance/data.db'