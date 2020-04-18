import matplotlib.pyplot as plt


X = [1,2,3,4,5,6,7,8,9,10] # X-axis
Y = [32,32,13,45,67,99,12,89,22,10] # Y-axis, your data

fig, ax = plt.subplots()
ax.plot(X, Y)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')

fig.savefig("test.png")
plt.show()
