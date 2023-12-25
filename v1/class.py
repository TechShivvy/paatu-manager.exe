class B:
    def __init__(self):
        self.__list = [1, 2, 3]

    def function(self):
        self.__list[2] = 1


class A:
    def __init__(self):
        self.__arr = {}

    def add(self, key):
        self.__arr[key] = {"arr": B(), "hello": "world"}

    def getarr(self, key) -> dict[str, B]:
        return self.__arr.get(key, None)


x = A()
x.add(1)
print(x.getarr(1)["arr"]._B__list)
print(x.getarr(1)["hello"])
x.getarr(1)["arr"].function()
print(x.getarr(1)["arr"]._B__list)

if __name__ == "__main__":
    x = A()
    x.add(1)
    if (b := x.getarr(1)["arr"]) and isinstance(b, B):
        b.function()
y=B()
print(y._B__list)