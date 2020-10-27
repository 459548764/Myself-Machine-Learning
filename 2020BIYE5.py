import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.style as style

#--------------------------------------------------
np.random.seed(70)

base5 = np.array([0,0.411,0.856,0.901,0.947,0.989,0.989,0.999,0.999])

generate5 = []

for i in range(8):
    low = base5[i]
    high = base5[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate5.append(temp[0])

generate5 = np.array(generate5)
generate5 = np.sort(generate5)

base4 = np.array([0,0.302,0.812,0.881,0.917,0.939,0.979,0.999,0.999])

generate4 = []

for i in range(8):
    low = base4[i]
    high = base4[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate4.append(temp[0])

generate4 = np.array(generate4)
generate4 = np.sort(generate4)

np.random.seed(60)

base3 = np.array([0,0.381,0.846,0.901,0.927,0.969,0.989,0.989,0.999])  #######################

generate3 = []

for i in range(8):
    low = base3[i]
    high = base3[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate3.append(temp[0])

generate3 = np.array(generate3)
generate3 = np.sort(generate3)

base2 = np.array([0,0.321,0.796,0.881,0.901,0.935,0.969,0.989,0.999])   #20%

generate2 = []

for i in range(8):
    low = base2[i]
    high = base2[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate2.append(temp[0])

generate2 = np.array(generate2)
generate2 = np.sort(generate2)

base1 = np.array([0,0.281,0.756,0.856,0.890,0.921,0.949,0.969,0.999])    #0%

generate1 = []

for i in range(8):
    low = base1[i]
    high = base1[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate1.append(temp[0])

generate1 = np.array(generate1)
generate1 = np.sort(generate1)

plt.rcParams['font.sans-serif']=['STSong'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# plt.figure(1)
plt.figure(figsize=(7,7))
plt.subplots_adjust(left=0.11,right=0.95,top=0.95,bottom=0.11)
ax1 = plt.subplot(1,1,1)
# ax2 = plt.subplot(2,1,2)
plt.rc('legend',**{'fontsize':15})
plt.sca(ax1)
#plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('误差距离/米', fontproperties = 'STSong',fontsize = 15)
plt.ylabel('累积概率', fontproperties = 'STSong',fontsize = 15)
# plt.title('(a)',y=-0.12)
#l00, = plt.plot(np.linspace(0,20,9),base5,'ro-')
l0, = plt.plot(np.linspace(0,20,9),base4,'bo-')
l1, = plt.plot(np.linspace(0,20,9),base3,'go-')
l2, = plt.plot(np.linspace(0,20,9),base2,'r*-', ms=10) #绘制累积概率密度函数
l3, = plt.plot(np.linspace(0,20,9),base1,'g*-', ms=10)
qq = plt.legend([l0,l1,l2,l3], ["负相关定位系统(p=60%):ALE=0.80m",
                                "负相关定位系统(p=40%):ALE=0.77m",
                                "负相关定位系统(p=20%):ALE=0.81m",
                                "负相关定位系统(p=0%):ALE=0.85m"], loc='lower right')
plt.savefig("test2.pdf")
plt.show()
