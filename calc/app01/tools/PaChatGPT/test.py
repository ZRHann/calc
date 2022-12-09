def f1():
    global server
    print(server)


if __name__ == "__main__":
    global server
    server = 1
    f1()