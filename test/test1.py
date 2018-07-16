def func():
    a = 1
    def B():
        nonlocal a
        a += 1
        print("...................", a)

    B()

func()