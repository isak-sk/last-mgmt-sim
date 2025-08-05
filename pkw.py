class PKW:

    def __init__(self):
        self.total_demand = 0
        self.from_pv = 0
        self.from_grid = 0
        self.unmet = 0

    def pkw_demand(self, hour):
        return 11 if 6 <= hour <= 10 else 0.0

    def consume(self, hour, pv_left):
        demand = self.pkw_demand(hour)

        if demand == 0.0:
            return pv_left, 0.0, 0.0

        pv_used = min(demand, pv_left)
        grid_used = demand - pv_used
        pv_left -= pv_used

        self.total_demand += demand
        self.from_pv += pv_used
        self.from_grid += grid_used

        return pv_left, grid_used, pv_used
