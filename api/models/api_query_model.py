from tortoise import fields
from tortoise.models import Model

class APIQueryModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    query_type = fields.CharField(max_length=20)  # 'sql' or 'analytics'
    query_text = fields.TextField()

    class Meta:
        table = "api_queries"