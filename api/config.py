import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_CONNECTION = os.getenv("DB_CONNECTION")
    ENABLE_AI_PROCESSING = os.getenv("ENABLE_AI_PROCESSING") == "true"
    ENABLE_EVENT_LISTENER = os.getenv("ENABLE_EVENT_LISTENER") == "true"
    MODELS_LIST = [
        'models.block_model',
        'models.receipt_action_model',
        'models.transaction_model',
    ]
    PAGE_LIMIT = 100


conf = Config()
