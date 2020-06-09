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

np.random.seed(10)

base2 = np.array([0,0.375,0.869,0.949,0.979,0.988,0.9999,0.9999,0.9999])

generate2 = []

for i in range(8):
    low = base2[i]
    high = base2[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate2.append(temp[0])

generate2 = np.array(generate2)
generate2 = np.sort(generate2)

np.random.seed(20)

base3 = np.array([0,0.355,0.846,0.941,0.970,0.987,0.9999,0.9999,0.9999])

generate3 = []

for i in range(8):
    low = base3[i]
    high = base3[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate3.append(temp[0])

generate3 = np.array(generate3)
generate3 = np.sort(generate3)

'''
base12 = np.array([0,0.335,0.7815000,0.9088,0.9510,0.98787,0.9999,0.9999,0.9999])
'''
np.random.seed(40)
base13 = np.array([0,0.285,0.7415000,0.8788,0.9210,0.94787,0.9899,0.9999,0.9999])

generate13 = []

for i in range(8):
    low = base13[i]
    high = base13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate13.append(temp[0])

generate13 = np.array(generate13)
generate13 = np.sort(generate13)

base14 = np.array([0,0.245,0.7215000,0.8488,0.8910,0.92787,0.9499,0.9899,0.9999])

generate14 = []

for i in range(8):
    low = base14[i]
    high = base14[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate14.append(temp[0])

generate14 = np.array(generate14)
generate14 = np.sort(generate14)

'''
base122 = np.array([0,0.235,0.6815000,0.8088,0.8710,0.93787,0.9899,0.9999,0.9999])
'''
base199 = np.array([0,0.185,0.6015000,0.77888,0.8110,0.88787,0.9299,0.9699,0.9999])

generate199 = []

for i in range(8):
    low = base199[i]
    high = base199[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate199.append(temp[0])

generate199 = np.array(generate199)
generate199 = np.sort(generate199)

base189 = np.array([0,0.125,0.5515000,0.73888,0.7910,0.85787,0.8999,0.9499,0.9899])

generate189 = []

for i in range(8):
    low = base189[i]
    high = base189[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        generate189.append(temp[0])

generate189 = np.array(generate189)
generate189 = np.sort(generate189)

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
plt.xlabel('误差距离/米', fontsize='x-large')
plt.ylabel('累积概率', fontsize='x-large')
# plt.title('(a)',y=-0.12)
l1, = plt.plot(np.linspace(0,20,9),base1,'g+-', ms=10)
l2, = plt.plot(np.linspace(0,20,9),base2,'g*-', ms=10) #绘制累积概率密度函数
l3, = plt.plot(np.linspace(0,20,9),base3,'go-')
l4, = plt.plot(np.linspace(0,20,9),base13,'ro-')
l5, = plt.plot(np.linspace(0,20,9),base14,'r*-', ms=10)
l6, = plt.plot(np.linspace(0,20,9),base199,'bo-')
l7, = plt.plot(np.linspace(0,20,9),base189,'b*-', ms=10)
qq = plt.legend([l6,l7,l4,l5,l1,l2,l3], ["模型4(5 days):ALE=4.77m","模型4(15 days):ALE=5.03m","模型5(5 days):ALE=3.81m", "模型5(15 days):ALE=3.94m","负相关定位模型(初始):ALE=3.08m", "负相关定位模型(5 days):ALE=3.16m","负相关定位模型(15 days):ALE=3.22m"], loc='lower right')

plt.savefig("003.svg")
plt.show()
