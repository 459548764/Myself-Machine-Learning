import numpy as np
import matplotlib.pyplot as plt

np.random.seed(80)
dist = np.array([0,0.3,0.6,0.8,1.1,1.3,1.4,1.6,1.9,2.1,2.3,2.4,2.6,3,3.6,4.1,5,7,10,12,14,14.6])
rssi = np.array([-50,-52,-58,-57,-62,-59,-63,-65,-66,-63,-64,-66,-69,-68,-70,-67,-69,-70,-73,-72,-73,-71])

print(dist.shape)
print(rssi.shape)

cur = 22
result = []
for i in range(cur):
    temp = i * 20 / cur + 1
    result.append(-49.1 - 17.51 * np.log10(temp))


# plt.figure(1)
plt.figure(figsize=(7,7))
plt.subplots_adjust(left=0.11,right=0.95,top=0.95,bottom=0.11)
ax1 = plt.subplot(1,1,1)
# ax2 = plt.subplot(2,1,2)

plt.rcParams['font.sans-serif']=['STSong'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rc('legend',**{'fontsize':15})

plt.xticks(np.arange(1, 27, 5),fontproperties = 'STSong', size = 15)
plt.yticks(np.arange(-80, -45, 5),fontproperties = 'STSong', size = 15)

plt.sca(ax1)
plt.grid()
# plt.xlim(0,25)
# plt.ylim(-80,-45)
plt.xlabel('距离/米', fontsize='x-large')
plt.ylabel('RSSI/dBm', fontsize='x-large')
# plt.title('(a)',y=-0.12)
l1, = plt.plot(np.linspace(1,26,22),rssi,'g+-', ms=10)
l2, = plt.plot(np.linspace(1,26,22),result,'r--', ms=10)
qq = plt.legend([l1,l2], ["实际RSSI采集数据","对数方程拟合数据"], loc='upper right')

plt.savefig("1_1.svg")
plt.show()
