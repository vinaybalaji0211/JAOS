class BaseRegistry:
    """
    Base registry for storing and managing Executive Brain objects.

    Registries do not make decisions.
    Registries do not execute actions.
    Registries only manage objects.
    """

    def __init__(self):
        self._items = {}

    def add(self, item_id, item):
        if not item_id:
            raise ValueError("item_id cannot be empty.")

        if item_id in self._items:
            raise ValueError(f"Item already exists: {item_id}")

        self._items[item_id] = item

    def get(self, item_id):
        return self._items.get(item_id)

    def update(self, item_id, item):
        if item_id not in self._items:
            raise KeyError(f"Item not found: {item_id}")

        self._items[item_id] = item

    def remove(self, item_id):
        if item_id not in self._items:
            raise KeyError(f"Item not found: {item_id}")

        return self._items.pop(item_id)

    def exists(self, item_id):
        return item_id in self._items

    def list_all(self):
        return list(self._items.values())

    def count(self):
        return len(self._items)

    def clear(self):
        self._items.clear()