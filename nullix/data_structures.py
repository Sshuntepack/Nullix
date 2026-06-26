"""Custom data structure implementations."""

from __future__ import annotations

from typing import Any, Iterator


class Stack:
    """A simple LIFO stack."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def push(self, item: Any) -> None:
        """Push an item onto the stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek on empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack is empty."""
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


class Queue:
    """A simple FIFO queue."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def enqueue(self, item: Any) -> None:
        """Add an item to the back of the queue."""
        self._items.append(item)

    def dequeue(self) -> Any:
        """Remove and return the front item."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def front(self) -> Any:
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError("front on empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        """Return True if the queue is empty."""
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Queue({self._items!r})"


class LinkedList:
    """A singly linked list."""

    class _Node:
        __slots__ = ("value", "next")

        def __init__(self, value: Any, nxt: LinkedList._Node | None = None) -> None:
            self.value = value
            self.next = nxt

    def __init__(self) -> None:
        self._head: LinkedList._Node | None = None
        self._size: int = 0

    def prepend(self, value: Any) -> None:
        """Insert a value at the front of the list."""
        self._head = self._Node(value, self._head)
        self._size += 1

    def append(self, value: Any) -> None:
        """Insert a value at the end of the list."""
        new_node = self._Node(value)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def remove(self, value: Any) -> None:
        """Remove the first occurrence of a value."""
        prev = None
        current = self._head
        while current is not None:
            if current.value == value:
                if prev is None:
                    self._head = current.next
                else:
                    prev.next = current.next
                self._size -= 1
                return
            prev = current
            current = current.next
        raise ValueError(f"{value!r} not in list")

    def __contains__(self, value: Any) -> bool:
        current = self._head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return f"LinkedList([{', '.join(repr(v) for v in self)}])"
