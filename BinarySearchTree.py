
class Node:
    def __init__(self, itemKey, itemValue):
        self.itemKey = itemKey
        self.itemValue = itemValue
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.itemValue)

    def keyValueStr(self):
        return f"{self.itemKey} -> {self.itemValue}"


# Tries to insert a new key -> value pair, if it already exists nothing happens, based on key appearance
def insert(root: Node, key: int, value):
    # If we get here it means that the key is not in the tree
    if root is None:
        return Node(key, value)

    # We found the key inside the tree so we return this node to the parent
    if root.itemKey == key:
        return root

    # Search by key
    if root.itemKey < key:
        # Replace the child if necessary
        root.right = insert(root.right, key, value)
    else:
        # Replace the child if necessary
        root.left = insert(root.left, key, value)

    # Return the root to the parent
    return root


def search(root: Node, key: int):
    # If we get here it means that the key is not in the tree
    if root is None:
        return None

    # We found the key inside the tree so we return this node
    if root.itemKey == key:
        return root

    # Search by key
    if root.itemKey < key:
        # Search in the right sub-tree
        return search(root.right, key)

        # Search in the left sub-tree
    return search(root.left, key)


# Inorder traversal of the tree that builds a dictionary of the value -> key pairs
# IMPORTANT: The nodes dict has to be empty, here we will get the result
def inorder(root: Node, nodes: dict):
    if root:
        # Traverse left sub-tree
        inorder(root.left, nodes)
        # Put the key -> value pair in the dict
        nodes[root.itemKey] = root.itemValue
        # Traverse right sub-tree
        inorder(root.right, nodes)


class BinarySearchTree:
    def __init__(self):
        # The starting root of the tree
        self.root = None
        # A list of all entries up until now
        self.entryKeys = []

    # [] operator to get the value of the key
    def __getitem__(self, key):
        return search(self.root, key)

    # [] setter for the key -> value pair
    def __setitem__(self, key, value):
        # if the key is not inside the tree then we add it to the list of keys
        if not search(self.root, key):
            self.entryKeys.append(key)

        # Set the root and parse the tree
        self.root = insert(self.root, key, value)

    # Returns the list of keys
    def keys(self):
        return self.entryKeys

    # Pops the item at <key> or returns the "returnValue" if not found
    def pop(self, key, returnValue=None):
        # TODO: If necessary
        pass

    def __str__(self):
        nodes = {}
        inorder(self.root, nodes)
        return str(nodes)
