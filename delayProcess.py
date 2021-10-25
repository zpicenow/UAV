import matplotlib.pyplot as plt
import numpy as np
import datetime
from mpl_toolkits.axisartist.parasite_axes import HostAxes,ParasiteAxes
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA


def pro(fname):
    f = fname
    time = []
    pci = []

    flag = datetime.datetime.strptime('00:00:00','%H:%M:%S').time()
    with open(f,'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
                pass
            i = line.strip().split(',')
            temp = i[0].split(' ')[1].split('.')[0]
            temp = datetime.datetime.strptime(temp,'%H:%M:%S')
            # print(temp)
            if temp != flag:
                # time.append(temp-(datetime.datetime.strptime('10:32:37','%H:%M:%S').time()).second)
                p=datetime.datetime.strptime('17:07:18','%H:%M:%S')
                time.append((temp - p).seconds)
                pci.append((int)(i[1]))

            flag = temp
    # print(time,pci)
    return time,pci

delay = []
stamp = []

def test():
    f = '09271707\\0927170718.txt'

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
    # plt.plot(stamp,delay)
    # # plt.plot(time,pci)
    # plt.grid(True)
    # plt.xlabel('Time/s')
    # plt.ylabel('Delay/ms')
    # mean = np.mean(delay)
    # min = np.min(delay)
    # print(mean,min)
    # plt.axhline(y=c, color='red')
    # plt.title('Single delay of uplink control command')
    # plt.show()



if __name__ == '__main__':
    # print("{UAV:67,Phone:67}".strip("}"))
    # test()
    # time1, pci = pro('09271707\\0927171109pci.csv')
    time2, rssi = pro('09271707\\0927171109rssi.csv')
    time3, rsrp = pro('09271707\\0927171109rsrp.csv')
    time4, rsrq = pro('09271707\\0927171109rsrq.csv')
    time5, sinr = pro('09271707\\0927171109sinr.csv')
    test()

    fig = plt.figure(figsize=(10,6))
    ax_delay = HostAxes(fig,[0.11,0.1,0.7,0.83])

    ax_pci = ParasiteAxes(ax_delay, sharex=ax_delay)
    ax_rssi = ParasiteAxes(ax_delay,sharex=ax_delay)
    ax_rsrp = ParasiteAxes(ax_delay,sharex=ax_delay)
    ax_rsrq = ParasiteAxes(ax_delay,sharex=ax_delay)
    ax_sinr = ParasiteAxes(ax_delay,sharex=ax_delay)


    ax_delay.parasites.append(ax_pci)
    ax_delay.parasites.append(ax_rssi)
    ax_delay.parasites.append(ax_rsrp)
    ax_delay.parasites.append(ax_rsrq)
    ax_delay.parasites.append(ax_sinr)

    ax_delay.axis['right'].set_visible(False)
    ax_delay.axis['top'].set_visible(False)
    ax_pci.axis['right'].set_visible(True)
    ax_pci.axis['right'].major_ticklabels.set_visible(True)
    ax_pci.axis['right'].label.set_visible(True)

    ax_delay.set_ylabel('Delay(ms)')
    ax_delay.set_xlabel('Time(s)')
    # ax_pci.set_ylabel('pci')
    # ax_rssi.set_ylabel('RSSI')
    # ax_rsrp.set_ylabel('RSRP')
    # ax_rsrq.set_ylabel('RSRQ')
    # ax_sinr.set_ylabel('SINR')

    rssi_axisline = ax_rssi.get_grid_helper().new_fixed_axis
    rsrp_axisline = ax_rsrp.get_grid_helper().new_fixed_axis
    rsrq_axisline = ax_rsrq.get_grid_helper().new_fixed_axis
    sinr_axisline = ax_sinr.get_grid_helper().new_fixed_axis

    ax_rssi.axis['right2'] = rssi_axisline(loc='right',axes=ax_rssi,offset=(20,0))
    ax_rsrp.axis['right3'] = rsrp_axisline(loc='right',axes=ax_rsrp,offset=(45,0))
    ax_rsrq.axis['right4'] = rsrq_axisline(loc='right',axes=ax_rsrq,offset=(70,0))
    ax_sinr.axis['right5'] = sinr_axisline(loc='right',axes=ax_sinr,offset=(95,0))

    fig.add_axes(ax_delay)


    curve_delay, = ax_delay.plot(stamp,delay,label="delay")
    # curve_pci, = ax_pci.plot(time1,pci,label="pci")
    curve_rssi, = ax_rssi.plot(time2,rssi,label="rssi")
    curve_rsrp, = ax_rsrp.plot(time3,rsrp,label="rsrp")
    curve_rsrq, = ax_rsrq.plot(time4,rsrq,label="rsrq")
    curve_sinr, = ax_sinr.plot(time5,sinr,label="sinr")

    # ax_temp.set_ylim(-80, -60)
    # ax_load.set_ylim(-110, -80)
    # ax_cp.set_ylim(-20, 0)
    # ax_wear.set_ylim(0, 30)

    ax_delay.set_ylim(0,300)
    ax_pci.set_ylim(470, 480)
    ax_rssi.set_ylim(-220, -0)

    ax_rsrp.set_ylim(-140, -20)
    ax_rsrq.set_ylim(-30, 20)
    ax_sinr.set_ylim(-55, 150)

    ax_delay.legend()

    # ax_pci.axis['right'].label.set_color(curve_pci.get_color())
    ax_rssi.axis['right2'].label.set_color(curve_rssi.get_color())
    ax_rsrp.axis['right3'].label.set_color(curve_rsrp.get_color())
    ax_rsrq.axis['right4'].label.set_color(curve_rsrq.get_color())
    ax_sinr.axis['right5'].label.set_color(curve_sinr.get_color())

    # ax_pci.axis['right'].major_ticks.set_color('red')
    # ax_rssi.axis['right2'].major_ticks.set_color('green')
    # ax_rsrp.axis['right3'].major_ticks.set_color('pink')
    # ax_rsrq.axis['right4'].major_ticks.set_color('blue')
    # ax_sinr.axis['right5'].major_ticks.set_color('yellow')
    #
    # ax_pci.axis['right'].major_ticklabels.set_color(curve_pci.get_color())
    ax_rssi.axis['right2'].major_ticklabels.set_color(curve_rssi.get_color())
    ax_rsrp.axis['right3'].major_ticklabels.set_color(curve_rsrp.get_color())
    ax_rsrq.axis['right4'].major_ticklabels.set_color(curve_rsrq.get_color())
    ax_sinr.axis['right5'].major_ticklabels.set_color(curve_sinr.get_color())

    # ax_pci.axis['right'].line.set_color(curve_pci.get_color())
    ax_rssi.axis['right2'].line.set_color(curve_rssi.get_color())
    ax_rsrp.axis['right3'].line.set_color(curve_rsrp.get_color())
    ax_rsrq.axis['right4'].line.set_color(curve_rsrq.get_color())
    ax_sinr.axis['right5'].line.set_color(curve_sinr.get_color())

    plt.show()

