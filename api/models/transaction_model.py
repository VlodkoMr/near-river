from tortoise import fields
from tortoise.models import Model


class TransactionModel(Model):
    block_height = fields.BigIntField()
    block_timestamp = fields.DatetimeField()
    tx_hash = fields.TextField(pk=True)
    signer_id = fields.CharField(max_length=64, null=True)
    nonce = fields.BigIntField(null=True)
    receipt_id = fields.TextField(null=True)
    receiver_id = fields.CharField(max_length=64, null=True)

    class Meta:
        table = "transactions"
        indexes = [
            ["block_timestamp"],
            ["signer_id"],
            ["receiver_id"]
        ]

    def __str__(self):
        return self.tx_hash

    def serialize(self):
        return {
            "tx_hash": self.tx_hash,
            "block_height": self.block_height,
            "block_timestamp": int(self.block_timestamp.timestamp()),
            "signer_id": self.signer_id,
            "nonce": self.nonce,
            "receipt_id": self.receipt_id,
            "receiver_id": self.receiver_id
        }
