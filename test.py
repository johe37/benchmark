def sum(x, y):
    return x + y

def echo(funcc):
    print(funcc())

echo(lambda: sum(10, 2))
