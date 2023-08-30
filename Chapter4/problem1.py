"""
Chapter 4
Problem 4.1

Author: Jerry Cazares
Date: August 7, 2023

Statement:
Derive and sketch both the speed-density diagram and the
fundamental diagram subject to the following idealized
assumptions:
(i)   All vehicles are of length l = 5 m
(ii)  In free traffic (speed does not depend on other vehicles), all
      vehicles drive at their desired speed Vo = 120 kph
(iii) In congested traffic (speed is the same as the speed of the leading vehicle),
      drivers keep a gap of s(v) = so + vT to the leading vehicle, w/
      the minimum gap so = 2 m and time gap T = 1.6 s

"""
import numpy as np
import math
import pandas as pd
import statistics
import itertools
import matplotlib.pyplot as plt
import csv

l = 5 # m
gap_min = 2 # m
time_gap = 1.6 # s
speed_des = 120 # kph


if __name__ == '__main__':
	# Find max density
	l_eff = l + gap_min
	kmax = 1/l_eff
	kmax *= 1000 # Convert from veh/m to veh/km

	# Find critical density
	speed_des *= 0.2778 # Convert from kph to mps
	kcap = 1/(speed_des*time_gap+l_eff)
	kcap *= 1000 # Convert from veh/m to veh/km

	# Find capacity
	qcap = (1/time_gap)*(1/(1 + (l_eff/(speed_des*time_gap))))
	qcap *= 3600 # convert from veh/s to veh/hr

	print("maximum density: ", kmax)
	print("critical density: ", kcap)
	print("capacity: ", qcap)


	# From here, we can develop a FD using either Greenshields or LWR Triangular Model

	speed_des /= 0.2778
	m = (-speed_des/ (kmax - kcap))
	k = np.arange(0, 120, 0.1)
	u = [speed_des if ki <= kcap else m*ki + (speed_des/(kmax-kcap))*kmax for ki in k]
	q = u*k

	fig, ax = plt.subplots(3,1)
	ax[0].plot(k, u, 'k-')
	ax[0].set_ylabel('Speed (kph)')
	ax[0].set_xlabel('Density (kpm)')
	ax[1].plot(k, q, 'k-')
	ax[1].set_ylabel('Flow (vph)')
	ax[1].set_xlabel('Density (kpm)')
	ax[2].plot(q, u, 'k-')
	ax[2].set_ylabel('Speed (kph)')
	ax[2].set_xlabel('Flow (vph)')
	plt.show()
