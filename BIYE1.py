
#卡方分布——画图
#导入需要的包
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.style as style
from IPython.core.display import HTML

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

plt.plot(np.linspace(0,20,200),generate)
plt.plot(np.linspace(0,20,200),generate2,color='red') #绘制累积概率密度函数
plt.plot(np.linspace(0,20,200),generate3,color='green')

plt.show()
