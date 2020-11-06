from tortoise.models import Model
from tortoise import fields


class Teacher(Model):
    class Meta:
        table = 'teachers'

    id = fields.IntField(pk=True)
    short_name = fields.CharField(max_length=100)
    full_name = fields.CharField(max_length=100, null=True)

    def __repr__(self):
        return f'<{self.short_name}>'
