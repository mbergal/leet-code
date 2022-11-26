from typing import Dict, Generator, List, Literal, Mapping, Set, Union


Node = Union[
    Literal["hit"],
    Literal["hot"],
    Literal["dot"],
    Literal["lot"],
    Literal["dog"],
    Literal["log"],
    Literal["cog"],
    Literal["lag"],
]

g: Dict[Node, Set[Node]] = {
    "hit": {"hot"},
    "hot": {"dot", "lot"},
    "dot": {"dog"},
    "lot": {"log"},
    "dog": {"cog"},
    "log": {"cog"},
    "cog": set(),
}

def all_paths(graph: Mapping[str, Set[str]], start: str, end:str) -> Generator[List[str], None, None]:
    if start == end:
        yield [start]
    if graph[start] == set():
        pass
    else:
        next = graph[start]
        for a in next:
            for b in all_paths(g, a, end):
                yield [start] + b


def show(paths: Generator[List[str], None, None]) :
    for a in list(sorted(paths)):
        print(a)
                
def main():
    """
    >>> show( all_paths(g, "hit", "cog") )
    ['hit', 'hot', 'dot', 'dog', 'cog']
    ['hit', 'hot', 'lot', 'log', 'cog']

    >>> show( all_paths(g, "hit", "lag") )
    """
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    main()


