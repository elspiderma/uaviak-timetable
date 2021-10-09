from dataclasses import dataclass


@dataclass
class ObjectWithTitleAndId:
    id: int

    @property
    def title(self) -> str:
        """Заголовок объекта.

        Returns:
            Заголовок.
        """
        raise NotImplemented
