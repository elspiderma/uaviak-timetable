from tortoise.models import Model

from utils.string import approximate_match


class SearchABC(Model):
    class Meta:
        abstract = True

    IGNORE_CHAR = []

    @property
    def _search_field(self):
        raise NotImplemented

    @classmethod
    async def approximate_search(cls, query: str):
        all_objs = await cls.all()
        found_objs = []

        for obj in all_objs:
            if approximate_match(obj._search_field, query, obj.IGNORE_CHAR):
                found_objs.append(obj)

        return found_objs
