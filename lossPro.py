import matplotlib.pyplot as plt

def test():
    # f = 'delay\\video0928.txt'
    delay = []
    stamp = []
    t = 1
    p = 1
    for i in range(1,1000):
        stamp.append(t)
        if t in [13,456,457,458,875]:
            p = p - 1
        else: pass
        delay.append(p/t)
        t = t + 1
        p = p + 1





    # with open(f, 'r') as file:
    #     while True:
    #         line = file.readline()
    #
    #         if not line:
    #             break
    #             pass
    #
    #         i = line.strip().split(",")
    #         p = ((float)(i[1]) - (float)(i[0]))*1000
    #         if p > 400:
    #             p = p-40
    #         delay.append(p)
    #         stamp.append(t)
    #         t = t + 1
    plt.plot(stamp,delay)
    plt.grid(True)
    plt.xlabel('count')
    plt.ylabel('rate')
    plt.ylim(0.9, 1.02)
    # plt.xlim(0, 150)
    # c = np.mean(delay)
    # plt.axhline(y=c,color='red')
    plt.title('Command packet loss rate')
    plt.show()
    print(stamp,delay)
    # print(c)

if __name__ == '__main__':
    test()