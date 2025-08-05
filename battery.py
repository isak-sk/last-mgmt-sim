class Battery:


    def __init__(self):
        self.requested = 0
        self.available = 0
        self.capacity = 1000.0
        self.soc = 0
        self.max_power = 11.0
        self.efficiency = 0.95


    def discharge(self, amount):
        actual = min(amount / self.efficiency, self.soc, self.max_power)
        self.soc -= actual
        return actual


    def charge(self, amount):
        actual = min(amount * self.efficiency, self.max_power, self.capacity - self.soc)
        self.soc += actual
        self.soc = min(self.capacity, max(0.0, self.soc))
        return actual
