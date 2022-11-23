import multiprocessing
from typing import Generator, List, Sequence, Tuple, TypeVar

T = TypeVar("T")


def chunks(lst: List[T], n: int) -> Generator[List[T], None, None]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

def pairs() -> Generator[Tuple[int,int], None, None]:
    for i in range(0, n):
        for j in range(i, n):
            yield i, j 


n = 1000
cpu_count = multiprocessing.cpu_count()
c = list(chunks(list(pairs()), multiprocessing.cpu_count()))


def f(lst: List[Tuple[int,int]]):
    for a, b in lst:
        a_cubed = a * a * a
        b_cubed = b * b * b
        for c in range(1, n):
            if c == a or c == b:
                continue
            c_cubed = c**3
            if c_cubed < a_cubed + b_cubed:
                for d in range(c, n):
                    if d == a or d == b or d == c:
                        continue
                    if (a_cubed + b_cubed) == (c_cubed + d**3):
                        print(a, b, a**3 + b**3, c, d)


with multiprocessing.Pool(cpu_count) as p:
    print(p.map(f, c))
