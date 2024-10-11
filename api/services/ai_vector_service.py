import json
import logging
from functools import lru_cache
from itertools import zip_longest

from sentence_transformers import SentenceTransformer
from tortoise.transactions import in_transaction

from models.receipt_action_model import ReceiptActionModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize the AI model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


class AiVectorService:
    """
    Service for generating vector data for AI usage.
    We transform transaction details and call arguments into text paragraphs and encode them into vectors.
    """

    def __init__(self):
        self.model = model  # Use the pre-initialized model

    def _format_json(self, data, level=0):
        if isinstance(data, dict):
            formatted_text = ""
            for key, value in data.items():
                # Indent sub-keys for nested objects
                indentation = '  ' * level
                formatted_text += f'{indentation}{key}:\n{self._format_json(value, level + 1)}\n\n'
            return formatted_text
        elif isinstance(data, list):
            # Handle lists (turn each item into a sub-paragraph)
            return '\n'.join([self._format_json(item, level + 1) for item in data])
        else:
            # For non-dict and non-list values, return them as plain text
            return '  ' * level + str(data)

    @lru_cache(maxsize=10000)
    def _preprocess_args(self, args: str):
        """
        Process JSON arguments and format them with key as title and value as text.
        If the value is JSON, format it as a sub-paragraph.
        """
        try:
            args_json = json.loads(args)
            return self._format_json(args_json)
        except (json.JSONDecodeError, TypeError):
            return args

    @lru_cache(maxsize=10000)
    def _preprocess_tx_data(self, action):
        """
        Preprocess tx data and associated fields (action_kind, social_kind, etc.) into a structured text format.
        """
        method_name = action.method_name if action.method_name else "Empty method"

        result = f'Call: {method_name}:\n'
        if action.social_kind:
            result += f'  Social action: {action.social_kind}\n'
        else:
            result += f'  Action: {action.action_kind}\n'

        result += f'  Sender: {action.predecessor_id}\n'
        result += f'  Receiver: {action.receiver_id}\n'

        if action.deposit > 0:
            result += f'  Deposit: {action.deposit}\n'
        if action.gas > 0:
            result += f'  Gas: {action.gas}\n'
        if action.stake > 0:
            result += f'  Stake: {action.stake}\n'

        return result

    async def generate_vectors_for_receipt_actions(self, batch_size: int = 1000):
        logger.info("Starting vectors generation batch...")

        while True:
            actions = await ReceiptActionModel.filter(tx_data_vector__isnull=True).limit(batch_size).all()

            if not actions:
                logger.info("No more receipt actions to process.")
                break

            args_texts = [self._preprocess_args(action.args) for action in actions if action.args and not action.args_vector]
            tx_data_texts = [self._preprocess_tx_data(action) for action in actions if not action.tx_data_vector]

            args_embeddings = self.model.encode(args_texts).tolist() if args_texts else []
            tx_data_embeddings = self.model.encode(tx_data_texts).tolist() if tx_data_texts else []

            async with in_transaction():
                for action, args_emb, tx_data_emb in zip_longest(actions, args_embeddings, tx_data_embeddings):
                    if action.args and not action.args_vector:
                        action.args_vector = args_emb
                    if not action.tx_data_vector:
                        action.tx_data_vector = tx_data_emb

                    await action.save()

            logger.info(f"Processed {len(actions)} receipt actions.")
