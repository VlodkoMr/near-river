import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_CONNECTION = os.getenv("DB_CONNECTION")
    ENABLE_EVENT_LISTENER = os.getenv("ENABLE_EVENT_LISTENER") == "true"
    MODELS_LIST = ['models.block_model', 'models.receipt_action_model', 'models.transaction_model', ]
    DEFAULT_PAGE_LIMIT = 100
    AI_MODEL_ID = "config/ai_models/Llama-3.2-3B-Instruct"
    AI_SQL_MAX_TOKENS = 300
    AI_SQL_NUM_BEAMS = 2
    AI_SUMMARY_MAX_TOKENS = 400
    AI_SUMMARY_NUM_BEAMS = 1


conf = Config()
