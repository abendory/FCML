import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_imbalance_mean(df, coupling, ax):
	t = df['TIME']
	vcap1 = (df['CH1'] - df['CH2']).rolling(window=5000).mean()
	vcap2 = (df['CH3'] - df['CH4']).rolling(window=5000).mean()
	imbalance = np.abs(vcap1 - vcap2)

	color = ('C2' if coupling == 'Uncoupled' else 'C3')
	idx = (0 if coupling == 'Uncoupled' else 1)
	mean = np.mean(imbalance)

	ax.axhline(mean, color=color, linestyle='dashed')
	ax.annotate('Mean imbalance ({}): {:1.2} V'.format(coupling, mean), (0, mean), fontweight='bold')

#----------------------------------------------------------------------
# def plot_vcap(df, coupling, ax):
def plot_vcap(df, coupling, ax_s, ax_d):

	#Vcap1 = CH1 - CH2. Vcap2 = CH3 - CH4

	lim = int((len(df['TIME']))/3)
	t = df['TIME']
	i1 = df['CH5']
	i2 = df['CH6']
	vcap1 = (df['CH1'] - df['CH2']).rolling(window=5000).mean()
	vcap2 = (df['CH3'] - df['CH4']).rolling(window=5000).mean()
	imbalance = np.abs(vcap1 - vcap2)

	ax_s.plot(t, vcap1)
	ax_s.plot(t, vcap2)
	ax_s.legend(['Vcap1', 'Vcap2'])
	ax_s.set_title('Flying Capacitor Voltages, {}'.format(coupling))
	ax_s.set_xlabel('Time (s)')
	ax_s.set_ylabel('Voltage (V)')

	color = ('C0' if coupling == 'Uncoupled' else 'C1')
	ax_d.plot(t, imbalance, color=color)

#----------------------------------------------------------------------

def main():
	header_rows = 11

	df_u = pd.read_csv('D=0.125_Rout=15_uncoupled/vcap_u_12.5_ALL.csv', skiprows=header_rows)
	df_c = pd.read_csv('D=0.125_Rout=15_coupled/vcap_c_12.5_ALL.csv', skiprows=header_rows)

	plt.figure(figsize=(12,8))
	ax1 = plt.subplot2grid((2,2), (0,0), colspan=1)
	ax2 = plt.subplot2grid((2,2), (0,1), colspan=1)
	ax3 = plt.subplot2grid((2,2), (1,0), colspan=2)
	ax1.grid('on')
	ax2.grid('on')
	ax3.grid('on')
	ax3.set_xticks(np.arange(df_u['TIME'][0], df_u['TIME'][len(df_u['TIME'])-1], 5000*(df_u['TIME'][1]-df_u['TIME'][0])))
	plot_vcap(df_u, 'Uncoupled', ax1, ax3)
	plot_vcap(df_c, 'Coupled', ax2, ax3)
	ax3.legend(['Uncoupled', 'Coupled'])
	plot_imbalance_mean(df_u, 'Uncoupled', ax3)
	plot_imbalance_mean(df_c, 'Coupled', ax3)
	ax3.set_title('Flying Capacitor Voltage Imbalance')
	ax3.set_xlabel('Time (s)')
	ax3.set_ylabel('Voltage (V)')

	plt.suptitle('Flying Capacitor Voltages', fontweight='bold')

	plt.tight_layout()
	plt.show()

#----------------------------------------------------------------------	

if __name__ == '__main__':
	main()