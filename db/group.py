from tortoise.models import Model
from tortoise import fields


class Group(Model):
    class Meta:
        table = 'groups'

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100, unique=True)

    def __repr__(self):
        return f'<{self.title}>'
