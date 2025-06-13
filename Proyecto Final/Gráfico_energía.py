import matplotlib.pyplot as plt
import numpy as np

casos = ['Caso 1', 'Caso 2', 'Caso 3']
energia_pot = [4.7589, 4.7589, 4.7589]
energia_cin = [1.1430, 1.1426, 0.9673]

x = np.arange(len(casos))
width = 0.35

fig, ax = plt.subplots()
ax.bar(x - width/2, energia_pot, width, label='Energía Potencial')
ax.bar(x + width/2, energia_cin, width, label='Energía Cinética')

ax.set_ylabel('Energía (J)')
ax.set_title('Comparación de Energías por Caso')
ax.set_xticks(x)
ax.set_xticklabels(casos)
ax.legend()

plt.show()