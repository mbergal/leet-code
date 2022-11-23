package main

import "fmt"

func cube(x int) int { return x * x * x }

func main() {

	var n = 1000
	for a := 1; a <= n; a += 1 {
		for b := a + 1; b <= n; b += 1 {
			for c := 1; c <= n; c += 1 {
				if c != a && c != b {
					if cube(c) < cube(a)+cube(b) {
						for d := c + 1; d <= n; d += 1 {
							if d != a && d != b && d != c {
								if cube(a)+cube(b) == cube(c)+cube(d) {
									fmt.Println(a, b, (cube(a) + cube(b)), c, d)
								}
							}
						}
					}
				}

			}
		}
	}
}
