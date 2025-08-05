import pandas as pd
import matplotlib.pyplot as plt
import os


def plot():
    df = pd.read_csv("output/simulation_log.csv")
    os.makedirs("output/plots", exist_ok=True)

    df['hour_of_day'] = df['tick'] % 24
    df['day'] = df['tick'] // 24
    df['month'] = pd.to_datetime(df['tick'], unit='h', origin='2024-01-01').dt.month

    # ---- Chart 1: Battery SoC % ----
    battery_capacity = 1000.0  # must match battery config
    df['soc_pct'] = df['battery_soc'] / battery_capacity * 100

    plt.figure(figsize=(14, 4))
    plt.plot(df['tick'], df['soc_pct'], label='Battery SoC (%)', color='blue')
    plt.xlabel("Hour")
    plt.ylabel("State of Charge (%)")
    plt.title("Battery State of Charge Over Time")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/plots/plot_1_soc_pct.png", dpi=150)

    # ---- Chart 2: Daily Profile - PKW + LKW Demand ----
    df['lkw_demand'] = df['lkw_battery'] + df['lkw_unmet']
    daily_profile = df.groupby('hour_of_day')[['pkw_demand', 'lkw_demand']].mean()

    plt.figure(figsize=(10, 5))
    plt.stackplot(daily_profile.index,
                  daily_profile['pkw_demand'],
                  daily_profile['lkw_demand'],
                  labels=['PKW Demand', 'LKW Demand'])
    plt.title("Average Daily Demand Profile: PKW + LKW")
    plt.xlabel("Hour of Day")
    plt.ylabel("kWh")
    plt.xticks(range(0, 24, 2))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/plots/plot_2_daily_demand.png", dpi=150)

    # ---- Chart 3: Daily Profile - PV, Grid, Battery Flow ----
    df['battery_out'] = df['lkw_battery']  # all discharge is for LKW
    daily_energy = df.groupby('hour_of_day')[['pv_prod', 'house_grid', 'pkw_grid', 'battery_charged', 'battery_out']].mean()
    daily_energy['grid_total'] = daily_energy['house_grid'] + daily_energy['pkw_grid']

    plt.figure(figsize=(10, 5))
    plt.stackplot(daily_energy.index,
                  daily_energy['pv_prod'],
                  daily_energy['grid_total'],
                  daily_energy['battery_charged'],
                  daily_energy['battery_out'],
                  labels=['PV Production', 'Grid Usage', 'Battery Charging', 'Battery Discharging'])
    plt.title("Average Daily Energy Flow: PV, Grid, Battery")
    plt.xlabel("Hour of Day")
    plt.ylabel("kWh")
    plt.xticks(range(0, 24, 2))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/plots/plot_3_daily_energy_flow.png", dpi=150)

    # ---- Chart 4: Monthly Energy Breakdown (already existed) ----
    monthly_summary = df.groupby('month')[['house_grid', 'house_pv', 'feed_in', 'battery_charged']].sum()

    monthly_summary.plot(kind='bar', stacked=True, figsize=(10, 5))
    plt.title("Monthly Energy Flow Breakdown")
    plt.xlabel("Month")
    plt.ylabel("kWh")
    plt.tight_layout()
    plt.savefig("output/plots/plot_4_monthly_energy.png", dpi=150)
