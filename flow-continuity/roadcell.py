import itertools


class RoadCell:
	id_iter = itertools.count()
	def __init__(self,
					lanes = 3,
					length = 100,
					max_density = 120, 
					time_gap = 1.2,
					speed_des = 50,
					veh_len = 4.5,
					min_gap = 2.0):
		self.id = next(RoadCell.id_iter)
		self.num_lanes = lanes
		self.length = length
		self.max_density = max_density
		self.time_gap = time_gap
		self.speed_des = speed_des
		self.veh_len = veh_len
		self.min_gap = min_gap
		self.l_eff = (1/max_density)*1000
		self.q_max = (1/(self.time_gap+(self.l_eff/(self.speed_des*(1000/3600)))))*3600
		self.c = (-self.l_eff/self.time_gap)*3.6
		self.density = 0
		self.flow = 0
		try:
			self.speed = self.flow/self.density
		except:
			self.speed = self.speed_des
		self.capacity = self.q_max*self.num_lanes
		self.capacity_density = 1/((self.speed_des*self.time_gap*(1000/3600)) + self.l_eff)
		self.supply = 0
		self.demand = 0
		self.cell_up = None
		self.cell_down = None

	def determine_upstream_downstream_cells(self, segments):
		num_segments = len(segments)
		if self.id == 0:
			self.cell_up = None
		else:
			self.cell_up = segments[self.id-1]

		if self.id >= num_segments-1:
			self.cell_down = None
		else:
			self.cell_down = segments[self.id+1]

	def determine_supply_and_demand(self):
		pc = self.capacity_density
		if self.cell_up != None:
			capacity_up = self.cell_up.capacity
			flow_up = self.cell_up.flow
			density_up = self.cell_up.density

			self.supply = 0
			if density_up>pc:
				self.supply = flow_up
			else:
				self.supply = capacity_up

		else:
			self.supply = self.q_max

		capacity = self.capacity
		flow = self.flow
		density = self.density
		self.demand = 0
		if density<=pc:
			self.demand=flow
		else:
			self.demand=capacity

	def determine_flow_thru_cell_bounds(self):
		self.Q_up = 0
		self.Q_down = 0
		if self.cell_up == None:
			self.Q_up = min(self.supply, self.capacity)
		else:
			self.Q_up = min(self.supply, self.cell_up.capacity)

		if self.cell_down == None:
			self.Q_down = min(self.capacity, self.demand)
		else:
			self.Q_down = min(self.cell_down.supply, self.demand)


	def update_cell(self):
		# DOUBLE CHECK THESE VALUES
		self.density = self.density + (1/(self.length/1000))*(self.Q_up-self.Q_down)*0.5/3600
		Q_e1 = self.speed_des*self.density
		Q_e2 = self.q_max*(1-(self.c/self.speed_des)) + self.c*self.density
		if self.density <= self.q_max/self.speed_des:
			Q_e = Q_e1/self.num_lanes
		else:
			Q_e = Q_e2/self.num_lanes
		if self.id == 4:
			print(f"q_max: {self.q_max}")
			print(f"num_lanes:{self.num_lanes}; Q_e:{Q_e}; density:{self.density}")
		self.flow = max(0,self.num_lanes*Q_e)#*(self.density/self.num_lanes)
		try:
			self.speed = self.flow/self.density
		except:
			self.speed = self.speed_des