class House:
    def __init__(self):
        self.total_demand = 0
        self.from_pv = 0
        self.from_grid = 0



    def consume(self, demand, pv_prod):
        pv_used = min(demand, pv_prod)
        grid_used = demand - pv_used 
        leftover_pv = pv_prod - pv_used

        # track stats
        self.total_demand += demand
        self.from_pv += pv_used
        self.from_grid += grid_used

        # leftover
        return leftover_pv, pv_used, grid_used
