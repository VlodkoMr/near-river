from tortoise import fields
from tortoise.models import Model

class TransactionModel(Model):
    block_height = fields.ForeignKeyField(
        'models.BlockModel',
        related_name='transactions',
        source_field='block_height',
        on_delete=fields.CASCADE
    )
    block_timestamp = fields.DatetimeField()
    tx_hash = fields.TextField(pk=True)
    signer_id = fields.CharField(max_length=64, null=True)
    nonce = fields.BigIntField(null=True)
    receipt_id = fields.TextField(null=True)
    receiver_id = fields.CharField(max_length=64, null=True)

    class Meta:
        table = "transactions"
        indexes = [
            ["block_timestamp"],   # Index on block_timestamp
            ["signer_id"],         # Index on signer_id
            ["receiver_id"]        # Index on receiver_id
        ]