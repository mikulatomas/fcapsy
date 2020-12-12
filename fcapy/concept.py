from bitsets.bases import BitSet
from typing import Type
from fcapy.context import Context


class Concept:
    def __init__(self, extent: Type[BitSet], intent: Type[BitSet]):
        self._extent = extent
        self._intent = intent

    @classmethod
    def from_intent(cls, intent: Type[BitSet], context: Context):
        extent = context.down(intent)
        return cls(extent, context.up(extent))

    @classmethod
    def from_extent(cls, extent: Type[BitSet], context: Context):
        intent = context.up(extent)
        return cls(context.down(intent), intent)

    @classmethod
    def from_intent_members(cls, intent: list, context: Context):
        intent = context._Attributes.frommembers(intent)
        return Concept.from_intent(intent, context)

    @classmethod
    def from_extent_members(cls, extent: list, context: Context):
        extent = context._Objects.frommembers(extent)
        return Concept.from_extent(extent, context)

    def __repr__(self):
        return "Concept({}x{})".format(len(self._extent.members()), len(self._intent.members()))

    def __str__(self):
        return "Concept({}, {})".format(str(self._extent.members()), str(self._intent.members()))

    def __eq__(self, other):
        if isinstance(self, type(other)):
            return (self._extent == other._extent) and (self._intent == other._intent)

    def __hash__(self):
        return (hash(self._extent) ^ hash(self._intent)) ^ hash((self._extent, self._intent))

    @ property
    def extent(self):
        return self._extent

    @ property
    def intent(self):
        return self._intent
