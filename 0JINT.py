import numpy as np
import matplotlib.pyplot as plt

data1 = [-70,-61,-67,-67,-72,-72,-73,-71,-67,-68,-70,-70,-68,-61,-70,-70,-71,-68,-71,-69,-65,-71,-70,-67]
data2 = [-66,-68,-65,-67,-68,-65,-66,-67,-65,-63,-63,-64,-68,-61,-58,-64,-65,-65,-65,-59,-65,-64,-64,-67]

dataq = [-72,-68,-65,-65,-71,-64,-64,-68,-69,-65,-71,-71,-69,-60,-66,-68,-69,-65,-66,-70,-64,-70,-70,-69,-70,-70]
plt.figure(figsize=(10,5))
plt.subplots_adjust(left=0.10,right=0.95,top=0.95,bottom=0.15)
ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)

bins = 2
group1 = int((max(data1) - min(data1)) / bins)
group2 = int((max(data2) - min(data2)) / bins)
groupq = int((max(dataq) - min(dataq)) / bins)

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.sca(ax1)
plt.grid()
plt.hist(data1, group1,normed=1, alpha=0.7,label='二月1号')
rects2 = plt.hist(dataq, groupq,normed=1, alpha=0.7,label='二月15号')
plt.xlabel('RSSI/dB')
plt.ylabel('概率分布')
plt.legend()
plt.title('(a)',y=-0.17)

plt.sca(ax2)
plt.grid()
rects1 = plt.hist(data1, group1,normed=1, alpha=0.7,label='二月15号')
rects2 = plt.hist(data2, group2,normed=1, alpha=0.7,label='三月30号')
plt.xlabel('RSSI/dB')
plt.ylabel('概率分布')
plt.title('(b)',y=-0.17)
plt.legend()

plt.show()
