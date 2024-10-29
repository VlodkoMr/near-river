import asyncio
import logging
from tortoise.expressions import Q

from config.settings import conf
from models.block_model import BlockModel
from models.event_progress import EventProgressModel
from models.transaction_model import TransactionModel
from services.database_service import DatabaseService

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class EventService:
    def __init__(self, check_interval: int):
        self.filter_sender = conf.EVENT_FILTER_SENDER
        self.filter_recipient = conf.EVENT_FILTER_RECIPIENT
        self.check_interval = check_interval  # in seconds

    async def listen_transactions(self):
        logger.info("Starting transaction event listener.")

        async with DatabaseService():
            event_progress = await EventProgressModel.first()
            last_block_height = event_progress.last_block_height if event_progress else await self.init_event_progress()
            print('last_block_height', last_block_height)


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

    async def start_listeners(self):
        await asyncio.gather(
            self.listen_transactions(),
        )
