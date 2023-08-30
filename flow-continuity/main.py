"""
Macroscopic Simulator
Continuity Equation w/ Cells

Author: Jerry Cazares
Date: August 7, 2023

Objective:
Simulate macroscopic flow through road cells using the
supply-demand methodology as described in 
Chapters 7 and 8 of
Traffic Flow Dyanmics by Trieber & Kesting.

The general appraoch uses the LWR model
with a triangular fundamental diagram.

"""

import numpy as np
import math
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import csv
from roadcell import RoadCell

# des speed: 110 kph (75 mph) in hwy, 50 kph (30) in city
# T: 1.4 s in hwy, 1.2 s in city
# max density: 120 veh/km (193 veh/mi) hwy, 120 veh/km city





def create_segments(num):
	segments = np.array([])
	for i in range(num):
		cell = RoadCell()
		segments = np.append(segments, cell)
	return segments

def plot_results(results):
	q_all = results[0]
	k_all = results[1]
	u_all = results[2]

	num_segments = len(q_all)
	num_plots = 3
	fig, ax = plt.subplots(num_plots, num_segments)
	for i, key in enumerate(q_all):
		for j in range(num_plots):
			axi = ax[j][i]
			if j == 0:
				axi.plot(k_all[key],u_all[key], 'ko')
				axi.set_ylabel('Speed (kph)')
				axi.set_xlabel('Density (kpm)')
				axi.set_ylim(top=55, bottom=0)
				axi.set_xlim(left=0, right=250)
			elif j == 1:
				axi.plot(k_all[key],q_all[key], 'ko')
				axi.set_ylabel('Flow (vph)')
				axi.set_xlabel('Density (kpm)')
				axi.set_ylim(top=2000, bottom=0)
				axi.set_xlim(left=0, right=250)
			else:
				axi.plot(q_all[key],u_all[key], 'ko')
				axi.set_ylabel('Speed (kph)')
				axi.set_xlabel('Flow (vph)')
				axi.set_ylim(top=55, bottom=0)
				axi.set_xlim(left=0, right=2000)

	for a_r in ax.reshape(-1):
		a_r.grid(True)
	plt.show()

if __name__ == '__main__':
	num_segments = 10
	segments=np.array([])
	segments = create_segments(num_segments)

	# Create bottleneck
	reduction_cell = segments[4]
	reduction_cell.num_lanes=2
	reduction_cell.speed_des = 40
	reduction_cell.q_max = (1/(reduction_cell.time_gap+(reduction_cell.l_eff/(reduction_cell.speed_des*(1000/3600)))))*3600
	reduction_cell.capacity = reduction_cell.q_max*reduction_cell.num_lanes
	print("reduction_cell number of lanes: ", reduction_cell.num_lanes)
	print("reduction cell capacity after: ", reduction_cell.capacity)
	
	total_time = 500
	time_step = 0.5
	time = 0

	for cell in segments:
		cell.determine_upstream_downstream_cells(segments)

	
	results_q = {2: [], 4: [], 6: [], 8: []}
	results_k = {2: [], 4: [], 6: [], 8: []}
	results_u = {2: [], 4: [], 6: [], 8: []}

	raw_q = {2: [], 4: [], 6: [], 8: []}
	raw_k = {2: [], 4: [], 6: [], 8: []}
	raw_u = {2: [], 4: [], 6: [], 8: []}
	
	while time <= total_time:
		print("\n=============================================")
		print(f"---------------   Time={time}s  ---------------")
		print("=============================================")

		for cell in segments:
			cell.determine_supply_and_demand()
			cell.determine_flow_thru_cell_bounds()
			cell.update_cell()
			if cell.id == 2:
				print(f"cell {cell.id}'s info:\nspeed: {cell.speed} kph\nflow: {cell.flow} veh/hr\ndensity: {cell.density} veh/km")

			if cell.id %2 == 0 and cell.id != 0 and cell.id != num_segments-1:
				# Create method to save values and aggregate every 5 seconds,
				# then give the aggregated values to the results dict

				raw_q[cell.id].append(cell.flow)
				raw_k[cell.id].append(cell.density)
				raw_u[cell.id].append(cell.speed)

				if time % 5 == 0 and time > 0:
					results_q[cell.id].append(statistics.mean(raw_q[cell.id]))
					results_k[cell.id].append(statistics.mean(raw_k[cell.id]))
					results_u[cell.id].append(statistics.mean(raw_u[cell.id]))

		time += time_step

	plot_results((results_q, results_k, results_u))

