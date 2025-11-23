import threading
import time

num = [0]


def test1():
    for i in range(5):
        num.append(i+1)
        time.sleep(1)


def test2():
    for i in range(5):
        print(num)
        time.sleep(1)


def main():
    t1 = threading.Thread(target = test1)
    t2 = threading.Thread(target = test2)
    t1.start()
    t2.start()
    time.sleep(2)
    print(f"最终：{num}")

if __name__ == "__main__":
    main()