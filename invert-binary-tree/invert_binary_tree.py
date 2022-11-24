from treelib import Node, Tree
from typing import Any, TypeVar
from binary_tree import BinaryTree, Codec

T = TypeVar("T")


def invert(tree: BinaryTree[T]) -> BinaryTree[T]:
    return BinaryTree(
        value=tree.value,
        left=invert(tree.right) if tree.right is not None else None,
        right=invert(tree.left) if tree.left is not None else None,
    )


def show_tree(tree: BinaryTree[Any]):
    treelib_tree = Tree()
    for parent, node in BinaryTree.visit_depth_first(tree):
        treelib_tree.create_node(node.value, node.value, parent=parent.value if parent is not None else None)  # type: ignore
    treelib_tree.show()  # type: ignore


def main():
    """
    # >>> BinaryTree.from_string("()", int)

    # >>> BinaryTree.from_string("(", int)
    # Traceback (most recent call last):
    # ...
    # Exception: Unexpected character None at position 1

    # >>> BinaryTree.from_string("(1)", int)
    # BinaryTree(value=1, left=None, right=None)

    # >>> BinaryTree.from_string("(1(2))", int)
    # BinaryTree(value=1, left=BinaryTree(value=2, left=None, right=None), right=None)

    # >>> BinaryTree.from_string("(1()(2))", int)
    # BinaryTree(value=1, left=None, right=BinaryTree(value=2, left=None, right=None))

    >>> BinaryTree.from_string("(1(3(4)(5))(2))", int)
    BinaryTree(value=1, left=BinaryTree(value=3, left=BinaryTree(value=4, left=None, right=None), right=BinaryTree(value=5, left=None, right=None)), right=BinaryTree(value=2, left=None, right=None))

    """
    tree = Codec().deserialize("(1(3(4)(5))(2))", int)
    assert tree
    show_tree(invert(tree))

    pass


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
