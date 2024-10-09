from tortoise import fields
from tortoise.models import Model


class ReceiptActionModel(Model):
    id = fields.TextField(pk=True)
    block_height = fields.BigIntField()
    block_timestamp = fields.DatetimeField()
    receipt_id = fields.TextField()
    predecessor_id = fields.CharField(max_length=64)
    receiver_id = fields.CharField(max_length=64)
    action_kind = fields.CharField(max_length=20)
    action_index = fields.BigIntField()
    method_name = fields.CharField(max_length=255)
    args = fields.TextField(null=True)
    social_kind = fields.CharField(max_length=20, null=True)
    gas = fields.IntField()
    deposit = fields.FloatField()
    stake = fields.FloatField()
    status = fields.CharField(max_length=20)
    args_vector = fields.JSONField(null=True)
    tx_data_vector = fields.JSONField(null=True)

    class Meta:
        table = "receipt_actions"
        indexes = [
            ["block_timestamp"],
            ["predecessor_id"],
            ["receiver_id"],
            ["method_name"]
        ]
