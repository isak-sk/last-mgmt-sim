from battery import Battery


class LWK:

    def __init__(self):
        self.total_demand = 0
        self.from_battery = 0
        self.from_pv = 0
        self.unmet = 0

    def lkw_demand(self, hour):
        if 16 <= hour <= 18:
            return 200.0
        elif 18 <= hour <= 20:
            return 300.0
        elif 20 <= hour <= 22:
            return 350.0
        elif 22 <= hour <= 5:
            return 400.0
        else:
            return 0.0

    def consume(self, hour, battery):
        # Only allow charging at night/evening
        if hour >= 17 or hour < 6:
            demand = self.lkw_demand(hour)
            battery_used = battery.discharge(demand)
            unmet = demand - battery_used
        else:
            battery_used = 0.0
            unmet = 0.0

        self.total_demand += battery_used + unmet
        self.from_battery += battery_used
        self.unmet += unmet

        return battery_used
