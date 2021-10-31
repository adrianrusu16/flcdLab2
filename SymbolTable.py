from BinarySearchTree import BinarySearchTree
from random import shuffle


# Symbol table class.
# Contains 2 data structures, one that maps keys -> values and one that maps values -> keys
# for fast search both ways, of both keys and values.
# It also contains a uuid that will give each new entry a new id.
# The values are sorted in the order they were put in the table, their keys going in ascending order
class SymbolTable:
    # Initializes the 2 dictionaries and the uuid with 0
    # Complexity: Theta(1) (with dicts)
    def __init__(self, dataClass):
        self.keysToValues = dataClass()
        self.valuesToKeys = dataClass()
        self.uuid = 1

    # Tries to add an entry to the Symbol Table
    # Complexity: Theta(1) (with dicts)
    def __add__(self, item) -> int:
        # If the item already exists as a value then the key of said value is returned
        if self.valuesToKeys.get(item, None) is not None:
            return self.valuesToKeys[item]

        # If the item is not present in the dictionary then a uuid is given to it
        itemId = self.uuid

        # And the uuid "generator" moves to the next entry
        self.uuid += 1

        # The key -> value pairs are introduced in the symbol table
        self.keysToValues[itemId] = item
        self.valuesToKeys[item] = itemId

        # And the key is returned
        return itemId

    # Tries to return the value mapped to the "itemKey" in the Symbol Table
    # Complexity: Theta(1) (with dicts)
    def __getitem__(self, itemKey):
        # If the value exists then its key is returned
        if self.keysToValues.get(itemKey, None):
            return str(self.keysToValues[itemKey])

        # If it does not exist then <None> is returned
        return None

    # Tries to remove a key from the Symbol Table
    # Complexity: Theta(1) (with dicts)
    def removeKey(self, itemKey):
        # Tries to get the value corresponding to said key, if it doesn't exist <None> is received
        itemValue = self.keysToValues.pop(itemKey, None)

        # Pop the corresponding key if it exists
        self.valuesToKeys.pop(itemValue, None)

        # Return the key's value, whether it was found, or None if not
        return itemValue

    # Tries to remove a value from the Symbol Table
    # Complexity: Theta(1) (with dicts)
    def removeValue(self, itemValue):
        # Tries to get the key corresponding to said value, if it doesn't exist <None> is received
        itemKey = self.valuesToKeys.pop(itemValue, None)

        # Pop the corresponding value if it exists
        self.keysToValues.pop(itemKey, None)

        # Return the value's key, whether it was found, or None if not
        return itemKey

    # Returns the dictionary of the key -> value pairs
    # Complexity: Theta(1) (with dicts)
    def getAll(self) -> dict:
        return self.keysToValues.items()

    # Returns a view of the set of all keys
    # Complexity: Theta(1) (with dicts)
    def getAllKeys(self):
        return self.keysToValues.keys()

    # Returns a view of the set of all values
    # Complexity: Theta(1) (with dicts)
    def getAllValues(self):
        return self.valuesToKeys.keys()


if __name__ == '__main__':
    # Testing
    st = SymbolTable(BinarySearchTree)  # For binary search tree as data structure
    # st = SymbolTable(dict)  # For python dict as data structure
    values = ["value0", "value1", "value2", "value3", "_BigValue_1245325_BIIIIIG_", "5value5"]
    keys = []

    for value in values:
        keys.append(st + value)

    print(f"Keys: {keys}\n\n")
    print(f"Values in st: {st.getAllValues()}\n\n")

    print(f"key mappings in st from stored keys")
    for key in keys:
        print(f"key: {key} -> value: {st[key]}")

    print(f"\nkey mappings in st from shuffled list of stored keys")
    shuffle(keys)
    for key in keys:
        print(f"key: {key} -> value: {st[key]}")

    print(f"\nST dict: {st.getAll()}")
    print(f"\nST dict keys: {st.getAllKeys()}")
    print(f"\nST dict values: {st.getAllValues()}")

    print(f"\nInvalid key search of 124: {st[124]}")
    print(f"\nInvalid key search of {len(values)}: {st[len(values)]}")
    print(f"\nInvalid key search of -1: {st[-1]}")
