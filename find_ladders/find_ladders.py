import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, Generator, List, Mapping, Optional, Sequence, Set, TypedDict

import graphviz


@lru_cache
def is_next_word_for(word: str, next_word: str) -> bool:
    """
    >>> is_next_word_for("dot","dog")
    True

    >>> is_next_word_for("dot","hog")
    False

    """
    return len([x == y for (x, y) in zip([*word], [*next_word]) if x != y]) == 1


def adjacent_words(word: str, words: Set[str], visited: Set[str]) -> Set[str]:
    """ """
    r = {
        next_word
        for next_word in words
        if next_word not in visited and is_next_word_for(word, next_word)
    }
    return r


Graph = Dict[str, Set[str]]
Step = Graph


def graph_to_str(g: Optional[Graph]):
    """
    >>> graph_to_str(None)
    ''

    >>> graph_to_str({})
    '{}'

    >>> graph_to_str({'a': {'a'}})
    "{'a': {'a'}}"

    >>> graph_to_str({'a': {'a', 'b'}})
    "{'a': {'a', 'b'}}"

    >>> graph_to_str({'bc': set(), 'ba': {'bc'}, 'aa': {'ba'}})
    "{'aa': {'ba'}, 'ba': {'bc'}, 'bc': {}}"
    """
    if g is not None:
        a = {k: list(sorted(list(v))) for k, v in sorted(g.items())}

        return str(a).replace("[", "{").replace("]", "}")
    else:
        return ""


def merge_graphs(g: Sequence[Graph]) -> Graph:
    """
    >>> merge_graphs([])
    {}

    >>> graph_to_str(merge_graphs([{'a': {'a'}}]))
    "{'a': {'a'}}"

    >>> graph_to_str(merge_graphs([{'a': 'a'}, {'b': 'b'}]))
    "{'a': {'a'}, 'b': {'b'}}"

    >>> graph_to_str(merge_graphs([{'a': 'a', 'b': 'c'}, {'b': 'b'}]))
    "{'a': {'a'}, 'b': {'b', 'c'}}"

    """
    merged: Graph = {}
    for s in g:
        for k, w in s.items():
            if merged.get(k) is None:
                merged[k] = set()
            merged[k].update(w)

    return merged


def find_path_backward(start_word: str, end_word: str, words: Set[str]):

    visited: Set[str] = {start_word}
    steps: List[Step] = [{start_word: set()}]

    while True:
        next_words: Set[str] = set()
        for current_word in steps[-1]:
            current_word_next_words = adjacent_words(current_word, words, visited)
            steps[-1][current_word] = current_word_next_words
            next_words = next_words.union(current_word_next_words)
        visited.update(next_words)
        steps.append({word: set() for word in next_words})

        if end_word in next_words:
            break

        if next_words == set():
            return

    return steps


def used_words(graph: Graph, nn: Set[str]):
    """
    >>> used_words({'a': {'b', 'c'}}, {'b'})
    {'a': {'b'}}
    """
    return {
        word: graph[word].intersection(nn)
        for word, s in graph.items()
        if len(s.intersection(nn)) > 0
    }

def find_path_forward(graph: Graph, end_word: str):
    new_graph: Graph = {end_word: graph[end_word]}
    prev_step_words: Set[str] = {end_word}
    while True:
        step_used_words: Graph = used_words(graph, prev_step_words)
        new_graph = merge_graphs([new_graph, step_used_words])
        prev_step_words = set(step_used_words.keys())
        if prev_step_words == set():
            break
    
    return new_graph


def find_shortest_path(
    start_word: str, end_word: str, words: Set[str]
) -> Optional[Graph]:
    """
    >>> graph_to_str(find_shortest_path("a", "b", {"a", "b"}))
    "{'a': {'b'}, 'b': {}}"

    >>> graph_to_str(find_shortest_path("aa", "bc", {"aa", "bc", "ba" }))
    "{'aa': {'ba'}, 'ba': {'bc'}, 'bc': {}}"

    >>> graph_to_str(find_shortest_path("hit", "cog", {"hot","dot","dog","lot","log", "cog"}))
    "{'cog': {}, 'dog': {'cog'}, 'dot': {'dog'}, 'hit': {'hot'}, 'hot': {'dot', 'lot'}, 'log': {'cog'}, 'lot': {'log'}}"

    >>> graph_to_str(find_shortest_path("hit", "cog", {"hot","dot","dog","lot","log"}))
    ''
    """

    steps = find_path_backward(start_word, end_word, words)
    if steps is None:
        return None

    new_steps = find_path_forward(merge_graphs(steps), end_word)

    return new_steps


def shortest_ladders(start_word: str, end_word: str, word_list: Set[str]):
    """
    # >>> print(shortest_ladders("hit", "cog", {"hot","dot","dog","lot","log", "cog"}))
    # [['hit', 'hot', 'dot', 'dog', 'cog'], ['hot', 'lot', 'log', 'cog']]
    """
    g = find_shortest_path(start_word, end_word, word_list)

    if g is not None:
        a = g

        # # show_steps(steps, word_list)
        # dot = graphviz.Digraph(comment="The Round Table")

        # for step in g:
        #     for word, next_words in step.items():
        #         dot.node(word)
        #         for next in next_words:
        #             dot.edge(word, next)

        # dot.render("round-table.gv")
        return list(all_paths(a, start_word, end_word))


def all_paths(
    graph: Mapping[str, Set[str]], start: str, end: str
) -> Generator[List[str], None, None]:
    if start == end:
        yield [start]
    if graph[start] == set():
        pass
    else:
        next = graph[start]
        for a in next:
            for b in all_paths(graph, a, end):
                yield [start] + b


def show_steps(steps: List[Step], words: Set[str]):
    for w in words:
        l = w
        for i in steps:
            l += "*" if w in i else "."
        print(l)


class TestData(TypedDict):
    start: str
    end: str
    list: List[str]


def test(file: Path):
    with open(file) as test_data_file:
        test_data: TestData = json.load(test_data_file)
        print(file)
        for x in (shortest_ladders(test_data["start"], test_data["end"], set(test_data["list"])) or []):
            print(x)
        print("")


def main():
    import doctest

    doctest.testmod()

    test(Path("./small.json"))
    test(Path("./large.json"))
    test(Path("./xlarge.json"))

    # print(shortest_ladders( "hit", "cog", {"hot","dot","dog","lot","log", "cog"}))


if __name__ == "__main__":
    main()
