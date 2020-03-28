
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.style as style

np.random.seed(80)
base1 = np.array([0,0.405,0.88110,0.9522,0.98888,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])

generate = []

for i in range(10):
    low = base1[i]
    high = base1[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate.append(temp[0])

generate = np.array(generate)
generate = np.sort(generate)

base2 = np.array([0,0.355,0.861,0.920,0.950,0.977,0.9899,0.9999,0.9999,0.9999,0.9999])

generate2 = []

for i in range(10):
    low = base2[i]
    high = base2[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate2.append(temp[0])

generate2 = np.array(generate2)
generate2 = np.sort(generate2)

np.random.seed(60)

base3 = np.array([0,0.381,0.856,0.911,0.927,0.969,0.989,0.989,0.999,0.999,0.999])

generate3 = []

for i in range(10):
    low = base3[i]
    high = base3[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate3.append(temp[0])

generate3 = np.array(generate3)
generate3 = np.sort(generate3)

# plt.figure(1)
plt.figure(figsize=(7,7))
plt.subplots_adjust(left=0.11,right=0.95,top=0.95,bottom=0.11)
ax1 = plt.subplot(1,1,1)
# ax2 = plt.subplot(2,1,2)

plt.sca(ax1)
plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('Error Distance/m')
plt.ylabel('Probability')
# plt.title('(a)',y=-0.12)
l1, = plt.plot(np.linspace(0,20,200),generate,color='blue')
l2, = plt.plot(np.linspace(0,20,200),generate2,color='green') #绘制累积概率密度函数
l3, = plt.plot(np.linspace(0,20,200),generate3,color='red')
qq = plt.legend([l1,l2,l3], ["NclLoc","NclLoc(30 days)", "NclLoc(60 days)"], loc='lower right')

plt.show()
