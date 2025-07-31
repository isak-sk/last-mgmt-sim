import simpy
from house import House

class Simulation:

    def __init__(self, df):
        self.data = df
        self.env = simpy.Environment()
        self.house = House()


    def sim_core(self):
        for i, row in self.data.iterrows():
            hour = row['parsed_time']
            pv_prod = row['Produktion']
            bezug = row['Bezug']

            pv_left = self.house.consume(bezug, pv_prod)



            yield self.env.timeout(1)
