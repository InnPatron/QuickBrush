def try_init_collection(c, n):
    size = len(c)
    diff = n - size
    if size <= n:
        for i in range(0, diff):
            b = c.add()
    else:
        for i in range(0, diff):
            c.pop()
