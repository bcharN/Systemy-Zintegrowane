import pandas as pd
import json

class GHP:
    def __init__(self, ghp_params):
        self.ghp_params = ghp_params

    def calculate_production(self):
        production = [0 for _ in range(10)]
        for pair in self.ghp_params['production'].split(","):
            week, amount = pair.split(":")
            week = int(week.strip())
            amount = int(amount.strip())
            production[week - 1] = amount
        return production

    def calculate_demand(self):
        demand = [0 for _ in range(10)]
        for pair in self.ghp_params['demand'].split(","):
            week, amount = pair.split(":")
            week = int(week.strip())
            amount = int(amount.strip())
            demand[week - 1] = amount
        return demand

    def calculate_available(self):
        available = [0 for _ in range(10)]
        demand = self.calculate_demand()
        production = self.calculate_production()
        available[0] = int(self.ghp_params['available'])
        for i in range(len(demand)):
            if demand[i] == 0:
                available[i] = int(self.ghp_params['available'])
            else:
                break
        for i in range(1, len(available)):
            if demand[i] != 0:
                available[i] = production[i] - demand[i] + available[i - 1]
            else:
                try:
                    available[i] = available[i - 1]
                except:
                    pass
        return available

    def calculate_ghp(self):
        ghp = {
            'tydzień': list(range(1, 11)),
            'przewidywany popyt': self.calculate_demand(),
            'produkcja': self.calculate_production(),
            'dostepne': self.calculate_available()
        }
        return pd.DataFrame(ghp).transpose()

if __name__ == "__main__":
    with open('hantla.json', 'r') as file:
        data = json.load(file)

    ghp_params = data['hantla_do_cwiczen']['ghp_params']
    ghp1 = GHP(ghp_params)
    print(ghp1.calculate_ghp())
