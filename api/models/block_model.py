from tortoise import fields
from tortoise.models import Model

class BlockModel(Model):
    block_height = fields.BigIntField(pk=True)
    block_timestamp = fields.DatetimeField()
    block_hash = fields.TextField()
    author_account_id = fields.CharField(max_length=64)
    approvals = fields.BigIntField(null=True)

    class Meta:
        table = "blocks"
        indexes = [["block_timestamp"]]