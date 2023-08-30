"""
Traffic Flow Dynamics
Chapter 3 Problem 3.2

Author: Jerry Cazares
Date: August 2, 2023
"""

# Problem 3.2 Determining Macroscopic Quantities from Single-Vehicle Dat

"""
Description:
On a two-lane highway all vehicles drive with distance headway 60 m.
The vehicles on the left lane all drive at speed 144 km/h on the right
lane at 72 km/h. A stationary detector captures single-vehicle data
(cf. Fig. 3.3) and aggregates them using deltaT = 60s.

1. What are the time headways deltaTalpha on both lanes? 
   What are the time gaps, assuming all vehicles are 5 m long?

2. Find the traffic flow, occupancy, and average speed (arithmetic and harmonic)
   seperately for both lanes (i.e. each lane is captured by its own detector) and
   also for both lanes combined (i.e. one detector captures vehicles on both lanes).
   For which type of average does the following statement hold: The average speed
   of all vehicles in both lanes is equal to the arithmetic mean of the average
   speed of each lane?
"""

# Problem 3.2.1

def find_time_headway(dx, v):
	# Units: 
	# dx: m
	# v: m/s
	t_headway = dx/v
	return t_headway

def find_time_gap(dx, l, v):
	# Units:
	# dx: m
	# l: m
	# v: m/s
	t_gap = (dx-l)/v
	return t_gap

v_len = 5
d_headway = 60
v_l1 = 144 * 0.2778
v_l2 = 72 * 0.2778

# Determine time headway for each lane
t_headway_l1 = find_time_headway(d_headway, v_l1)
t_headway_l2 = find_time_headway(d_headway, v_l2)

# Determine time gaps for each lane
t_gap_l1 = find_time_gap(d_headway, v_len, v_l1)
t_gap_l2 = find_time_gap(d_headway, v_len, v_l2)

print("\nSolution to Problem 3.2.1:")
print("time headway for the left lane is {:.1f} s".format(t_headway_l1))
print("time headway for the right lane is {:.1f} s".format(t_headway_l2))
print("time gap for the left lane is {:.2f} s".format(t_gap_l1))
print("time gap for the right lane is {:.2f} s".format(t_gap_l2))