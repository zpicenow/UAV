import matplotlib.pyplot as plt
import numpy as np


def test():
    f = r'09271705\0927170100.txt'
    delay = []
    stamp = []
    t = 0
    with open(f, 'r') as file:
        while True:
            line = file.readline()

            if not line:
                break
                pass

            i = line.strip().strip("}").split(",")
            delay.append(((float)(i[0].split(':')[1]) + (float)((i[1].split(':'))[1])) / 2)
            stamp.append(t)
            t = t + 1
        # print(delay, stamp)
    plt.plot(stamp,delay)
    # # plt.plot(time,pci)
    plt.grid(True)
    plt.xlabel('Time/s')
    plt.ylabel('Delay/ms')
    plt.ylim(20,170)
    mean = np.mean(delay)
    # min = np.min(delay)
    # print(mean,min)
    plt.axhline(y=mean, color='red')
    # plt.title('Single delay of uplink control command')
    plt.show()

if __name__ == '__main__':
    test()