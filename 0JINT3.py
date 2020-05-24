import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.style as style

np.random.seed(80)
base1 = np.array([0,0.405,0.88110,0.9522,0.98888,0.9999,0.9999,0.9999,0.9999])

generate = []

for i in range(8):
    low = base1[i]
    high = base1[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate.append(temp[0])

generate = np.array(generate)
generate = np.sort(generate)

base2 = np.array([0,0.355,0.861,0.920,0.950,0.977,0.9899,0.9999,0.9999])

generate2 = []

for i in range(8):
    low = base2[i]
    high = base2[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate2.append(temp[0])

generate2 = np.array(generate2)
generate2 = np.sort(generate2)

np.random.seed(60)

base3 = np.array([0,0.381,0.856,0.911,0.927,0.969,0.989,0.989,0.999])

generate3 = []

for i in range(8):
    low = base3[i]
    high = base3[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate3.append(temp[0])

generate3 = np.array(generate3)
generate3 = np.sort(generate3)

base13 = np.array([0,0.125,0.5915000,0.7788,0.8710,0.91787,0.9399,0.9599,0.9799])

generate13 = []

for i in range(8):
    low = base13[i]
    high = base13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate13.append(temp[0])

generate13 = np.array(generate13)
generate13 = np.sort(generate13)

base14 = np.array([0,0.105,0.5215000,0.7388,0.8310,0.89787,0.9199,0.9399,0.9699])

generate14 = []

for i in range(8):
    low = base14[i]
    high = base14[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate14.append(temp[0])

generate14 = np.array(generate14)
generate14 = np.sort(generate14)

# plt.figure(1)
plt.figure(figsize=(7,7))
plt.subplots_adjust(left=0.11,right=0.95,top=0.95,bottom=0.11)
ax1 = plt.subplot(1,1,1)
# ax2 = plt.subplot(2,1,2)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

plt.rc('legend',**{'fontsize':15})
plt.sca(ax1)
plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('误差距离/米')
plt.ylabel('累积概率')
# plt.title('(a)',y=-0.12)
l1, = plt.plot(np.linspace(0,20,160),generate,color='blue')
l2, = plt.plot(np.linspace(0,20,160),generate2,color='green') #绘制累积概率密度函数
l3, = plt.plot(np.linspace(0,20,160),generate3,color='red')
l4, = plt.plot(np.linspace(0,20,160),generate13,color='chocolate')
l5, = plt.plot(np.linspace(0,20,160),generate14,color='darkgray')
qq = plt.legend([l3,l4,l5,l1,l2], ["模型5(30 days):ALE=4.45m", "模型5(60 days):ALE=5.03m","负相关定位模型(初始):ALE=3.08m","负相关定位模型(30 days):ALE=3.55m", "负相关定位模型(60 days):ALE=3.87m"], loc='lower right')

plt.show()
