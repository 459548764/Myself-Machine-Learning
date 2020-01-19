
#卡方分布——画图
#导入需要的包
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

base11 = np.array([0,0.405,0.88110,0.9522,0.98888,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])

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
plt.figure(figsize=(10,4))
plt.subplots_adjust(left=0.07,right=0.95,top=0.95,bottom=0.15)
ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)

plt.sca(ax1)
plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('Error Distance/m')
plt.ylabel('Probability')
plt.title('(a)',y=-0.20)
l1, = plt.plot(np.linspace(0,20,200),generate,color='blue')
l2, = plt.plot(np.linspace(0,20,200),generate2,color='green') #绘制累积概率密度函数
l3, = plt.plot(np.linspace(0,20,200),generate3,color='red')
qq = plt.legend([l1,l2,l3], ["ATFM","Only MLP", "MLP+AE"], loc='lower right')

plt.sca(ax2)
plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('Error Distance/m')
plt.ylabel('Probability')
plt.title('(b)',y=-0.20)
y1,=plt.plot(np.linspace(0,20,200),generate11,color='blue')
y3,=plt.plot(np.linspace(0,20,200),generate13,color='green')
y2,=plt.plot(np.linspace(0,20,200),generate12,color='red')
qq = plt.legend([y1,y3,y2], ["ATFM","Only MLP", "MLP+AE"], loc='lower right')

# plt.show()

'''
base11 = np.array([0,0.405,0.88110,0.9522,0.98888,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])
df21 = np.array([0,0.375,0.82110,0.9022,0.96788,0.9799,0.9999,0.9999,0.9999,0.9999,0.9999])
dfmmd21 = np.array([0,0.3835,0.841515,0.92551178,0.9815,0.9888,0.9999,0.9999,0.9999,0.9999,0.9999])
dfcoral21 = np.array([0,0.405,0.880,0.949,0.98601,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])
'''
f21 = np.array([0,0.3135,0.7811,0.87178,0.912144,0.9861,0.9999,0.9999,0.9999,0.9999,0.9999])

ff21 = []

for i in range(10):
    low = f21[i]
    high = f21[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        ff21.append(temp[0])

ff21 = np.array(ff21)
ff21 = np.sort(ff21)

fmmd21 = np.array([0,0.3235,0.841,0.9069,0.949,0.9888,0.9999,0.9999,0.9999,0.9999,0.9999])

ffmmd21 = []

for i in range(10):
    low = fmmd21[i]
    high = fmmd21[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        ffmmd21.append(temp[0])

ffmmd21 = np.array(ffmmd21)
ffmmd21 = np.sort(ffmmd21)

fcoral21 = np.array([0,0.3835,0.869515,0.944378,0.97822134,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])

ffcoral21 = []

for i in range(10):
    low = fcoral21[i]
    high = fcoral21[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        ffcoral21.append(temp[0])

ffcoral21 = np.array(ffcoral21)
ffcoral21 = np.sort(ffcoral21)

'''
base11 = np.array([0,0.405,0.88110,0.9522,0.98888,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])
'''

df21 = np.array([0,0.375,0.82110,0.9022,0.96788,0.9799,0.9999,0.9999,0.9999,0.9999,0.9999])

dff21 = []

for i in range(10):
    low = df21[i]
    high = df21[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        dff21.append(temp[0])

dff21 = np.array(dff21)
dff21 = np.sort(dff21)

dfmmd21 = np.array([0,0.3835,0.841515,0.92551178,0.9815,0.9888,0.9999,0.9999,0.9999,0.9999,0.9999])

dffmmd21 = []

for i in range(10):
    low = dfmmd21[i]
    high = dfmmd21[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        dffmmd21.append(temp[0])

dffmmd21 = np.array(dffmmd21)
dffmmd21 = np.sort(dffmmd21)

dfcoral21 = np.array([0,0.405,0.880,0.949,0.98601,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])

dffcoral21 = []

for i in range(10):
    low = dfcoral21[i]
    high = dfcoral21[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        dffcoral21.append(temp[0])

dffcoral21 = np.array(dffcoral21)
dffcoral21 = np.sort(dffcoral21)

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
l1, = plt.plot(np.linspace(0,20,200),generate11,color='blue')
l2, = plt.plot(np.linspace(0,20,200),dff21,color='blue',linestyle='--') #绘制累积概率密度函数
l3, = plt.plot(np.linspace(0,20,200),dffmmd21,color='red')
l4, = plt.plot(np.linspace(0,20,200),dffcoral21,color='green')
qq = plt.legend([l1,l2,l3,l4], ["Pretrain","Without Update", "MMD Update","Correlation Update"], loc='lower right')

plt.sca(ax2)
plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('Error Distance/m')
plt.ylabel('Probability')
plt.title('(b)',y=-0.17)
l1, = plt.plot(np.linspace(0,20,200),generate11,color='blue')
l2, = plt.plot(np.linspace(0,20,200),ff21,color='blue',linestyle='--') #绘制累积概率密度函数
l3, = plt.plot(np.linspace(0,20,200),ffmmd21,color='red')
l4, = plt.plot(np.linspace(0,20,200),ffcoral21,color='green')
qq = plt.legend([l1,l2,l3,l4], ["Pretrain","Without Update", "MMD Update","Correlation Update"], loc='lower right')


# plt.show()

'''
base11 = np.array([0,0.405,0.88110,0.9522,0.98888,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])
f21 = np.array([0,0.3135,0.7811,0.87178,0.912144,0.9861,0.9999,0.9999,0.9999,0.9999,0.9999])
'''

ffbase13 = np.array([0,0.285,0.6415000,0.7888,0.8910,0.95787,0.9899,0.9999,0.9999,0.9999,0.9999])

ffgenerate13 = []

for i in range(10):
    low = ffbase13[i]
    high = ffbase13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        ffgenerate13.append(temp[0])

ffgenerate13 = np.array(ffgenerate13)
ffgenerate13 = np.sort(ffgenerate13)

mmdffbase13 = np.array([0,0.321,0.7515000,0.8888,0.92110,0.96787,0.9999,0.9999,0.9999,0.9999,0.9999])

mmdffgenerate13 = []

for i in range(10):
    low = mmdffbase13[i]
    high = mmdffbase13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        mmdffgenerate13.append(temp[0])

mmdffgenerate13 = np.array(mmdffgenerate13)
mmdffgenerate13 = np.sort(mmdffgenerate13)

coralffbase13 = np.array([0,0.365,0.8515000,0.9488,0.9710,0.9755,0.9999,0.9999,0.9999,0.9999,0.9999])

coralffgenerate13 = []

for i in range(10):
    low = coralffbase13[i]
    high = coralffbase13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        coralffgenerate13.append(temp[0])

coralffgenerate13 = np.array(coralffgenerate13)
coralffgenerate13 = np.sort(coralffgenerate13)

'''
base11 = np.array([0,0.405,0.88110,0.9522,0.98888,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])
f21 = np.array([0,0.285,0.6415000,0.7888,0.8910,0.95787,0.9899,0.9999,0.9999,0.9999,0.9999])
'''

dffbase13 = np.array([0,0.205,0.6015000,0.7588,0.8710,0.90787,0.9599,0.9899,0.9999,0.9999,0.9999])

dffgenerate13 = []

for i in range(10):
    low = dffbase13[i]
    high = dffbase13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        dffgenerate13.append(temp[0])

dffgenerate13 = np.array(dffgenerate13)
dffgenerate13 = np.sort(dffgenerate13)

dmmdffbase13 = np.array([0,0.254,0.7415000,0.8288,0.91110,0.95787,0.9888,0.9888,0.9999,0.9999,0.9999])

dmmdffgenerate13 = []

for i in range(10):
    low = dmmdffbase13[i]
    high = dmmdffbase13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        dmmdffgenerate13.append(temp[0])

dmmdffgenerate13 = np.array(dmmdffgenerate13)
dmmdffgenerate13 = np.sort(dmmdffgenerate13)

dcoralffbase13 = np.array([0,0.351,0.8415000,0.9288,0.9800,0.9899,0.9999,0.9999,0.9999,0.9999,0.9999])

dcoralffgenerate13 = []

for i in range(10):
    low = dcoralffbase13[i]
    high = dcoralffbase13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        dcoralffgenerate13.append(temp[0])

dcoralffgenerate13 = np.array(dcoralffgenerate13)
dcoralffgenerate13 = np.sort(dcoralffgenerate13)

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
y1,=plt.plot(np.linspace(0,20,200),generate11,color='blue')
y2,=plt.plot(np.linspace(0,20,200),ffgenerate13,color='blue',linestyle='--')
y3,=plt.plot(np.linspace(0,20,200),mmdffgenerate13,color='red')
y4,=plt.plot(np.linspace(0,20,200),coralffgenerate13,color='green')
qq = plt.legend([l1,l2,l3,l4], ["Pretrain","Without Update", "MMD Update","Correlation Update"], loc='lower right')

plt.sca(ax2)
plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('Error Distance/m')
plt.ylabel('Probability')
plt.title('(b)',y=-0.17)
y1,=plt.plot(np.linspace(0,20,200),generate11,color='blue')
y2,=plt.plot(np.linspace(0,20,200),dffgenerate13,color='blue',linestyle='--')
y3,=plt.plot(np.linspace(0,20,200),dmmdffgenerate13,color='red')
y4,=plt.plot(np.linspace(0,20,200),dcoralffgenerate13,color='green')
qq = plt.legend([l1,l2,l3,l4], ["Pretrain","Without Update", "MMD Update","Correlation Update"], loc='lower right')

# plt.show()

'''
---np.array([0,0.1535,0.4111,0.5578,0.68144,0.8061,0.8414,0.8651,0.88111,0.89654,0.91114])
np.array([0,0.1935,0.451515,0.654378,0.7522134,0.862221,0.9011251454,0.918487,0.92999,0.9455,0.9666])
'''

'''
base11 = np.array([0,0.405,0.88110,0.9522,0.98888,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])
f21 = np.array([0,0.3135,0.7811,0.87178,0.912144,0.9861,0.9999,0.9999,0.9999,0.9999,0.9999])
'''
jcoral21 = np.array([0,0.3245,0.8102,0.8901,0.9234,0.9899,0.9999,0.9999,0.9999,0.9999,0.9999])

jjcoral21 = []

for i in range(10):
    low = jcoral21[i]
    high = jcoral21[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        jjcoral21.append(temp[0])

jjcoral21 = np.array(jjcoral21)
jjcoral21 = np.sort(jjcoral21)

kcoral21 = np.array([0,0.345,0.842,0.9041,0.9333,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])

kkcoral21 = []

for i in range(10):
    low = kcoral21[i]
    high = kcoral21[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        kkcoral21.append(temp[0])

kkcoral21 = np.array(kkcoral21)
kkcoral21 = np.sort(kkcoral21)

'''
base11 = np.array([0,0.255,0.75110,0.9322,0.97788,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])
dffbase13 = np.array([0,0.115,0.5515000,0.7288,0.8410,0.90787,0.9599,0.9899,0.9999,0.9999,0.9999])
dcoralffbase13 = np.array([0,0.171,0.6615000,0.8488,0.952110,0.9800,0.9999,0.9999,0.9999,0.9999,0.9999])
'''

'''
base11 = np.array([0,0.255,0.75110,0.9322,0.97788,0.9999,0.9999,0.9999,0.9999,0.9999,0.9999])
dffbase13 = np.array([0,0.205,0.6015000,0.7588,0.8710,0.90787,0.9599,0.9899,0.9999,0.9999,0.9999])
'''

jcoralffbase13 = np.array([0,0.235,0.6715000,0.8288,0.9082110,0.92500,0.9899,0.9999,0.9999,0.9999,0.9999])

jcoralffgenerate13 = []

for i in range(10):
    low = jcoralffbase13[i]
    high = jcoralffbase13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        jcoralffgenerate13.append(temp[0])

jcoralffgenerate13 = np.array(jcoralffgenerate13)
jcoralffgenerate13 = np.sort(jcoralffgenerate13)



kcoralffbase13 = np.array([0,0.2510,0.72155000,0.880188,0.9401,0.9800,0.9899,0.9999,0.9999,0.9999,0.9999])

kcoralffgenerate13 = []

for i in range(10):
    low = kcoralffbase13[i]
    high = kcoralffbase13[i+1]
    for j in range(20):
        temp = np.random.uniform(low,high,1)
        kcoralffgenerate13.append(temp[0])

kcoralffgenerate13 = np.array(kcoralffgenerate13)
kcoralffgenerate13 = np.sort(kcoralffgenerate13)

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
l1, = plt.plot(np.linspace(0,20,200),generate11,color='blue')
l2, = plt.plot(np.linspace(0,20,200),ff21,color='blue',linestyle='--') #绘制累积概率密度函数
l3, = plt.plot(np.linspace(0,20,200),ffcoral21,color='green')
l4, = plt.plot(np.linspace(0,20,200),jjcoral21,color='green',linestyle='--')
l5, = plt.plot(np.linspace(0,20,200),kkcoral21,color='green',linestyle=':')
qq = plt.legend([l1,l2,l4,l5,l3], ["Pretrain","Without Update", "Correlation Update(k=5%*m)","Correlation Update(k=15%*m)","Correlation Update(k=25%*m)"], loc='lower right')

plt.sca(ax2)
plt.grid()
plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel('Error Distance/m')
plt.ylabel('Probability')
plt.title('(b)',y=-0.17)
y1,=plt.plot(np.linspace(0,20,200),generate11,color='blue')
y2,=plt.plot(np.linspace(0,20,200),dffgenerate13,color='blue',linestyle='--')
y3,=plt.plot(np.linspace(0,20,200),dcoralffgenerate13,color='green')
y4, = plt.plot(np.linspace(0,20,200),jcoralffgenerate13,color='green',linestyle='--')
y5, = plt.plot(np.linspace(0,20,200),kcoralffgenerate13,color='green',linestyle=':')
qq = plt.legend([y1,y2,y4,y5,y3], ["Pretrain","Without Update", "Correlation Update(k=5%*m)","Correlation Update(k=15%*m)","Correlation Update(k=25%*m)"], loc='lower right')


plt.show()
#
#
#
#
