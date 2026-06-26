"""Tests for nullix.data_structures — comprehensive coverage."""

import pytest

from nullix.data_structures import LinkedList, Queue, Stack


class TestStack:
    def test_push_and_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_peek(self):
        s = Stack()
        s.push("a")
        assert s.peek() == "a"
        assert len(s) == 1

    def test_is_empty(self):
        s = Stack()
        assert s.is_empty() is True
        s.push(1)
        assert s.is_empty() is False

    def test_pop_empty(self):
        with pytest.raises(IndexError, match="empty stack"):
            Stack().pop()

    def test_peek_empty(self):
        with pytest.raises(IndexError, match="empty stack"):
            Stack().peek()

    def test_len(self):
        s = Stack()
        assert len(s) == 0
        s.push(1)
        s.push(2)
        assert len(s) == 2

    def test_repr(self):
        s = Stack()
        s.push(1)
        assert repr(s) == "Stack([1])"


class TestQueue:
    def test_enqueue_and_dequeue(self):
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")
        assert q.dequeue() == "a"
        assert q.dequeue() == "b"

    def test_front(self):
        q = Queue()
        q.enqueue(10)
        assert q.front() == 10
        assert len(q) == 1

    def test_is_empty(self):
        q = Queue()
        assert q.is_empty() is True
        q.enqueue(1)
        assert q.is_empty() is False

    def test_dequeue_empty(self):
        with pytest.raises(IndexError, match="empty queue"):
            Queue().dequeue()

    def test_front_empty(self):
        with pytest.raises(IndexError, match="empty queue"):
            Queue().front()

    def test_len(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        assert len(q) == 3

    def test_repr(self):
        q = Queue()
        q.enqueue(1)
        assert repr(q) == "Queue([1])"


class TestLinkedList:
    def test_prepend(self):
        ll = LinkedList()
        ll.prepend(1)
        ll.prepend(2)
        assert list(ll) == [2, 1]

    def test_append(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        assert list(ll) == [1, 2]

    def test_append_to_empty(self):
        ll = LinkedList()
        ll.append(42)
        assert list(ll) == [42]

    def test_remove_head(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.remove(1)
        assert list(ll) == [2]
        assert len(ll) == 1

    def test_remove_middle(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.remove(2)
        assert list(ll) == [1, 3]

    def test_remove_not_found(self):
        ll = LinkedList()
        ll.append(1)
        with pytest.raises(ValueError, match="not in list"):
            ll.remove(99)

    def test_contains(self):
        ll = LinkedList()
        ll.append("a")
        ll.append("b")
        assert "a" in ll
        assert "c" not in ll

    def test_len(self):
        ll = LinkedList()
        assert len(ll) == 0
        ll.append(1)
        ll.append(2)
        assert len(ll) == 2

    def test_iter(self):
        ll = LinkedList()
        ll.append(10)
        ll.append(20)
        assert list(ll) == [10, 20]

    def test_repr(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        assert repr(ll) == "LinkedList([1, 2])"
