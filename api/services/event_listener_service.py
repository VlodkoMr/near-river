import asyncio
import logging

from tortoise.expressions import Q

from models.receipt_action_model import ReceiptActionModel
from models.transaction_model import TransactionModel

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class EventListener:
    def __init__(self, smart_contracts: set, methods: set, check_interval: int = 10):
        self.smart_contracts = smart_contracts
        self.methods = methods
        self.check_interval = check_interval  # in seconds

    async def listen_transactions(self):
        logger.info("Starting transaction event listener.")
        processed_hashes = set()

        while True:
            transactions = await TransactionModel.filter(
                receiver_id__in=self.smart_contracts,
                tx_hash__not_in=processed_hashes
            ).all()

            for tx in transactions:
                logger.info(f"Detected transaction {tx.tx_hash} to smart contract {tx.receiver_id}")
                # Implement your action here (e.g., send notification, trigger workflow)
                # Example:
                # await self.notify(tx)
                processed_hashes.add(tx.tx_hash)

            await asyncio.sleep(self.check_interval)

    async def listen_receipt_actions(self):
        logger.info("Starting receipt action event listener.")
        processed_ids = set()

        while True:
            actions = await ReceiptActionModel.filter(
                Q(receiver_id__in=self.smart_contracts),
                Q(method_name__in=self.methods),
                Q(id__not_in=processed_ids)
            ).all()

            for action in actions:
                logger.info(f"Detected receipt action {action.id} with method {action.method_name}")
                # Implement your action here
                # Example:
                # await self.trigger_action(action)
                processed_ids.add(action.id)

            await asyncio.sleep(self.check_interval)

    async def start_listeners(self):
        await asyncio.gather(
            self.listen_transactions(),
            self.listen_receipt_actions()
        )
