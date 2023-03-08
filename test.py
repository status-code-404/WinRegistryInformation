def time_cal(func):
    def a(*args):
        import time
        a = time.time()
        func(*args)
        b = time.time()
        print(b - a)
    return a


@time_cal
def k(n):
    if n == 0 or n == 1:
        return 1, 1
    last = 1
    now = 1
    for i in range(n):
        if i == 0 or i == 1:
            continue
        last1 = now
        now = now + last if now + last <= 10007 else now + last - 10007
        last = last1
        if now >= 10007:
            now -= 10007
    return now, last


if __name__ == '__main__':
    print(k(1000000))
