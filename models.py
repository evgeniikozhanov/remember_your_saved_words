from tortoise.models import Model
from tortoise import fields


class SavedWord(Model):
    id = fields.IntField(pk=True)
    words_group_name = fields.TextField()
    cdate = fields.DateField()
    from_language = fields.TextField()
    to_language = fields.TextField()
    from_word = fields.TextField()
    to_word = fields.TextField()
