import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#----------------------------------------------------------------------

def plot_performance(df, coupling, ax):

	# I1, I2 in CH5, CH6. Vout in CH3. VSW1, VSW2 in CH1, CH2

	lim = int((len(df['TIME']))/3)
	t = df['TIME'][:lim]
	i1 = df['CH5'][:lim]
	i2 = df['CH6'][:lim]
	sw1 = df['CH1'][:lim]
	sw2 = df['CH2'][:lim]
	iout = i1 + i2
	# vout = df['CH3'][:lim]
	vout = df['CH3'].rolling(window=50).mean()[:lim]
	t_sub = t[t<0]
	i1_zeros = np.where(np.diff(np.sign(i1[:len(t_sub)])))[0]
	# period = np.mean([t_sub[i1_zeros[i+2]] - t_sub[i1_zeros[i]] for i in range(len(i1_zeros)-2)])
	period = t_sub[i1_zeros[2]] - t_sub[i1_zeros[0]]

	i1_ptp = np.ptp(i1)
	i2_ptp = np.ptp(i2)
	vout_ptp = np.amax(vout) - np.amin(vout)

	col = (0 if coupling == 'uncoupled' else 1)

	# Plot currents
	ax[0,col].plot(t, i1, color='C0')
	ax[0,col].plot(t, i2, color='C1')
	ax[0,col].set_ylabel('Current (A)')
	ax[0,col].legend(['I1', 'I2'])
	ax[0,col].set_title('Inductor Currents')

	# Plot currents peak-to-peak
	ax[0,col].axhline(np.amax(i1), color='C2', linestyle='dashed')
	ax[0,col].axhline(np.amin(i1), color='C3', linestyle='dashed')
	ax[0,col].annotate('', 
		xy=(t[int(len(t)/4)],np.amax(i1)),
		xytext=(t[int(len(t)/4)],np.amin(i1)),
		arrowprops=dict(arrowstyle="<->")
		)
	ax[0,col].annotate(' I1 peak-to-peak: {}'.format(i1_ptp), (t[int(len(t)/4)], 1), fontweight='bold')

	ax[0,col].annotate('', 
		xy=(0,np.amax(i2)),
		xytext=(0,np.amin(i2)),
		arrowprops=dict(arrowstyle="<->")
		)
	ax[0,col].annotate(' I2 peak-to-peak: {}'.format(i2_ptp), (0,1), fontweight='bold')
	ax[0,col].axhline(np.amax(i2), color='C6', linestyle='dashed')
	ax[0,col].axhline(np.amin(i2), color='C5', linestyle='dashed')

	# Plot period
	ax[0,col].annotate('', 
		xy=(t[i1_zeros[0]],0),
		xytext=(t[i1_zeros[2]],0),
		arrowprops=dict(arrowstyle="<->")
		)
	ax[0,col].annotate(' Period: {:.2e}'.format(period), (t[i1_zeros[0]],-1), fontweight='bold')

	ax[1,col].plot(t, sw1)
	ax[1,col].plot(t, sw2)
	ax[1,col].legend(['Vsw1', 'Vsw2'])
	ax[1,col].set_ylabel('Volts (V)')
	ax[1,col].set_title('Switch Node Voltages')

	ax[2,col].plot(t, vout, color='C0')
	ax[2,col].legend(['Vout'])
	# ax[2,col].annotate('{}'.format(vout_ptp), (2,np.mean(vout)))
	ax[2,col].set_xlabel('Time (s)')
	ax[2,col].set_ylabel('Volts (V)')
	ax[2,col].set_title('Output Voltage')
	ax[2,col].axhline(np.amax(vout), color='C1', linestyle='dashed')
	ax[2,col].axhline(np.amin(vout), color='C2', linestyle='dashed')
	# ax[2,col].axhline(np.mean(vout), color='C3')
	ax[2,col].annotate(' Vout peak-to-peak: {:.2f}'.format(vout_ptp), (t[int(len(t)/4)], np.mean(vout)), fontweight='bold')
	ax[2,col].annotate('', 
		xy=(t[int(len(t)/4)],np.amax(vout)),
		xytext=(t[int(len(t)/4)],np.amin(vout)),
		arrowprops=dict(arrowstyle="<->")
		)

#----------------------------------------------------------------------

def main():
	header_rows = 11

	df_u = pd.read_csv('D=0.125_Rout=15_uncoupled/vout_u_12.5_ALL.csv', skiprows=header_rows)
	df_c = pd.read_csv('D=0.125_Rout=15_coupled/vout_c_12.5_ALL.csv', skiprows=header_rows)

	f, ax = plt.subplots(3, 2, sharex='col', figsize=(12,8))
	# f, ax = plt.subplots(2, 2, sharex='row', figsize=(12,8))
	for a in ax.flatten():
		a.grid('on')
	f.suptitle('Uncoupled (left) vs. Coupled (right)', fontweight='bold')
	plot_performance(df_u, 'uncoupled', ax)
	plot_performance(df_c, 'coupled', ax)
	f.tight_layout()

	plt.show()

#----------------------------------------------------------------------	

if __name__ == '__main__':
	main()
