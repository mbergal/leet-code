let cube x = x * x * x

let n = 1000
for a in 1..n do
    for b in a+1..n do
        for c in 1..n do
            if c <> a && c <> b then
                if cube(c) < cube(a) + cube(b) then
                    for d in c+1..n do
                        if d <> a && d <> b && d <> c then
                            if  cube(a) + cube(b) = cube(c) + cube(d) then
                                printf "%d %d %d %d %d \n" a b (cube(a)+cube(b)) c d

