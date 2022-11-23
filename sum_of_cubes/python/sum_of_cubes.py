import multiprocessing
from typing import Generator, List, Sequence, TypeVar

T = TypeVar("T")


def chunks(lst: List[T], n: int) -> Generator[List[T], None, None]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


n = 1000
cpu_count = multiprocessing.cpu_count()
c: List[List[int]] = list(chunks(list(range(1, n)), multiprocessing.cpu_count()))


def f(numbers: Sequence[int]):
    for a in numbers:
        a_cubed = a**3
        for b in range(a, n):
            if a == b:
                continue
            b_cubed = b**3
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
