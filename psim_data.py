#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import hilbert, chirp

#----------------------------------------------------------------------

def plot_imbalance_mean(ax, t, imbalance_c, imbalance_d):

	lim = 100000

	ax.set_title('Flying Capacitor Voltage Imbalance')
	ax.set_xlabel('Time (s)')
	ax.set_ylabel('Voltage (V)')

	mean_d = np.mean(imbalance_d)
	mean_c = np.mean(imbalance_c)

	ax.plot(t, imbalance_d)
	ax.plot(t, imbalance_c)

	ax.legend(['Discrete', 'Coupled'])

	ax.axhline(mean_c, color='C2', linestyle='dashed')
	ax.annotate('Mean imbalance ({}): {:1.2} V'.format('Coupled', mean_c), (0, mean_c), fontweight='bold')

	ax.axhline(mean_d, color='C3', linestyle='dashed')
	ax.annotate('Mean imbalance ({}): {:1.2} V'.format('Discrete', mean_d), (t[len(t)-1]/3, mean_d), fontweight='bold')

#----------------------------------------------------------------------

def plot_vcap(df, ax_1, ax_2, ax_d):

	lim = 100000

	t = df['Time'][:lim]

	vcap1_c = df['VC1'][:lim]
	vcap2_c = df['VC2'][:lim]
	imbalance_c = np.abs(vcap1_c - vcap2_c)

	vcap1_d = df['VD1'][:lim]
	vcap2_d = df['VD2'][:lim]
	imbalance_d = np.abs(vcap1_d - vcap2_d)

	ax_1.plot(t, vcap1_c)
	ax_1.plot(t, vcap2_c)
	ax_1.legend(['Vcap1', 'Vcap2'])
	ax_1.set_title('Coupled')
	ax_1.set_xlabel('Time (s)')
	ax_1.set_ylabel('Voltage (V)')

	ax_2.plot(t, vcap1_d)
	ax_2.plot(t, vcap2_d)
	ax_2.legend(['Vcap1', 'Vcap2'])
	ax_2.set_title('Discrete')
	ax_2.set_xlabel('Time (s)')
	ax_2.set_ylabel('Voltage (V)')

	ax_1.grid('on')
	ax_2.grid('on')
	ax_d.grid('on')

	plot_imbalance_mean(ax_d, t, imbalance_c, imbalance_d)

#----------------------------------------------------------------------

def plot_performance(df, coupling, ax):
	start = 10000
	end = 12000
	lim = 100000

	t = df['Time']

	if coupling == 'Coupled':
		i1 = df['IC1']
		i2 = df['IC2']
		vout = df['VoutC']
	else:
		i1 = df['ID1']
		i2 = df['ID2']
		vout = df['VoutD']
	iout = i1 + i2

	# i1_r = i1.rolling(window=500).mean()
	# i2_r = i2.rolling(window=500).mean()
	# i1_zeros = np.where(np.diff(np.sign(i1 - i1_r)))
	# i2_zeros = np.where(np.diff(np.sign(i1 - i1_r)))
	# i1_zeros = np.where(np.diff(np.sign(i1[:len(t)])))[0]
	# period = t[i1_zeros[2]] - t[i1_zeros[0]]

	# i1_ptp = np.ptp(i1)
	# i2_ptp = np.ptp(i2)
	# vout_ptp = np.amax(vout) - np.amin(vout)

	col = (1 if coupling == 'Coupled' else 0)

	# # Plot currents
	ax[0,col].plot(t[:lim], i1[:lim], color='C0')
	ax[0,col].plot(t[:lim], i2[:lim], color='C1')
	# ax[0,col].plot(t[:lim], i1_r[:lim])
	# ax[0,col].plot(t[:lim], i2_r[:lim])
	ax[0,col].set_ylabel('Current (A)')
	ax[0,col].legend(['I1', 'I2'])
	ax[0,col].set_title('Inductor Currents')

	ax[1,col].plot(t[start:end], i1[start:end], color='C0')
	ax[1,col].plot(t[start:end], i2[start:end], color='C1')
	# ax[0,col].plot(t[:lim], i1_r[:lim])
	# ax[0,col].plot(t[:lim], i2_r[:lim])
	ax[1,col].set_ylabel('Current (A)')
	ax[1,col].legend(['I1', 'I2'])
	ax[1,col].set_title('Inductor Currents (Zoomed In)')

	# # Plot currents peak-to-peak
	# ax[0,col].axhline(np.amax(i1), color='C2', linestyle='dashed')
	# ax[0,col].axhline(np.amin(i1), color='C3', linestyle='dashed')
	# ax[0,col].annotate('', 
	# 	xy=(t[int(len(t)/4)],np.amax(i1)),
	# 	xytext=(t[int(len(t)/4)],np.amin(i1)),
	# 	arrowprops=dict(arrowstyle="<->")
	# 	)
	# ax[0,col].annotate(' I1 peak-to-peak: {}'.format(i1_ptp), (t[int(len(t)/4)], 1), fontweight='bold')

	# ax[0,col].annotate('', 
	# 	xy=(0,np.amax(i2)),
	# 	xytext=(0,np.amin(i2)),
	# 	arrowprops=dict(arrowstyle="<->")
	# 	)
	# ax[0,col].annotate(' I2 peak-to-peak: {}'.format(i2_ptp), (0,1), fontweight='bold')
	# ax[0,col].axhline(np.amax(i2), color='C6', linestyle='dashed')
	# ax[0,col].axhline(np.amin(i2), color='C5', linestyle='dashed')

	# # Plot period
	# ax[0,col].annotate('', 
	# 	xy=(t[i1_zeros[0]],0),
	# 	xytext=(t[i1_zeros[2]],0),
	# 	arrowprops=dict(arrowstyle="<->")
	# 	)
	# ax[0,col].annotate(' Period: {:.2e}'.format(period), (t[i1_zeros[0]],-1), fontweight='bold')

	# ax[1,col].plot(t, sw1)
	# ax[1,col].plot(t, sw2)
	# ax[1,col].legend(['Vsw1', 'Vsw2'])
	# ax[1,col].set_ylabel('Volts (V)')
	# ax[1,col].set_title('Switch Node Voltages')

	ax[2,col].plot(t[:lim], vout[:lim], color='C0')
	ax[2,col].legend(['Vout'])
	# ax[2,col].annotate('{}'.format(vout_ptp), (2,np.mean(vout)))
	ax[2,col].set_xlabel('Time (s)')
	ax[2,col].set_ylabel('Volts (V)')
	ax[2,col].set_title('Output Voltage')
	# ax[2,col].axhline(np.amax(vout), color='C1', linestyle='dashed')
	# ax[2,col].axhline(np.amin(vout), color='C2', linestyle='dashed')
	# # ax[2,col].axhline(np.mean(vout), color='C3')
	# ax[2,col].annotate(' Vout peak-to-peak: {:.2f}'.format(vout_ptp), (t[int(len(t)/4)], np.mean(vout)), fontweight='bold')
	# ax[2,col].annotate('', 
	# 	xy=(t[int(len(t)/4)],np.amax(vout)),
	# 	xytext=(t[int(len(t)/4)],np.amin(vout)),
	# 	arrowprops=dict(arrowstyle="<->")
	# 	)

def main():

	df = pd.read_csv('psim_out.csv')

	plt.figure(figsize=(12,8))
	ax1 = plt.subplot2grid((2,2), (0,0), colspan=1)
	ax2 = plt.subplot2grid((2,2), (0,1), colspan=1)
	ax3 = plt.subplot2grid((2,2), (1,0), colspan=2)
	plot_vcap(df, ax1, ax2, ax3)

	plt.suptitle('Flying Capacitor Voltages', fontweight='bold')
	plt.tight_layout()

	# f, ax = plt.subplots(3, 2, figsize=(12,8))
	# plot_performance(df, 'Coupled', ax)
	# plot_performance(df, 'Discrete', ax)
	# f.suptitle('Discrete (left) vs. Coupled (right) performance', fontweight='bold')
	# f.tight_layout()

	plt.show()

#----------------------------------------------------------------------	

if __name__ == '__main__':
	main()