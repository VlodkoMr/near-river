import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_CONNECTION = os.getenv("DB_CONNECTION")
    ENABLE_EVENT_LISTENER = os.getenv("ENABLE_EVENT_LISTENER") == "true"
    MODELS_LIST = ['models.block_model', 'models.receipt_action_model', 'models.transaction_model', ]
    DEFAULT_PAGE_LIMIT = 100
    AI_SQL_MODEL_ID = "config/ai_models/sqlcoder-7b-2"
    AI_SQL_MODEL_MAX_TOKENS = 256
    AI_SQL_MODEL_NUM_BEAMS = 1
    AI_SUMMARY_MODEL_ID = "config/ai_models/Llama-3.2-1B-Instruct"
    AI_SUMMARY_MODEL_MAX_TOKENS = 256


conf = Config()
