import matplotlib.pyplot as plt
import numpy as np

levels = [0, 3, 6, 9, 12, 15, 18, 21, 24, 21, 18, 15, 12, 9, 6, 3]
d_yticks = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5]
cycles = 3
step = 0

deltas = [1000, 100, 50, 10, 5]

f, ax = plt.subplots(5, 1, figsize=(10,10))
for i, delta in enumerate(deltas):
	delta = deltas[i]
	signal = []
	duty = []
	for cycle in range(cycles):
		for level in levels:
			for j in range(delta):
				signal.append(level)
				duty.append(level / 24)

	ax[i].plot(signal, color='C0')
	ax2 = ax[i].twinx()
	ax[i].grid('on')
	ax2.plot(duty, color='C1')
	ax2.set_yticks(d_yticks)
	ax[i].legend(['Output Signal'], loc='upper left')
	ax2.legend(['Duty Cycle'], loc='lower left')
	ax[i].set_xlabel('Time (uS)')
	ax[i].set_ylabel('Voltage (V)')
	ax2.set_ylabel('Duty Cycle')
	ax[i].set_title('Delta = {} uS'.format(delta))

f.suptitle('Sample pseudo-traingular waveform with eight steps', fontweight='bold')
f.tight_layout()

plt.plot(signal)
plt.show()