fn cube(x: u64) -> u64 {
    return x * x * x;
}

fn main() {
    let n = 1000;
    for a in 1..n {
        let a_cubed = cube(a);
        for b in a + 1..n {
            let b_cubed = cube(b);
            for c in 1..n {
                let c_cubed = cube(c);
                if c != a && c != b {
                    if c_cubed < a_cubed + b_cubed {
                        for d in c + 1..n {
                            if d != a && d != b && d != c {
                                if a_cubed + b_cubed == c_cubed + cube(d) {
                                    println!("{} {} {} {} {}", a, b, (a_cubed + b_cubed), c, d)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
