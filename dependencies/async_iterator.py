class AsyncListIterator:
    def __init__(self, lst):
        self.lst = lst
        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index < len(self.lst):
            result = self.lst[self.index]
            self.index += 1
            return result
        else:
            raise StopAsyncIteration
