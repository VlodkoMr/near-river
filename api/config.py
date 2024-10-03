import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_CONNECTION = os.getenv("DB_CONNECTION")
    MODELS_LIST = [
        'models.api_query_model',
        'models.block_model',
        'models.receipt_action_model',
        'models.transaction_model',
    ]

conf = Config()
