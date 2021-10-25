import matplotlib.pyplot as plt
import numpy as np
import datetime
from mpl_toolkits.axisartist.parasite_axes import HostAxes,ParasiteAxes

def pro(fname,outname):
    f = fname
    time = []
    pci = []
    tp = 0

    flag = datetime.datetime.strptime('17:01:00','%H:%M:%S')
    with open(f,'r') as file:
        while True:
            line = file.readline()
            if not line:
                break

            i = line.strip().split(',')
            temp = i[0].split(' ')[1].split('.')[0]
            temp = datetime.datetime.strptime(temp,'%H:%M:%S')

            # print(temp)
            if temp != flag:

                p=datetime.datetime.strptime('17:01:00','%H:%M:%S')
                # if (temp-flag).seconds > 1:
                #     time.append((flag-p).seconds+1)
                #     pci.append(tp)

                # time.append(temp-(datetime.datetime.strptime('10:32:37','%H:%M:%S').time()).second)

                time.append((temp - p).seconds)
                pci.append((int)(i[1]))

            # tp = (int)(i[1])
            flag = temp
    map = [list(x) for x in zip(time,pci)]
    with open(outname,'w') as out:
        for a,b in map:

            out.write(str(b))
            out.write("\n")
            print(a)
    # print(time,pci)
    # return time,pci


if __name__ == '__main__':
    f = '09271705pci.csv'
    out = 'pci2.txt'
    pro(f,out)