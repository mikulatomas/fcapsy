class Context:
    def __init__(self, matrix, Objects, Attributes):
        self.rows = tuple(map(Attributes.frombools, matrix))
        self.columns = tuple(map(Objects.frombools, zip(*matrix)))

        self._Objects = Objects
        self._Attributes = Attributes

    def up(self, objects):
        return self.__arrow_operator(objects, self.rows, self._Attributes)

    def down(self, attributes):
        return self.__arrow_operator(attributes, self.columns, self._Objects)

    def __arrow_operator(self, input_set, data, ResultClass):
        result = ResultClass.supremum

        for row in data:
            if input_set & 1:
                result &= row
            input_set >>= 1

            if not input_set:
                break

        return result