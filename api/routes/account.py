from typing import Optional
from fastapi import APIRouter, HTTPException

from config import conf
from helpers.decorators import exception_handler
from services.db_service import DatabaseService

router = APIRouter()


@router.get("/near-token-sent/{signer_id}")
@exception_handler
async def get_near_token_sent(
        signer_id: str,
        limit: Optional[int] = conf.PAGE_LIMIT,
        offset: Optional[int] = 0
):
    """ Get NEAR token transfers sent by the signer with pagination """
    total_records_query = """
    SELECT COUNT(*) 
    FROM receipt_actions 
    WHERE predecessor_id = $1 AND deposit > 0 AND status != 'Failure'
    """

    paginated_query = """
    SELECT * 
    FROM receipt_actions 
    WHERE predecessor_id = $1 AND deposit > 0 AND status != 'Failure'
    ORDER BY block_timestamp DESC
    LIMIT $2 OFFSET $3
    """

    async with DatabaseService() as db:
        # Get total records count
        total_records = await db.run_raw_sql(total_records_query, [signer_id])

        # Get paginated result
        paginated_result = await db.run_raw_sql(paginated_query, [signer_id, limit, offset])

        return {
            "total": total_records[0]["count"],
            "result": paginated_result
        }


@router.get("/near-token-received/{receiver_id}")
@exception_handler
async def get_near_token_received(
        receiver_id: str,
        limit: Optional[int] = conf.PAGE_LIMIT,
        offset: Optional[int] = 0
):
    """ Get NEAR token transfers received by the account with pagination """
    total_records_query = """
    SELECT COUNT(*) 
    FROM receipt_actions 
    WHERE receiver_id = $1 AND deposit > 0 AND status != 'Failure'
    """

    paginated_query = """
    SELECT * 
    FROM receipt_actions 
    WHERE receiver_id = $1 AND deposit > 0 AND status != 'Failure'
    ORDER BY block_timestamp DESC
    LIMIT $2 OFFSET $3
    """

    async with DatabaseService() as db:
        # Get total records count
        total_records = await db.run_raw_sql(total_records_query, [receiver_id])

        # Get paginated result
        paginated_result = await db.run_raw_sql(paginated_query, [receiver_id, limit, offset])

        return {
            "total": total_records[0]["count"],
            "result": paginated_result
        }


@router.get("/ft-token-sent/{signer_id}")
@exception_handler
async def get_ft_transfers_sent(
        signer_id: str,
        limit: Optional[int] = conf.PAGE_LIMIT,
        offset: Optional[int] = 0
):
    """ Get fungible token transfers sent by the signer with pagination """
    total_records_query = """
    SELECT COUNT(*) 
    FROM receipt_actions 
    WHERE predecessor_id = $1 AND method_name = 'ft_transfer' AND status != 'Failure'
    """

    paginated_query = """
    SELECT * 
    FROM receipt_actions 
    WHERE predecessor_id = $1 AND method_name = 'ft_transfer' AND status != 'Failure'
    ORDER BY block_timestamp DESC
    LIMIT $2 OFFSET $3
    """

    async with DatabaseService() as db:
        # Get total records count
        total_records = await db.run_raw_sql(total_records_query, [signer_id])

        # Get paginated result
        paginated_result = await db.run_raw_sql(paginated_query, [signer_id, limit, offset])

        return {
            "total": total_records[0]["count"],
            "result": paginated_result
        }


@router.get("/ft-token-received/{receiver_id}")
@exception_handler
async def get_ft_transfers_received(
        receiver_id: str,
        limit: Optional[int] = conf.PAGE_LIMIT,
        offset: Optional[int] = 0
):
    """ Get fungible token transfers received by the account with pagination """
    total_records_query = """
    SELECT COUNT(*) 
    FROM receipt_actions 
    WHERE receiver_id = $1 AND method_name = 'ft_transfer' AND status != 'Failure'
    """

    paginated_query = """
    SELECT * 
    FROM receipt_actions 
    WHERE receiver_id = $1 AND method_name = 'ft_transfer' AND status != 'Failure'
    ORDER BY block_timestamp DESC
    LIMIT $2 OFFSET $3
    """

    async with DatabaseService() as db:
        # Get total records count
        total_records = await db.run_raw_sql(total_records_query, [receiver_id])

        # Get paginated result
        paginated_result = await db.run_raw_sql(paginated_query, [receiver_id, limit, offset])

        return {
            "total": total_records[0]["count"],
            "result": paginated_result
        }


@router.get("/daily-tx-sent/{signer_id}")
@exception_handler
async def get_daily_tx_sent(signer_id: str):
    """ Get daily transaction count sent by the signer """
    query = """
    SELECT DATE(block_timestamp) as date, COUNT(receipt_id) as daily_count, SUM(deposit) as near_deposit
    FROM receipt_actions
    WHERE predecessor_id = $1 AND status != 'Failure'
    GROUP BY date 
    ORDER BY date
    """
    async with DatabaseService() as db:
        result = await db.run_raw_sql(query, [signer_id])
        return result


@router.get("/daily-tx-received/{receiver_id}")
@exception_handler
async def get_daily_tx_received(receiver_id: str):
    """ Get daily transaction count sent by the signer """
    query = """
    SELECT DATE(block_timestamp) as date, COUNT(receipt_id) as daily_count, SUM(deposit) as near_deposit
    FROM receipt_actions
    WHERE receiver_id = $1 AND status != 'Failure'
    GROUP BY date 
    ORDER BY date
    """
    async with DatabaseService() as db:
        result = await db.run_raw_sql(query, [receiver_id])
        return result
