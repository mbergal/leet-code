from functools import lru_cache
from typing import Generator, List, Tuple


@lru_cache
def is_next_word_for(word: str, next_word: str) -> bool:
    """
    >>> is_next_word_for("dot","dog")
    True

    >>> is_next_word_for("dot","hog")
    False

    """
    return len([x == y for (x, y) in zip([*word], [*next_word]) if x != y]) == 1


def f_next(
    word: str, *, end_word: str, list: Tuple[str,...]
) -> Generator[List[str], None, None]:
    """
    >>> list(f_next("dog", end_word="dog", list=[]))
    [[]]

    >>> list(f_next("dot", end_word="dog", list=["dog"]))
    [['dog']]

    >>> list(f_next("hot", end_word="dog", list=["got", "dot", "dog"]))
    [['got', 'dot', 'dog'], ['dot', 'dog']]

    >>> list(f_next("hit", end_word="cog", list=["hot","dot","dog","lot","log","cog"]))
    [['hot', 'dot', 'dog', 'log', 'cog'], ['hot', 'dot', 'dog', 'cog'], ['hot', 'dot', 'lot', 'log', 'dog', 'cog'], ['hot', 'dot', 'lot', 'log', 'cog'], ['hot', 'lot', 'dot', 'dog', 'log', 'cog'], ['hot', 'lot', 'dot', 'dog', 'cog'], ['hot', 'lot', 'log', 'dog', 'cog'], ['hot', 'lot', 'log', 'cog']]
    """
    print(list)
    if word == end_word:
        yield []
    for w in [next_word for next_word in list if is_next_word_for(word, next_word)]:
        if w == end_word:
            yield [w]
        else:
            for next in f_next(w, end_word=end_word, list=tuple([x for x in list if x != w])):
                yield [w] + next


def shortest_ladders(start_word: str, end_word: str, word_list: Tuple[str,...]):
    """
    # >>> shortest_ladders("hit", "cog", ["hot","dot","dog","lot","log","cog"])
    # [['hot', 'dot', 'dog', 'cog'], ['hot', 'lot', 'log', 'cog']]

    >>> shortest_ladders("qa", "sq", ["si","go","se","cm","so","ph","mt","db","mb","sb","kr","ln","tm","le","av","sm","ar","ci","ca","br","ti","ba","to","ra","fa","yo","ow","sn","ya","cr","po","fe","ho","ma","re","or","rn","au","ur","rh","sr","tc","lt","lo","as","fr","nb","yb","if","pb","ge","th","pm","rb","sh","co","ga","li","ha","hz","no","bi","di","hi","qa","pi","os","uh","wm","an","me","mo","na","la","st","er","sc","ne","mn","mi","am","ex","pt","io","be","fm","ta","tb","ni","mr","pa","he","lr","sq","ye"])

    """

    def min_func(x: List[str]):
        return len(x)

    ladders = list(f_next(start_word, end_word=end_word, list=tuple(word_list)))

    shortest_length = len(min(ladders, key=min_func))

    return [l for l in ladders if len(l) == shortest_length]


def main():
    import doctest

    doctest.testmod()

    pass


if __name__ == "__main__":
    main()
