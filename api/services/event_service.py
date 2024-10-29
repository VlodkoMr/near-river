import httpx
import asyncio
import logging

from pynear.account import Account
from config.settings import conf
from models.block_model import BlockModel
from models.event_progress import EventProgressModel
from models.transaction_model import TransactionModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EventService:
    def __init__(self, check_interval: int):
        self.filter_sender = conf.EVENT_FILTER_SENDER
        self.filter_recipient = conf.EVENT_FILTER_RECIPIENT
        self.event_batch_blocks_count = conf.EVENT_BATCH_BLOCKS_COUNT
        self.notification_target = conf.EVENT_NOTIFICATION_TARGET
        self.check_interval = check_interval  # in seconds

    async def start_listeners(self):
        await asyncio.gather(
            self.listen_transactions(),
        )

    async def init_event_progress(self):
        first_block = await BlockModel.all().order_by('block_height').first()
        if not first_block:
            logger.error("No blocks in the database.")
            return

        init_block_height = first_block.block_height
        await EventProgressModel.create(
            init_block_height=init_block_height,
            last_block_height=init_block_height,
        )
        return init_block_height

    async def listen_transactions(self):
        logger.info("Starting event listener.")

        event_progress = await EventProgressModel.first()
        start_block_height = event_progress.last_block_height if event_progress else await self.init_event_progress()
        end_block_height = start_block_height + self.event_batch_blocks_count

        for block_height in range(start_block_height, end_block_height+1):
            transactions_query = TransactionModel.filter(block_height=block_height)

            if self.filter_sender:
                transactions_query = transactions_query.filter(signer_id=self.filter_sender)
            if self.filter_recipient:
                transactions_query = transactions_query.filter(receiver_id=self.filter_recipient)

            transactions = await transactions_query.all()
            for transaction in transactions:
                await self.handle_notification(transaction)

        await EventProgressModel.update(
            last_block_height=end_block_height
        ).where(id == event_progress.id)

    # This method is called for each transaction that matches the filters
    async def handle_notification(self, transaction):
        if self.notification_target.startswith("http"):
            await self._send_http_notification(self.notification_target, dict(transaction))
        elif self.notification_target and "|" in self.notification_target:
            contract_address, contract_method = self.notification_target.split("|", 1)
            await self._call_near_smart_contract(contract_address, contract_method, dict(transaction))
        else:
            logger.error("No event notification target specified.")

    async def _send_http_notification(self, url: str, data: dict):
        """Send transaction data to an HTTP endpoint."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data)
                if response.status_code == 200:
                    logger.info(f"Successfully sent transaction data to {url}")
                else:
                    logger.error(f"Failed to send data to {url}: {response.status_code} - {response.text}")
            except httpx.RequestError as e:
                logger.error(f"HTTP request failed: {e}")

    async def _call_near_smart_contract(self, address: str, method: str, tx_data: dict):
        """Call a NEAR smart contract method with provided arguments."""
        try:
            near_account = Account(conf.EVENT_NEAR_ACCOUNT_ID, conf.EVENT_NEAR_ACCOUNT_PRIVATE_KEY)
        except Exception as e:
            logger.error(f"Failed to load NEAR account: {e}")
            return

        try:
            result = await near_account.call_function(address, method, {"data": tx_data})
            logger.info(f"Successfully called smart contract method with result: {result}")
        except Exception as e:
            logger.error(f"Smart contract call failed: {e}")