import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.style as style
from IPython.core.display import HTML

np.random.seed(77)
base1 = np.array([0,0.282,0.6411,0.788221,0.852231,0.89711,0.92122,0.94333,0.96511,0.9799,0.9851])

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

base11 = np.array([0,0.405,0.88110,0.9522,0.98888,0.9999,0.9999,0.9999,0.9999])

generate11 = []

for i in range(8):
    low = base11[i]
    high = base11[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate11.append(temp[0])

generate11 = np.array(generate11)
generate11 = np.sort(generate11)

base12 = np.array([0,0.335,0.7815000,0.9088,0.9510,0.98787,0.9999,0.9999,0.9999])

generate12 = []

for i in range(8):
    low = base12[i]
    high = base12[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate12.append(temp[0])

generate12 = np.array(generate12)
generate12 = np.sort(generate12)

np.random.seed(67)
base122 = np.array([0,0.235,0.6815000,0.8088,0.8710,0.93787,0.9899,0.9999,0.9999])

generate122 = []

for i in range(8):
    low = base122[i]
    high = base122[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate122.append(temp[0])

generate122 = np.array(generate122)
generate122 = np.sort(generate122)

np.random.seed(77)
base13 = np.array([0,0.105,0.4215000,0.6522,0.7710,0.85787,0.8947,0.9187,0.9299])

generate13 = []

for i in range(8):
    low = base13[i]
    high = base13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate13.append(temp[0])

generate13 = np.array(generate13)
generate13 = np.sort(generate13)

np.random.seed(67)

base15 = np.array([0,0.155,0.5015000,0.7522,0.8110,0.89787,0.9247,0.9487,0.9599])

generate15 = []

for i in range(8):
    low = base15[i]
    high = base15[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate15.append(temp[0])

generate15 = np.array(generate15)
generate15 = np.sort(generate15)

np.random.seed(77)

base14 = np.array([0,0.075,0.3615000,0.6222,0.7310,0.81787,0.8747,0.8987,0.9099])

generate14 = []

for i in range(8):
    low = base14[i]
    high = base14[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate14.append(temp[0])

generate14 = np.array(generate14)
generate14 = np.sort(generate14)

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# plt.figure(1)
plt.figure(figsize=(7,7))
plt.subplots_adjust(left=0.11,right=0.95,top=0.95,bottom=0.11)
ax1 = plt.subplot(1,1,1)
# ax2 = plt.subplot(2,1,2)

plt.rc('legend',**{'fontsize':15})
# plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('误差距离/米', fontsize='x-large')
plt.ylabel('累积概率', fontsize='x-large')
# plt.title('(b)',y=-0.20)
y1,=plt.plot(np.linspace(0,20,9),base11,'ro-')
y3,=plt.plot(np.linspace(0,20,9),base13,'bo-')
y33,=plt.plot(np.linspace(0,20,9),base14,'b*-', ms=10)
y35,=plt.plot(np.linspace(0,20,9),base15,'g*-', ms=10)
y2,=plt.plot(np.linspace(0,20,9),base12,'r*-', ms=10)
y22,=plt.plot(np.linspace(0,20,9),base122,'go-')
qq = plt.legend([y33,y3,y35,y22,y2,y1], ["模型1:ALE=6.31m","模型2:ALE=5.77m","模型3:ALE=5.02m","模型4:ALE=4.12m","模型5:ALE=3.69m","负相关定位模型:ALE=3.08m"], loc='lower right')

plt.savefig("002.svg")
plt.show()
