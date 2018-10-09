import matplotlib.pyplot as plt

x = []
y = []

fig = plt.figure()
# rect = fig.patch
# rect.set_facecolor('#31312e')

# readFile = open('SampleData.txt','r')
# sepFile = readFile.read().split('\n')
# readFile.close()

# for plotPair in sepFile:
#     xAndY = plotPair.split(',')
#     x.append(int(xAndY[0]))
#     y.append(int(xAndY[1]))

ax1 = fig.add_subplot(2,2,1, axisbg='w')
ax1.plot(x, y, 'c', linewidth=3.3)
ax1.tick_params(axis='x', colors='k')
ax1.tick_params(axis='y', colors='k')
ax1.spines['bottom'].set_color('w')
ax1.spines['top'].set_color('w')
ax1.spines['left'].set_color('w')
ax1.spines['right'].set_color('w')
ax1.yaxis.label.set_color('k')
ax1.xaxis.label.set_color('k')
ax1.set_title('Matplotlib graph', color = 'k')
ax1.set_xlabel('x axis')
ax1.set_ylabel('y axis')

ax2 = fig.add_subplot(2,2,2, axisbg='grey')
ax2.plot(x, y, 'c', linewidth=3.3)
ax2.tick_params(axis='x', colors='c')
ax2.tick_params(axis='y', colors='c')
ax2.spines['bottom'].set_color('w')
ax2.spines['top'].set_color('w')
ax2.spines['left'].set_color('w')
ax2.spines['right'].set_color('w')
ax2.yaxis.label.set_color('c')
ax2.xaxis.label.set_color('c')
ax2.set_title('Matplotlib graph', color = 'c')
ax2.set_xlabel('x axis')
ax2.set_ylabel('y axis')

# ax3 = fig.add_subplot(2,1,2, axisbg='grey')
# ax3.plot(x, y, 'c', linewidth=3.3)
# ax3.tick_params(axis='x', colors='c')
# ax3.tick_params(axis='y', colors='c')
# ax3.spines['bottom'].set_color('w')
# ax3.spines['top'].set_color('w')
# ax3.spines['left'].set_color('w')
# ax3.spines['right'].set_color('w')
# ax3.yaxis.label.set_color('c')
# ax3.xaxis.label.set_color('c')
# ax3.set_title('Matplotlib graph', color = 'c')
# ax3.set_xlabel('x axis')
# ax3.set_ylabel('y axis')

plt.show()   