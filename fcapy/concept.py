from bitsets.bases import BitSet
from typing import Type
from fcapy.context import Context


class Concept:
    def __init__(self, extent: Type[BitSet], intent: Type[BitSet]):
        self._extent = extent
        self._intent = intent

    @classmethod
    def from_intent(cls, intent: Type[BitSet], context: Context):
        return cls(context.down(intent), intent)

    @classmethod
    def from_extent(cls, extent: Type[BitSet], context: Context):
        return cls(extent, context.down(extent))

    @classmethod
    def from_intent_members(cls, intent: list, context: Context):
        intent = context._Attributes.frommembers(intent)
        return cls(context.down(intent), intent)

    @classmethod
    def from_extent_members(cls, extent: list, context: Context):
        extent = context._Objects.frommembers(extent)
        return cls(extent, context.up(extent))

    def __repr__(self):
        return "Concept({}, {})".format(repr(self._extent), repr(self._intent))

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
