import pandas as pd
from GHP import GHP

class MRP:
    
    calk_zap = "calkowite zapotrzebowanie"
    plan_przyj = "planowane przyjecia"
    przew_na_stn = "przewidywane na stanie"
    zapo_nett = "zapotrzebowanie netto"
    plan_zam = "planowane zamowienia"
    plan_przyj_zam = "planowane przyjecie zamowien"
        
    def __init__(self, na_stanie, czas_realizacji, wielkosc_partii, calk_zapot_list:pd.Series,  ilosc_tyg=9):
        self.ilosc_tyg = ilosc_tyg
        self.na_stanie = int(na_stanie)
        self.wielkosc_partii = int(wielkosc_partii)
        self.czas_realizacji = int(czas_realizacji)
        self.calk_zapot_list = self.parse_calk_zap_list(czl=calk_zapot_list, it=self.ilosc_tyg)
        self.mrp = self.create_dataframe(self.ilosc_tyg)
        # #LABELS
        # self.calk_zap = "calkowite zapotrzebowanie"
        # self.plan_przyj = "planowane przyjecia"
        # self.przew_na_stn = "przewidywane na stanie"
        # self.zapo_nett = "zapotrzebowanie netto"
        # self.plan_zam = "planowane zamowienia"
        # self.plan_przyj_zam = "planowane przyjecie zamowien"
        
    def parse_calk_zap_list(self,czl,it):
        czl_len = czl.size
        if czl_len == it:
            return czl
        elif czl_len < it:
            res = pd.concat([pd.Series(data=[0]),czl,pd.Series(data=[0 for x in range(0,it-czl_len)])],ignore_index=True)
            print(res)
            return res
        else:
            print("ERROR: lista całkowitego zapotrzebowania jest dłuższa niż ilość tygodni!!!")
            return czl

    def create_dataframe(self, ilosc_tyg):
        
        # calk_zap = "calkowite zapotrzebowanie"
        # plan_przyj = "planowane przyjecia"
        # przew_na_stn = "przewidywane na stanie"
        # zapo_nett = "zapotrzebowanie netto"
        # plan_zam = "planowane zamowienia"
        # plan_przyj_zam = "planowane przyjecie zamowien"
        
        empt = [0 for x in range(ilosc_tyg)]

        print(empt)

        data = {
            self.calk_zap:self.calk_zapot_list,
            self.plan_przyj:empt,
            self.przew_na_stn:empt,
            self.zapo_nett:empt,
            self.plan_zam:empt,
            self.plan_przyj_zam:empt
        }

        mrp = pd.DataFrame(data=data, index=[x for x in range(1,self.ilosc_tyg+1)], dtype="int64")        
        return mrp

    def calculate_MRP(self):
        # mrp = self.create_dataframe(ilosc_tyg)
        for aktu_tydz in range(1, self.ilosc_tyg+1):
            if aktu_tydz == 1:
                wpns = self.na_stanie # wpns <=> wczesniejsze przewidywane na stanie
            else:
                wpns = self.mrp.loc[aktu_tydz-1,self.przew_na_stn]
        
            zn = wpns - self.mrp.loc[aktu_tydz, self.calk_zap]  # zn <=> zapotrzebowanie netto (z mozliwym minusem)
            if zn < 0:
                ppz = self.wielkosc_partii # ppz <=> planowane przyjecie zamowien
                while ppz < zn:
                    ppz += self.wielkosc_partii # petla zebysmy dostali wystarczajaco produktu
                    
                self.mrp.loc[aktu_tydz, self.zapo_nett] = abs(zn)
                if aktu_tydz - self.czas_realizacji >= 1:
                    self.mrp.loc[aktu_tydz-self.czas_realizacji, self.plan_zam] = ppz
                    self.mrp.loc[aktu_tydz, self.plan_przyj_zam] = ppz
                else:
                    print("Nie wystarczy czasu!")
                    self.mrp.loc[1, self.plan_zam] = ppz
                    self.mrp.loc[1+self.czas_realizacji, self.plan_przyj_zam] = ppz
                    
                self.mrp.loc[aktu_tydz,self.przew_na_stn] = self.mrp.loc[aktu_tydz, self.plan_przyj_zam] - abs(zn)
            else:   
                self.mrp.loc[aktu_tydz, self.przew_na_stn] = zn 

        return self.mrp.transpose()
    
    def getCalkZap(self):
        print(self.mrp)
        print(f'calk zap list = : {self.calk_zapot_list}')
        # print(self.mrp.loc[:,self.calk_zap])
        # return self.mrp.loc[:,self.calk_zap].to_list()
        return self.mrp.loc[:,self.calk_zap].fillna(0).to_list()
    def recalc(self):
        self.calculate_MRP()
    def __str__(self):
        return f"{self.mrp.transpose()}"
    
    
    
    
# if __name__ == "__main__":
#     ghp_prod = GHP('5:20,7:40', '5:18,7:40', '2').get_production()
#     example_prod = pd.Series(data=[0,0,0,28,0,30])
#     mrp1 = MRP(22, 3, 40, example_prod)
#     mrp1.calculate_MRP()
#     print(mrp1.getCalkZap())
    