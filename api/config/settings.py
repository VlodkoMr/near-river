import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_CONNECTION = os.getenv("DB_CONNECTION")
    MODELS_LIST = ['models.block_model', 'models.receipt_action_model', 'models.transaction_model', 'models.event_progress', ]
    DEFAULT_PAGE_LIMIT = 100
    AI_SQL_MODEL_ID = "config/ai_models/llama-3-sqlcoder-8b"
    AI_SQL_MAX_TOKENS = 250
    AI_SQL_NUM_BEAMS = 1
    AI_SUMMARY_MODEL_ID = "config/ai_models/Llama-3.2-1B-Instruct"
    AI_SUMMARY_MAX_TOKENS = 400
    AI_SUMMARY_NUM_BEAMS = 1
    EVENT_BATCH_BLOCKS_COUNT = int(os.getenv("EVENT_BATCH_BLOCKS_COUNT"))
    EVENT_FILTER_SENDER = os.getenv("EVENT_FILTER_SENDER")
    EVENT_FILTER_RECIPIENT = os.getenv("EVENT_FILTER_RECIPIENT")
    EVENT_NOTIFICATION_TARGET = os.getenv("EVENT_NOTIFICATION_TARGET")
    EVENT_NEAR_ACCOUNT_ID = os.getenv("EVENT_NEAR_ACCOUNT_ID")
    EVENT_NEAR_ACCOUNT_PRIVATE_KEY = os.getenv("EVENT_NEAR_ACCOUNT_PRIVATE_KEY")


conf = Config()
