def fib_generator(n):
    if n <= 0:
        return

    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
n =int(input())
for i in fib_generator(n):
    print(i, end=" ")