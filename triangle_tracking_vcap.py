import pandas as pd
import matplotlib.pyplot as plt

header_rows = 11

dfs_u = []
dfs_c = []

deltas = [1000, 100, 50, 10]

# Assume Vout in CH1, Vcap1 in CH2-Ch3, Vcap2 in CH4-Ch7, current in Ch5/6
# For delta == 1000 uncoupled, Vcap1 in CH3-CH4, Vcap2 in CH7-CH8
def plot_vcap(df, coupling, delta):
	if delta == 1000 and coupling == 'uncoupled':
		vcap1 = (df['CH3'] - df['CH4']).rolling(window=1000).mean()
		vcap2 = (df['CH7'] - df['CH8']).rolling(window=1000).mean()
		vout = [0 for t in df['TIME']]
	elif delta == 50 and coupling == 'coupled':
		vcap1 = (df['CH2'] - df['CH3']).rolling(window=1000).mean()
		vcap2 = [0 for t in df['TIME']]
		vout = df['CH1']
	else:
		vcap1 = (df['CH2'] - df['CH3']).rolling(window=1000).mean()
		vcap2 = (df['CH4'] - df['CH7']).rolling(window=1000).mean()
		vout = df['CH1']

	t = df['TIME']

	f, ax = plt.subplots(3, sharex = True)
	f.suptitle('{}, delta = {}'.format(coupling, delta))
	ax[0].plot(t, vout)
	ax[0].set_ylabel('Voltage (V)')
	ax[0].set_title('Output voltage')

	ax[1].plot(t, vcap1)
	ax[1].plot(t, vcap2)
	ax[1].set_ylabel('Voltage (V)')
	ax[1].set_title('Flying capacitor voltages')
	ax[1].legend(['Vcap1', 'Vcap2'])

	ax[2].plot(t, vout-vcap1)
	ax[2].plot(t, vout-vcap2)
	ax[2].set_ylabel('Error (V)')
	ax[2].set_title('Flying capacitor deviation from output voltage')
	ax[2].legend(['Vcap1 error', 'Vcap2 error'])
	ax[2].set_xlabel('Time (s)')


def main():

	for i, delta in enumerate(deltas):
		path_u = 'triangle_tracking_uncoupled/vcap_u_{}_ALL.csv'.format(delta)
		path_c = 'triangle_tracking_coupled/vcap_c_{}_ALL.csv'.format(delta)
		df_u = pd.read_csv(path_u, skiprows=header_rows)
		df_c = pd.read_csv(path_c, skiprows=header_rows)

		plot_vcap(df_u, 'uncoupled', delta)
		plot_vcap(df_c, 'coupled', delta)

	plt.show()

if __name__ == '__main__':
	main()
