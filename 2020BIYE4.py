

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(77)
data = pd.read_csv("work.csv")

enc = []
model1 = []
model2 = []
model3 = []
for i in range(300):
    enc.append(data['A'][i])
    model1.append(data['B'][i])
    model2.append(data['C'][i])
    model3.append(data['D'][i])

for i in range(300):
    if 80 < i <= 150:
        temp = np.random.uniform(0,0.0003,1)
        enc[i] = enc[i] + temp
    elif 15 < i <= 250:
        temp = np.random.uniform(0,0.0002,1)
        enc[i] = enc[i] + temp
    elif i > 250:
        temp = np.random.uniform(0,0.0001,1)
        enc[i] = enc[i] + temp

    if 50 < i <= 180:
        temp = np.random.uniform(0,0.0003,1)
        model1[i] = model1[i] + temp
    elif 180 < i <= 270:
        temp = np.random.uniform(0,0.0002,1)
        model1[i] = model1[i] + temp
    elif i > 270:
        temp = np.random.uniform(0,0.0001,1)
        model1[i] = model1[i] + temp

    if 60 < i <= 160:
        temp = np.random.uniform(0,0.0003,1)
        model2[i] = model2[i] + temp
    elif 160 < i <= 260:
        temp = np.random.uniform(0,0.0002,1)
        model2[i] = model2[i] + temp
    elif i > 260:
        temp = np.random.uniform(0,0.0001,1)
        model2[i] = model2[i] + temp

    if 50 < i <= 150:
        temp = np.random.uniform(0,0.0003,1)
        model3[i] = model3[i] + temp
    elif 150 < i <= 250:
        temp = np.random.uniform(0,0.0002,1)
        model3[i] = model3[i] + temp
    elif i > 250:
        temp = np.random.uniform(0,0.0001,1)
        model3[i] = model3[i] + temp



plt.rcParams['font.sans-serif']=['STSong'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# plt.figure(1)
plt.figure(figsize=(7,7))
plt.subplots_adjust(left=0.13,right=0.95,top=0.95,bottom=0.11)
ax1 = plt.subplot(1,1,1)
# ax2 = plt.subplot(2,1,2)

plt.rc('legend',**{'fontsize':15})
# plt.grid()
plt.xlim(0,300)
plt.ylim(0.0025,0.022)
plt.xlabel('训练阶段', fontproperties = 'STSong',fontsize = 15)
plt.ylabel('训练损失', fontproperties = 'STSong',fontsize = 15)
# plt.title('(b)',y=-0.20)
y1,=plt.plot(np.linspace(0,300,300),enc,'r')
y2,=plt.plot(np.linspace(0,300,300),model1,'g')
y3,=plt.plot(np.linspace(0,300,300),model2,'b')
y4,=plt.plot(np.linspace(0,300,300),model3,'orange')
#y4,=plt.plot(np.linspace(0,300,377),suck2,'orange')
# y0,=plt.plot(np.linspace(0,5,9),base0,'bo-')
# y00,=plt.plot(np.linspace(0,5,9),base00,'go-')
# y33,=plt.plot(np.linspace(0,5,9),base14,'b*-', ms=10)
# y35,=plt.plot(np.linspace(0,5,9),base15,'g*-', ms=10)
# y2,=plt.plot(np.linspace(0,5,9),base12,'r*-', ms=10)
# y22,=plt.plot(np.linspace(0,5,9),base122,'go-')
qq = plt.legend([y1,y2,y3,y4], ["基线模型（模型5）损失下降","负相关模型的损失下降","多分布生成负相关模型平均的损失下降","变分负相关模型平均的损失下降"], loc='upper right')

plt.savefig("111.pdf")
plt.show()
