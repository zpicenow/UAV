import random

import matplotlib.pyplot as plt
import numpy as np


def test():
    f = 'delay\\video0928.txt'
    delay = []
    stamp = []
    t = 0
    with open(f, 'r') as file:
        while True:
            line = file.readline()

            if not line:
                break
                pass

            i = line.strip().split(",")
            p = ((float)(i[1]) - (float)(i[0]))*1000
            if p > 400:
                p = p-40
            delay.append(p)
            stamp.append(t)
            t = t + 1
    plt.plot(stamp,delay)
    plt.grid(True)
    plt.xlabel('Time/s')
    plt.ylabel('Delay/ms')
    plt.ylim(0, 1000)
    # plt.xlim(0, 150)
    c = np.mean(delay)
    plt.axhline(y=c,color='red')
    plt.title('Single delay of video streaming')
    plt.show()
    print(c)



if __name__ == '__main__':
    # print("{UAV:67,Phone:67}".strip("}"))
    test()