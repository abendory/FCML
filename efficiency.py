#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt

def main():
	path_c = 'efficiency/D=0.125_coupled.csv'
	path_u = 'efficiency/D=0.125_uncoupled.csv'
	df_c = pd.read_csv(path_c)
	df_u = pd.read_csv(path_u)

	f, ax = plt.subplots(2, 1, figsize=(8,6))

	ax[0].grid('on')
	ax[0].plot(df_c['Iout'], df_c['Efficiency'])
	ax[0].plot(df_u['Iout'], df_u['Efficiency'])
	ax[0].scatter(df_c['Iout'], df_c['Efficiency'])
	ax[0].scatter(df_u['Iout'], df_u['Efficiency'])
	ax[0].set_xlabel('Load (A)')
	ax[0].set_ylabel('Efficiency (\%)')
	ax[0].set_title('Efficiency vs. Current Load')
	ax[0].legend(['Coupled', 'Uncoupled'])

	ax[1].grid('on')
	ax[1].plot(df_c['Iout'], df_c['Vout'])
	ax[1].plot(df_u['Iout'], df_u['Vout'])
	ax[1].scatter(df_c['Iout'], df_c['Vout'])
	ax[1].scatter(df_u['Iout'], df_u['Vout'])
	ax[1].set_xlabel('Load (A)')
	ax[1].set_ylabel('Output Voltage (V)')
	ax[1].set_title('Output Voltage vs. Current Load')
	ax[1].legend(['Coupled', 'Uncoupled'])

	plt.tight_layout()

	plt.show()

if __name__ == '__main__':
	main()