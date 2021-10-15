import uuid


class SymbolTable:
    def __init__(self):
        self.hashTable = {}

    def __add__(self, other) -> uuid.UUID:
        itemId = uuid.uuid4()

        self.hashTable[itemId] = other

        return itemId

    def __getitem__(self, item: uuid.UUID):
        return self.hashTable[item]


st = SymbolTable()
myKey = st + "myValue"
print(st[myKey])


class Node:
    def __init__(self, value):
        self.item = value
        self.root = None
        self.left = None
        self.right = None


def insert(root, value):
    if root is None:
        return Node(value)
    else:
        if str(root.item) == str(value):
            return root
        elif str(root.item) < str(value):
            root.right = insert(root.right, value)
        else:
            root.left = insert(root.left, value)
    return root


def search(root: Node, value):
    if root.item == value:
        return root

    if root.item > value:
        if root.left is None:
            return None

        return search(root.left, value)

    if root.right is None:
        return None

    return search(root.right, value)


class BinarySearchKey:
    def __init__(self, root: Node, value):
        self.root = root
        self.value = value
        self.directions = []

        self.Search()

    def Right(self):
        self.directions.insert(0, 1)

    def Left(self):
        self.directions.insert(0, -1)

    def Search(self):
        if str(self.root.item) == str(self.value):
            return

        if str(self.root.item) > str(self.value):
            if self.root.left is None:
                return None

            self.Left()
            return search(self.root.left, self.value)

        if self.root.right is None:
            return

        self.Right()
        return search(self.root.right, self.value)

    def Navigate(self):
        node = self.root

        for direction in self.directions:
            if direction == -1:
                node = node.left
            else:
                node = node.right

        return node.item


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def __getitem__(self, bstKey: BinarySearchKey):
        return bstKey.Navigate()

    def __add__(self, other) -> BinarySearchKey:
        self.root = insert(self.root, other)
        return BinarySearchKey(self.root, other)


bst = BinarySearchTree()

keys = [bst + "value1", bst + "value2", bst + 1]

for key in keys:
    print(key.Navigate())
