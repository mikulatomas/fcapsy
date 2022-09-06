import typing
import concepts

from .utils import get_vectors


class Category:
    """Category defined as group of exemplars (extent)."""

    def __init__(self, context: "concepts.Context", extent) -> None:
        self.context = context
        self._extent = extent

    @property
    def extent(self) -> typing.Tuple[str, ...]:
        return self._extent.members()

    def vectors(self, item: str) -> typing.Dict:
        return get_vectors(self, item)
