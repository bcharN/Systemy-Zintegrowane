import json

class BOM:
    
    def __init__(self):
        self.bom = json.load(open('hantla.json', 'r'))

    # def __str__(self) -> str:
    #     return str(self.bom)
    

bom = BOM()

# print(bom.__dict__['bom']['hantla_do_cwiczen']['ciezarki'])