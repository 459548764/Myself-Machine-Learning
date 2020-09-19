import numpy as np
import matplotlib.pyplot as plt

np.random.seed(80)
dist = np.array([0,0.3,0.6,0.8,1.1,1.3,1.4,1.6,1.9,2.1,2.3,2.4,2.6,3,3.6,4.1,5,7,10,12,14,14.6])
rssi = np.array([-55,-55,-55,-54,-53,-53,-52,-56,-56,-57,-57,-54,-70,-56,-53,-55,-56,-55,-59,-54,-72,-53,-54,-56,-54,-54,-55,-55,-53,-57,-52,-53,-53,-54,-54,-55,-55,-55,-55,-54,-53,-53,-52,-56,-56,-57,-57,-54,-55,-54,-54,-53,-53,-52,-57,-53,-55,-55,-54,-54])

print(rssi[::-1])

print(dist.shape)
print(rssi.shape)

cur = 36

resu = np.array([-55,-55,-55,-54,-54,-54,-53,-54,-54,-56,-57,-55,-55,-56,-54,-54,-55,-55,-56,-54,-56,-54,-54,-55,-56,-55,-55,-55,-54,-55,-53,-53,-53,-53,-54,-54,-55,-55,-55,-55,-54,-54,-55,-55,-56,-56,-56,-55,-55,-54,-54,-54,-53,-53,-54,-55,-55,-55,-55,-55])
print(resu[::-1])


# plt.figure(1)
plt.figure(figsize=(7,7))
plt.subplots_adjust(left=0.11,right=0.95,top=0.95,bottom=0.11)
ax1 = plt.subplot(1,1,1)
# ax2 = plt.subplot(2,1,2)

plt.rcParams['font.sans-serif']=['STSong'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rc('legend',**{'fontsize':15})

plt.xticks(np.arange(0, 61, 5),fontproperties = 'STSong', size = 15)
plt.yticks(np.arange(-70, -35, 5),fontproperties = 'STSong', size = 15)

plt.sca(ax1)
#plt.grid()
# plt.xlim(0,25)
# plt.ylim(-80,-45)
plt.xlabel('采集时间/秒', fontsize='x-large')
plt.ylabel('RSSI/dBm', fontsize='x-large')
# plt.title('(a)',y=-0.12)
l1, = plt.plot(np.linspace(0,60,60),rssi,'g--', ms=10)
l2, = plt.plot(np.linspace(0,60,60),resu,'r--', ms=10)
qq = plt.legend([l1,l2], ["实际RSSI采集数据","卡尔曼滤波之后RSSI数据"], loc='lower right')

plt.savefig("1_1.svg")
plt.show()
