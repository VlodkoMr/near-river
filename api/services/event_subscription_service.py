import asyncio
import logging

from tortoise.expressions import Q

from config.settings import conf
from models.receipt_action_model import ReceiptActionModel
from models.transaction_model import TransactionModel

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class EventSubscriptionService:
    def __init__(self, check_interval: int = 10):
        self.filter_sender = conf.EVENT_FILTER_SENDER
        self.filter_recipient = conf.EVENT_FILTER_RECIPIENT
        self.check_interval = check_interval  # in seconds

    async def listen_transactions(self):
        logger.info("Starting transaction event listener.")
        # TODO: Implement the transaction listener and call NEAR smart-contract

    async def start_listeners(self):
        await asyncio.gather(
            self.listen_transactions(),
        )
