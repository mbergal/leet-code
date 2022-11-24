from dataclasses import dataclass
from typing import Any, Callable, Generator, Generic, Optional, TypeVar, Tuple

T = TypeVar("T")


@dataclass
class BinaryTree(Generic[T]):
    value: T
    left: Optional["BinaryTree[T]"] = None
    right: Optional["BinaryTree[T]"] = None

    @staticmethod
    def visit_depth_first(
        tree: "BinaryTree[T]", parent: Optional["BinaryTree[T]"] = None
    ) -> Generator[Tuple[Optional["BinaryTree[T]"], "BinaryTree[T]"], None, None]:
        yield (parent, tree)
        if tree.left is not None:
            yield from BinaryTree.visit_depth_first(tree.left, tree)
        if tree.right is not None:
            yield from BinaryTree.visit_depth_first(tree.right, tree)


class Codec:
    def serialize(self, tree: "BinaryTree[Any]") -> str:
        return self._serialize(tree)

    def deserialize(
        self, str: str, value_deserializer: Callable[[str], T]
    ) -> Optional["BinaryTree[T]"]:
        return BinaryTreeParser(str, value_deserializer).parse()

    def _serialize(self, tree: Optional["BinaryTree[Any]"]) -> str:
        if tree is not None:
            return f"({tree.value}{self._serialize(tree.left) }{self._serialize(tree.right)})"
        else:
            return "()"


class BinaryTreeParser(Generic[T]):
    position: int
    stream: str
    converter: Callable[[str], T]

    def __init__(self, stream: str, value_converter: Callable[[str], T]) -> None:
        super().__init__()
        self.position = 0
        self.stream = stream
        self.converter = value_converter

    def _(self):
        return self.stream[self.position :]

    def peek(self):
        if self.position < len(self.stream):
            return self.stream[self.position]
        else:
            return None

    def read(self):
        if self.position < len(self.stream):
            r = self.stream[self.position]
            self.position += 1
            return r
        else:
            return None

    def readNonNone(self):
        r = self.read()
        if r is None:
            raise Exception("Expected non-None value")
        return r

    def parse(self) -> Optional["BinaryTree[T]"]:
        if self.read() == "(":
            value = ""
            while not self.peek() in ["(", ")", None]:
                value += self.readNonNone()

            if self.peek() == ")":
                self.read()
                if value.strip() == "":
                    return None
                else:
                    return BinaryTree(self.converter(value), left=None, right=None)
            elif self.peek() == "(":
                left = self.parse()
                if self.stream[self.position] == "(":
                    right = self.parse()
                else:
                    right = None
                if self.peek() != ")":
                    raise Exception("Expected closing parenthesis")
                else:
                    self.read()
                return BinaryTree(self.converter(value), left=left, right=right)
            else:
                raise Exception(
                    f"Unexpected character {self.peek()} at position {self.position}"
                )
