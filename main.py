from excel import ExcelLoader
from simulation import Simulation


def main():
    print("Loading excel files")
    loader = ExcelLoader()
    df = loader.load_data()
    
    sim = Simulation(df)
    sim.env.process(sim.sim_core())
    sim.env.run()


if __name__ == "__main__":
    main()
