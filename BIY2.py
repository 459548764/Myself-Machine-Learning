
#卡方分布——画图
#导入需要的包
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.style as style
from IPython.core.display import HTML

np.random.seed(77)
base1 = np.array([0,0.232,0.5311,0.718221,0.802231,0.88711,0.91122,0.93333,0.94511,0.9699,0.9751])

generate = []

for i in range(10):
    low = base1[i]
    high = base1[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate.append(temp[0])

generate = np.array(generate)
generate = np.sort(generate)

base2 = np.array([0,0.092,0.221,0.355,0.521,0.65554,0.722153,0.7554,0.82345,0.83999,0.860000])

generate2 = []

for i in range(10):
    low = base2[i]
    high = base2[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate2.append(temp[0])

generate2 = np.array(generate2)
generate2 = np.sort(generate2)

base3 = np.array([0,0.191,0.457,0.650,0.764,0.82241,0.8674,0.9015,0.9222,0.94100,0.9555])

generate3 = []

for i in range(10):
    low = base3[i]
    high = base3[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate3.append(temp[0])

generate3 = np.array(generate3)
generate3 = np.sort(generate3)

base11 = np.array([0,0.255,0.75110,0.9322,0.97788,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])

generate11 = []

for i in range(10):
    low = base11[i]
    high = base11[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate11.append(temp[0])

generate11 = np.array(generate11)
generate11 = np.sort(generate11)

base12 = np.array([0,0.195,0.7015000,0.8688,0.9410,0.98787,0.9999,0.9999,0.9999,0.9999,0.9999])

generate12 = []

for i in range(10):
    low = base12[i]
    high = base12[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate12.append(temp[0])

generate12 = np.array(generate12)
generate12 = np.sort(generate12)

base13 = np.array([0,0.105,0.4215000,0.6522,0.7710,0.85787,0.8947,0.9187,0.9299,0.9299,0.9399])

generate13 = []

for i in range(10):
    low = base13[i]
    high = base13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate13.append(temp[0])

generate13 = np.array(generate13)
generate13 = np.sort(generate13)

# plt.figure(1)
plt.figure(figsize=(10,5))
plt.subplots_adjust(left=0.07,right=0.95,top=0.95,bottom=0.15)
ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)

plt.sca(ax1)
plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('Error Distance/m')
plt.ylabel('Probability')
plt.title('(a)',y=-0.17)
l1, = plt.plot(np.linspace(0,20,200),generate)
l2, = plt.plot(np.linspace(0,20,200),generate2,color='green') #绘制累积概率密度函数
l3, = plt.plot(np.linspace(0,20,200),generate3,color='red')
qq = plt.legend([l1,l2,l3], ["Proposed","Only MLP", "MLP+AE"], loc='lower right')

plt.sca(ax2)
plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('Error Distance/m')
plt.ylabel('Probability')
plt.title('(b)',y=-0.17)
y1,=plt.plot(np.linspace(0,20,200),generate11)
y3,=plt.plot(np.linspace(0,20,200),generate13,color='green')
y2,=plt.plot(np.linspace(0,20,200),generate12,color='red')
qq = plt.legend([y1,y3,y2], ["Proposed","Only MLP", "MLP+AE"], loc='lower right')

plt.show()
