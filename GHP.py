import pandas as pd

# demand_input = input("Podaj tygodnie i odpowiadające im popyty (np. '5:12,7:8'): ")
demand_input = '5:20,7:40'
# production_input = input("Podaj tygodnie i odpowiadające im sztuki do wyprodukowania (np. '5:12,7:8'): ")
production_input = '5:18,7:40'
# available_input = input("Podaj obecnie dostępne sztuki towaru: ")
available_input = '2'
class GHP:

    def __init__(self, demand_input, production_input, available_input):
        self.demand_input = demand_input
        self.production_input = production_input
        self.available_input = available_input

    def calculate_production(self, production_input):
        production = [0 for x in range(10)]
        for pair in production_input.split(","):
            week, amount = pair.split(":")
            week = int(week.strip())
            amount = int(amount.strip())
            production[week-1] = amount
        return production

    def calculate_demand(self, demand_input):
        demand = [0 for x in range(10)]
        for pair in demand_input.split(","):
            week, amount = pair.split(":")
            week = int(week.strip())
            amount = int(amount.strip())
            demand[week-1] = amount
        return demand

    def calculate_available(self, available_input):
        available = [0 for x in range(10)]
        demand = self.calculate_demand(demand_input)
        production = self.calculate_production(production_input)
        available[0] = available_input
        for i in range(len(demand)):
            if demand[i] == 0: 
                available[i] = int(available_input)
            else:
                break
        for i in range(1, len(available)):
            if demand[i] != 0:
                available[i] = production[i] - demand[i] + available[i-1]
            else:
                try:
                    available[i] = available[i-1]
                except:
                    pass
        return available

    def calculate_ghp(self):
        ghp = {
        'tydzień' : [1,2,3,4,5,6,7,8,9,10],
        'przewidywany popyt' : self.calculate_demand(demand_input),
        'produkcja' : self.calculate_production(production_input),
        'dostepne' : self.calculate_available(available_input)
        }
        return pd.DataFrame(ghp).transpose()
    
    def __str__(self):
        return f"{self.calculate_ghp()}"
    
    def get_production(self):
        print(f'produkcja to: {self.calculate_ghp().loc['produkcja',:]}')
        return self.calculate_ghp().loc['produkcja',:]


if __name__ == "__main__":

    ghp1 = GHP('5:20,7:40', '5:18,7:40', '2')
    print(ghp1)
#print(ghp1.get_production())

# g = calculate_ghp()

# print(make_dataframe(g))