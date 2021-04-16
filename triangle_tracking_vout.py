#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, peak_widths

header_rows = 11

deltas = [1000, 100, 50, 10]

def generate_sample_signal(delta, t):
	levels = [0, 3, 6, 9, 12, 15, 18, 21, 24, 21, 18, 15, 12, 9, 6, 3]
	signal = np.array([])
	
	dt = t[len(t)-1] - t[0]

	pts_per_delta = int(dt / (delta*1E-6))
	
	cycles = dt / (15*delta)

	iterations = int(len(t) / len(levels))
	for j in range(iterations):
		print('{}'.format(j))
		for level in levels:
			signal = np.append(signal, level*np.ones(pts_per_delta))

	print(len(signal))
	return signal
	
# From https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def calculate_rise_time(vout,t):
	vout_r = vout.rolling(window=100).mean()
	rise_times = []
	levels = [3*i for i in range(9)]
	for i in range(len(levels)-1):
		highs = np.where(np.diff(np.sign(vout_r-levels[i+1])))[0]
		highs = highs[highs > 100]
		lows = np.where(np.diff(np.sign(vout_r-levels[i])))[0]
		lows = lows[lows > 100]
		min_pair = (2*len(vout), -2*len(vout))
		for high in highs:
			low = find_nearest(array=lows, value=high)
			if np.abs(high-low) < np.abs(min_pair[0]-min_pair[1]):
				min_pair = (high,low)
		rise_times.append(np.abs(t[min_pair[0]]-t[min_pair[1]]))
	return rise_times

# Assume Vout in ['CH1'], vsw1 in ['CH2'], vsw2 in ['CH3'], isw1 in ['CH5'], isw2 in ['CH6']
def plot_vout(df, coupling, delta, ax):

	base = 100000
	lim = int(len(df['TIME']) / (deltas.index(delta) + 1))
	t = df['TIME']
	vout = df['CH1']

	try:
		rise_times = calculate_rise_time(vout,t)
	except Exception as e:
		rise_times = None

	vout = vout[:lim]
	t = t[:lim]
	
	# vsw1 = df['CH2'].rolling(window=1000).mean()[:lim]
	# vsw2 = df['CH3'].rolling(window=1000).mean()[:lim]
	# i1 = df['CH5'].rolling(window=100).mean()[:lim]
	# i2 = df['CH6'].rolling(window=100).mean()[:lim]

	col = (0 if coupling == 'Uncoupled' else 1)

	# ax[col].plot(t, vout_r)
	# sample_signal = generate_sample_signal(delta, t)

	# Vout
	ax[col].grid('on')
	ax[col].plot(t, vout)
	# ax[col].plot(t, sample_signal)
	# ax[col].set_title('Vout, delta = {} uS'.format(delta))
	if col == 0:
		ax[col].set_ylabel('Delta = {} uS\n\nVoltage (V)'.format(2*delta))
	else:
		ax[col].set_ylabel('Voltage (V)')
	if delta == 10:
		ax[col].set_xlabel('Time (s)')
	if delta == 1000:
		ax[col].set_title('{}\n'.format(coupling), fontweight='bold')
	# for i in range(25):
	# 	ax[col].axhline(i, linestyle='dashed')
	ax[col].axhline(24, linestyle='dashed', color='C2')
	ax[col].axhline(0, linestyle='dashed', color='C3')
	# ax.legend('Vout')

	# # Switch node voltages
	# ax[1].grid('on')
	# ax[1].plot(t, vsw1)
	# ax[1].plot(t, vsw2)
	# ax[1].set_ylabel('Voltage (V)')
	# ax[1].set_title('Switch node voltages, {}'.format(coupling))
	# ax[1].legend(['Vsw1', 'Vsw2'])

	# # Currents
	# ax[2].grid('on')
	# ax[2].plot(t, i1)
	# ax[2].plot(t, i2)
	# ax[2].set_title('Inductor currents, {}'.format(coupling))
	# ax[2].set_xlabel('Time (s)')
	# ax[2].set_ylabel('Current (A)')
	# ax[2].legend(['I1', 'I2'])
	return rise_times

# def plot_vcap(df, coupling, delta):


def main():

	f, ax = plt.subplots(4, 2, figsize=(12,8))
	coupled_rise_times = []
	uncoupled_rise_times = []
	# i = 0
	# delta = 1000
	# if i == 0:
	for i, delta in enumerate(deltas):
	
		path_u_vout = 'triangle_tracking_uncoupled/vout_u_{}_ALL.csv'.format(delta)
		path_c_vout = 'triangle_tracking_coupled/vout_c_{}_ALL.csv'.format(delta)
		df_u_vout = pd.read_csv(path_u_vout, skiprows=header_rows)
		df_c_vout = pd.read_csv(path_c_vout, skiprows=header_rows)

		rise_times = plot_vout(df_u_vout, 'Uncoupled', delta, ax[i])
		if rise_times:
			for t in rise_times:
				uncoupled_rise_times.append(t)
		rise_times = plot_vout(df_c_vout, 'Coupled', delta, ax[i])
		if rise_times:
			for t in rise_times:
				coupled_rise_times.append(t)

		# plot_vcap(df_u_vcap, 'uncoupled', delta)
		# plot_vcap(df_c_vcap, 'coupled', delta)

	f.suptitle('Output Voltage with Changing Duty Ratio', fontweight='bold')
	f.tight_layout()
	plt.show()

	print('Coupled rise time: {}'.format(np.median(coupled_rise_times)))
	print('Uncoupled rise time: {}'.format(np.median(uncoupled_rise_times)))

if __name__ == '__main__':
	main()

