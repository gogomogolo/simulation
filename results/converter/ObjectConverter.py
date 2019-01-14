class ObjectConverter(object):
    def __init__(self, reader, conversion_logic):
        self.reader = reader
        self.conversion_logic = conversion_logic

    def convert(self):
        output = self.reader.read()
        return self.conversion_logic.convert(output)
