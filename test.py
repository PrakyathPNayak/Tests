def is_safe(b, r, c): return all(b[i]!=c and abs(b[i]-c)!=r-i for i in range(r))


def solve_n_queens(N, b=[]):
    if len(b) == N:
        print(b)
        return
    for c in range(N):
        if is_safe(b, len(b), c): solve_n_queens(N, b + [c])


solve_n_queens(8)
a=input("press enter\n")
