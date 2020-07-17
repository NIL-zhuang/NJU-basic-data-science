import matplotlib.pyplot as plt
import numpy as np


labels = ['string', 'list', 'array', 'search-algorithm', 'tree', 'graph', 'numeric-operation', 'sort-algorithm']
ax1 = plt.subplot(projection='polar')

theta = np.linspace(0, 2 * np.pi, 8, endpoint=False)
theta = np.append(theta, theta[0])

player = {
    'M': np.random.randint(size=8, low=60, high=90),
}

player['M'] = np.append(player['M'], player['M'][0])
ax1.plot(theta, player['M'], 'b')
ax1.fill(theta, player['M'], 'b', alpha=0.5)
ax1.set_xticks(theta)  # 分成8等分
ax1.set_xticklabels(labels, y=0.01)
ax1.set_title('abilities', color='b', size=20)
ax1.set_yticks([20, 40, 60, 80, 100])
plt.show()