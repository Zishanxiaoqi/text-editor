#帮我绘制一个二次函数图像，并给出其表达式。
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-5, 5, 100)
y = x**2

plt.plot(x, y)
plt.show()

# 二次函数表达式：y = x^2   