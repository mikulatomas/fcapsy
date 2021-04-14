from typing import Type

from bitsets.bases import BitSet
from fcapsy.context import Context


class Concept:
    def __init__(self, extent: Type[BitSet], intent: Type[BitSet], name: str = None):
        self.extent = extent
        self.intent = intent
        self.name = name

    @classmethod
    def from_intent(cls, intent, context: Context, name: str = None):
        intent = context.Attributes(intent)
        extent = context.down(intent)
        return cls(extent, context.up(extent), name)

    @classmethod
    def from_extent(cls, extent, context: Context, name: str = None):
        extent = context.Objects(extent)
        intent = context.up(extent)
        return cls(context.down(intent), intent, name)

    @property
    def ratio(self):
        return self.extent.count() / self.intent.count() if self.intent.count() else 0

    def __repr__(self):
        if self.name:
            return "Concept({}, {}x{})".format(self.name, len(self.extent.members()), len(self.intent.members()))

        return "Concept({}x{})".format(len(self.extent.members()), len(self.intent.members()))

    def __str__(self):
        if self.name:
            return "Concept({}, {}, {})".format(self.name, str(self.extent.members()), str(self.intent.members()))

        return "Concept({}, {})".format(str(self.extent.members()), str(self.intent.members()))

    def __eq__(self, other):
        if isinstance(self, type(other)):
            return (self.extent == other.extent) and (self.intent == other.intent)

    def __hash__(self):
        return (hash(self.extent) ^ hash(self.intent)) ^ hash((self.extent, self.intent))
