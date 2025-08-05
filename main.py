import pandas as pd
import os
from plot import plot

from excel import ExcelLoader
from simulation import Simulation


def main():
    print("Loading excel file...")
    loader = ExcelLoader()
    df = loader.load_data()

    sim = Simulation(df)
    sim.env.process(sim.sim_core())
    sim.env.run()

    os.makedirs("output", exist_ok=True)

    df_logs = pd.DataFrame(sim.logs)
    df_logs.to_csv("output/simulation_log.csv", index=False)

    # PV Usage Breakdown

    total_pv = sum(log['pv_prod'] for log in sim.logs)
    house_pv = sum(log['house_pv'] for log in sim.logs)
    pkw_pv = sim.pkw.from_pv
    battery_charged = sum(log['battery_charged'] for log in sim.logs)
    feed_in = sim.feed_in

    reconstructed_pv = house_pv + pkw_pv + battery_charged + feed_in
    diff = total_pv - reconstructed_pv

    print("\n--- PV Usage Breakdown ---")
    print(f"Total PV Produced:        {total_pv:10.2f} kWh")
    print(f"  → House direct:         {house_pv:10.2f} kWh")
    print(f"  → PKW direct:           {pkw_pv:10.2f} kWh")
    print(f"  → Battery charged:      {battery_charged:10.2f} kWh")
    print(f"  → Fed into grid:        {feed_in:10.2f} kWh")
    print(f"  → Total accounted for:  {reconstructed_pv:10.2f} kWh")
    print(f"Difference:               {diff:+.5f} kWh ({100 * diff / total_pv:.4f}%)")

    # Demand Breakdown

    house_demand = sim.house.total_demand
    lkw_demand = sim.lkw.total_demand
    pkw_demand = sim.pkw.total_demand

    house_grid = sim.house.from_grid
    pkw_grid = sim.pkw.from_grid

    house_pv = sim.house.from_pv
    pkw_pv = sim.pkw.from_pv

    battery_used = sim.lkw.from_battery

    print("\n--- Demand Breakdown ---")
    print(f"House Demand:   {house_demand:10.2f} kWh  → PV: {house_pv:10.2f} | Grid: {house_grid:10.2f}")
    print(f"LKW Demand:     {lkw_demand:10.2f} kWh  → Battery: {battery_used:10.2f}")
    print(f"PKW Demand:     {pkw_demand:10.2f} kWh  → PV: {pkw_pv:10.2f} | Grid: {pkw_grid:10.2f}")

    # Totals

    total_demand = house_demand + lkw_demand + pkw_demand
    total_grid = house_grid + pkw_grid
    total_pv_direct = house_pv + pkw_pv

    print(f"\nTOTAL DEMAND:   {total_demand:10.2f} kWh")
    print(f"  → Grid:        {total_grid:10.2f} kWh")
    print(f"  → Direct PV:   {total_pv_direct:10.2f} kWh")
    print(f"  → From Battery:{battery_used:10.2f} kWh")
    print(f"  → PV Charged:  {battery_charged:10.2f} kWh")
    print(f"  → PV Fed In:   {feed_in:10.2f} kWh")

    # Plots

    plot()


if __name__ == "__main__":
    main()
