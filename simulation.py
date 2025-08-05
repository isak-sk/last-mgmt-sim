import simpy
from house import House
from battery import Battery
from lkw import LWK
from pkw import PKW


class Simulation:

    def __init__(self, df):
        self.data = df
        self.env = simpy.Environment()
        self.logs = []
        self.house = House()
        self.battery = Battery()
        self.lkw = LWK()
        self.pkw = PKW()
        self.feed_in = 0.0

    def sim_core(self):
        for i, row in self.data.iterrows():
            hour = row['parsed_time']
            pv_prod = row['Produktion']
            bezug = row['Bezug']

            pv_left, pv_used_house, grid_used_house = self.house.consume(bezug, pv_prod)


            hour = row['parsed_time'].hour
            demand_lkw = self.lkw.lkw_demand(hour)
            
            bat_used = self.lkw.consume(hour, self.battery)
            

            pv_left, grid_pkw, pv_used_pkw = self.pkw.consume(hour, pv_left)


            # feed battery whatever is left
            if pv_left > 0:
                charged = self.battery.charge(pv_left)
                pv_left -= charged
            else:
                charged = 0.0

            # Feed in remaining to grid.
            if pv_left > 0:
                feed_kwh = pv_left
                self.feed_in += pv_left
                pv_left = 0

            else: 
                feed_kwh = 0.0

            self.logs.append({
                "tick": i,
                "hour": hour,
                "pv_prod": pv_prod,
                "bezug_house": bezug,
                "house_pv": pv_used_house,
                "house_grid": grid_used_house,
                "lkw_demand": demand_lkw,
                "lkw_unmet": self.lkw.unmet,
                "lkw_battery": bat_used,
                "pkw_demand": pv_used_pkw + grid_pkw,
                "pkw_grid": grid_pkw,
                "pkw_pv": pv_used_pkw,
                "battery_soc": self.battery.soc,
                "battery_charged": charged,
                "pv_left": pv_left,
                "feed_in": feed_kwh,
            })


            yield self.env.timeout(1)
