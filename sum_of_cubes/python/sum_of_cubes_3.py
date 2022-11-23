from typing import Dict, List, Tuple

n: int = 1000

com: Dict[int, List[Tuple[int,int]]] = {}
for a in range(1, n):
    for b in range(a, n):
        s = a**3 + b**3
        if s not in com: 
            com[s] = []
        com[a**3 + b**3].append((a, b))

for s, nn in com.items():
    if len(nn) > 1:
        print(nn)

