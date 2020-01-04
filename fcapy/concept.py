class Concept:
    def __init__(self, extent, intent):
        self._extent = extent
        self._intent = intent

    def __repr__(self):
        return "Concept({}, {})".format(repr(self._extent), repr(self._intent))

    def __eq__(self, other):
        if isinstance(self, type(other)):
            return (self._extent == other._extent) and (self._intent == other._intent)

    def __hash__(self):
        return (hash(self._extent) ^ hash(self._intent)) ^ hash((self._extent, self._intent))

    def get_id(self):
        return int(self._intent)

    @property
    def extent(self):
        return self._extent

    @property
    def intent(self):
        return self._intent
