import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_CONNECTION = os.getenv("DB_CONNECTION")
    MODELS_LIST = ['models.block_model', 'models.receipt_action_model', 'models.transaction_model', 'models.event_progress', ]
    DEFAULT_PAGE_LIMIT = 100
    AI_MODEL_ID = "config/ai_models/Llama-3.2-3B-Instruct"
    AI_SQL_MAX_TOKENS = 300
    AI_SQL_NUM_BEAMS = 2
    AI_SUMMARY_MAX_TOKENS = 400
    AI_SUMMARY_NUM_BEAMS = 1
    ENABLE_EVENT_LISTENER = os.getenv("ENABLE_EVENT_LISTENER") == "true"
    EVENT_FILTER_SENDER = os.getenv("EVENT_FILTER_SENDER")
    EVENT_FILTER_RECIPIENT = os.getenv("EVENT_FILTER_RECIPIENT")
    EVENT_NOTIFICATION_TARGET = os.getenv("EVENT_NOTIFICATION_TARGET")
    EVENT_NOTIFICATION_ACCOUNT = os.getenv("EVENT_NOTIFICATION_ACCOUNT")


conf = Config()
