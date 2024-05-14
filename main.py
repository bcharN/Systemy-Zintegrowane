import tkinter as tk
from tkinter import ttk
import json
import pandas as pd
from MRP import MRP
from GHP import GHP
from pandastable import Table, TableModel
pd.set_option('future.no_silent_downcasting', True)

def jsonWindow(data, filename):

    newWindow = tk.Toplevel()
    newWindow.title("JSON Data")
    text_widget = tk.Text(newWindow, width=100, height=30)
    text_widget.pack()
    text_widget.insert(tk.END, json.dumps(data, indent=4))
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)



def calcAllMRPs():
    mrp_window = tk.Toplevel(root)
    mrp_window.title("MRP Tables")

    # Create a canvas and a frame inside a canvas
    canvas = tk.Canvas(mrp_window)
    scroll_y = tk.Scrollbar(mrp_window, orient="vertical", command=canvas.yview)
    scroll_x = tk.Scrollbar(mrp_window, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    def createMRPTable(frame, item_name, item_data, parent_el = None, parent_output=None):
        na_stanie = item_data['params']['available']
        czas_realizacji = item_data['params']['lead_time']
        wielkosc_partii = item_data['params']['batch_size']
        calk_zap = pd.Series(data=[0,0,0,28,0,30])
    
        if parent_el == "hantla_do_cwiczen":
            tempGHP = GHP(bom['hantla_do_cwiczen']['ghp_params'])
            calk_zap = pd.Series( tempGHP.calculate_production())
        else : 
            calk_zap = bom['hantla_do_cwiczen'][parent_el]['params']['output']
        elMRP = MRP(na_stanie, czas_realizacji, wielkosc_partii, calk_zap)#bom['hantla_do_cwiczen'][parent]['params']['output'] lub ['production'] w GHP
        print(f'calk zap: {elMRP.getCalkZap()}')
        bom["hantla_do_cwiczen"][item]["params"]["output"] = elMRP.getCalkZap() 
        # with open(filename, 'w') as f:
        #     json.dump(bom, f, indent=4)
        mrpTable = elMRP.calculate_MRP()

        row_names = ["calkowite zapotrzebowanie", "planowane przyjecia", "przewidywane na stanie", "zapotrzebowanie netto", "planowane zamowienia", "planowane przyjecie zamowien"]
        mrpTable.index = pd.Index(row_names)

        table_model = TableModel(dataframe=mrpTable)
        dataframe_table = Table(frame, model=table_model)

        dataframe_table.show()

        label_table = tk.Label(frame, text=f"{item_name.capitalize()} Table", font=("Helvetica", 10))
        label_table.grid(row=0, column=0, columnspan=2, sticky="w")

    row = 0

    for item in bom['hantla_do_cwiczen']:
        if bom['hantla_do_cwiczen'][item] == "ghp_params":
            tempGHP = GHP(bom['hantla_do_cwiczen']['ghp_params'])
            parent_output = pd.Series( tempGHP.calculate_production())
            #parent_output = bom['hantla_do_cwiczen'][item]["production"]
        else:
            item_data = bom['hantla_do_cwiczen'][item]
            if 'params' in item_data:
                frame = ttk.Frame(scrollable_frame)
                frame.grid(row=row, column=0, sticky="nsew")
                label_item = tk.Label(frame, text=f"{item} MRP Table", font=("Helvetica", 12, "bold"))
                label_item.grid(row=2, column=0, columnspan=2)
                createMRPTable(frame, item, item_data,parent_el='hantla_do_cwiczen', parent_output=parent_output)
                row += 1

                ttk.Separator(scrollable_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky="ew")
                row += 1
            
            for sub_item in item_data:
                if sub_item != 'params' and 'params' in item_data[sub_item]:
                    frame = ttk.Frame(scrollable_frame)
                    frame.grid(row=row, column=0, sticky="nsew")
                    label_item = tk.Label(frame, text=f"{sub_item} MRP Table", font=("Helvetica", 12, "bold"))
                    label_item.grid(row=2, column=0, columnspan=2)
                    print(item_data)
                    createMRPTable(frame, sub_item, item_data[sub_item],parent_el=item_data)
                    row += 1

                    ttk.Separator(scrollable_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky="ew")
                    row += 1

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")

# def calculateMRP(bom, item):
#     mrp_window = tk.Toplevel(root)
#     mrp_window.title(f"MRP Table for {item.capitalize()}")

#     na_stanie = bom['hantla_do_cwiczen'][item]['params']['available']
#     czas_realizacji = bom['hantla_do_cwiczen'][item]['params']['lead_time']
#     wielkosc_partii = bom['hantla_do_cwiczen'][item]['params']['batch_size']
#     # calk_zap = bom['hantla_do_cwiczen'][item]
#     print("item: ")
#     # print(bom['hantla_do_cwiczen'][item])
#     print(item)
#     calk_zap = pd.Series(data=[0,0,0,28,0,30])

#     zelazoMRP = MRP(na_stanie, czas_realizacji, wielkosc_partii, calk_zap) #bom['hantla_do_cwiczen'][parent]['params']['output']
    
#     # bom["hantla_do_cwiczen"][item]["params"]["output"] = zelazoMRP.getCalkZap() 
#     # with open(filename, 'w') as f:
#     #     json.dump(bom, f, indent=4)
    
#     mrpTable = zelazoMRP.calculate_MRP()

#     row_names = ["calkowite zapotrzebowanie", "planowane przyjecia", "przewidywane na stanie", "zapotrzebowanie netto", "planowane zamowienia", "planowane przyjecie zamowien"]
#     mrpTable.index = pd.Index(row_names)

#     mrpTable.columns.name = "Tygodnie"
    
#     table_model = TableModel(dataframe=mrpTable)

#     dataframe_table = Table(mrp_window, model=table_model)
#     dataframe_table.show()

def updateParameters(entries, bom, item, filename):
    bom["hantla_do_cwiczen"][item]["params"]["quantity"] = int(entries[0].get())
    bom["hantla_do_cwiczen"][item]["params"]["lead_time"] = int(entries[1].get())
    bom["hantla_do_cwiczen"][item]["params"]["batch_size"] = int(entries[2].get())
    bom["hantla_do_cwiczen"][item]["params"]["available"] = int(entries[3].get())

    with open(filename, 'w') as f:
        json.dump(bom, f, indent=4)

def updateParametersOfSubitem(entries, bom, item, subitem, filename):
    bom["hantla_do_cwiczen"][item][subitem]["params"]["quantity"] = int(entries[0].get())
    bom["hantla_do_cwiczen"][item][subitem]["params"]["lead_time"] = int(entries[1].get())
    bom["hantla_do_cwiczen"][item][subitem]["params"]["batch_size"] = int(entries[2].get())
    bom["hantla_do_cwiczen"][item][subitem]["params"]["available"] = int(entries[3].get())

    with open(filename, 'w') as f:
        json.dump(bom, f, indent=4)

def updateGHP(entries, bom, filename):
    bom["hantla_do_cwiczen"]["ghp_params"]["demand"] = entries[0].get()
    bom["hantla_do_cwiczen"]["ghp_params"]["production"] = entries[1].get()
    bom["hantla_do_cwiczen"]["ghp_params"]["available"] = entries[2].get()

    with open(filename, 'w') as f:
        json.dump(bom, f, indent=4)

def createGHPTab(notebook, bom, filename):
    frame = ttk.Frame(notebook)
    label_demand = tk.Label(frame, text=f"Demand [format type: week:demand]:", font=("Helvetica", 12))
    label_demand.pack()
    entry_demand = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_demand.insert(0, bom["hantla_do_cwiczen"]["ghp_params"]["demand"])
    entry_demand.pack(pady=5)

    label_production = tk.Label(frame, text=f"Production [format type: week:production]:", font=("Helvetica", 12))
    label_production.pack()
    entry_production = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_production.insert(0, bom["hantla_do_cwiczen"]["ghp_params"]["production"])
    entry_production.pack(pady=5)

    label_available = tk.Label(frame, text=f"Available:", font=("Helvetica", 12))
    label_available.pack()
    entry_available = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_available.insert(0, bom["hantla_do_cwiczen"]["ghp_params"]["available"])
    entry_available.pack(pady=5)

    entries = [entry_demand, entry_production, entry_available]

    button_update = tk.Button(frame, text="Update GHP", font=("Helvetica", 12), command=lambda: updateGHP(entries, bom, filename))
    button_update.pack(pady=5)

    notebook.add(frame, text="GHP")

def createTab(notebook, bom, item, filename):
    frame = ttk.Frame(notebook)
    label_quantity = tk.Label(frame, text=f"{item.capitalize()} Quantity:", font=("Helvetica", 12))
    label_quantity.pack()
    entry_quantity = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_quantity.insert(0, bom["hantla_do_cwiczen"][item]["params"]["quantity"])
    entry_quantity.pack(pady=5)

    label_lead_time = tk.Label(frame, text=f"Lead Time [in days]: ", font=("Helvetica", 10))
    label_lead_time.pack()
    entry_lead_time = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_lead_time.insert(0, bom["hantla_do_cwiczen"][item]["params"]["lead_time"])
    entry_lead_time.pack(pady=5)

    label_batch_size = tk.Label(frame, text=f"Batch Size: ", font=("Helvetica", 10))
    label_batch_size.pack()
    entry_batch_size = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_batch_size.insert(0, bom["hantla_do_cwiczen"][item]["params"]["batch_size"])
    entry_batch_size.pack(pady=5)

    label_available = tk.Label(frame, text=f"Available: ", font=("Helvetica", 10))
    label_available.pack()
    entry_available = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_available.insert(0, bom["hantla_do_cwiczen"][item]["params"]["available"])
    entry_available.pack(pady=5)

    entries = [entry_quantity, entry_lead_time, entry_batch_size, entry_available]
    
    button_update = tk.Button(frame, text="Update", font=("Helvetica", 12), command=lambda: updateParameters(entries, bom, item, filename))
    button_update.pack(pady=5)

    # button_mrp = tk.Button(root, text=f"Show MRP for {item.capitalize()}", font=("Helvetica", 12), command=lambda: calculateMRP(bom, item))
    # button_mrp.pack(pady=5)

    if item == "ciezarki" and isinstance(bom["hantla_do_cwiczen"][item], dict):
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=10, padx=10)

        subnotebook = ttk.Notebook(sub_frame)
        subnotebook.pack(fill='both', expand=True)

        for sub_item in bom["hantla_do_cwiczen"][item]:
            if sub_item != "params":
                sub_tab = ttk.Frame(subnotebook)
                sub_tab.pack(fill='both', expand=True)

                sub_label_quantity = tk.Label(sub_tab, text=f"{sub_item.capitalize()} Quantity:", font=("Helvetica", 12))
                sub_label_quantity.pack()
                sub_entry_quantity = tk.Entry(sub_tab, font=("Helvetica", 12), width=10)
                sub_entry_quantity.insert(0, bom["hantla_do_cwiczen"][item][sub_item]["params"]["quantity"])
                sub_entry_quantity.pack(pady=5)

                sub_label_lead_time = tk.Label(sub_tab, text=f"Lead Time [in days]:", font=("Helvetica", 10))
                sub_label_lead_time.pack()
                sub_entry_lead_time = tk.Entry(sub_tab, font=("Helvetica", 12), width=10)
                sub_entry_lead_time.insert(0, bom["hantla_do_cwiczen"][item][sub_item]["params"]["lead_time"])
                sub_entry_lead_time.pack(pady=5)

                sub_label_batch_size = tk.Label(sub_tab, text=f"Batch Size:", font=("Helvetica", 10))
                sub_label_batch_size.pack()
                sub_entry_batch_size = tk.Entry(sub_tab, font=("Helvetica", 12), width=10)
                sub_entry_batch_size.insert(0, bom["hantla_do_cwiczen"][item][sub_item]["params"]["batch_size"])
                sub_entry_batch_size.pack(pady=5)

                sub_label_available = tk.Label(sub_tab, text=f"Available:", font=("Helvetica", 10))
                sub_label_available.pack()
                sub_entry_available = tk.Entry(sub_tab, font=("Helvetica", 12), width=10)
                sub_entry_available.insert(0, bom["hantla_do_cwiczen"][item][sub_item]["params"]["available"])
                sub_entry_available.pack(pady=5)

                sub_entries = [sub_entry_quantity, sub_entry_lead_time, sub_entry_batch_size, sub_entry_available]

                button_update_subitem = tk.Button(sub_tab, text="Update", font=("Helvetica", 12), command=lambda sub_entries=sub_entries, bom=bom, item=item, sub_item=sub_item, filename=filename: updateParametersOfSubitem(sub_entries, bom, item, sub_item, filename))
                button_update_subitem.pack(pady=5)

                subnotebook.add(sub_tab, text=sub_item.capitalize())

        notebook.add(frame, text=item.capitalize())
    else:
        notebook.add(frame, text=item.capitalize())

with open('hantla.json', 'r') as file:
    bom = json.load(file)

root = tk.Tk()
root.title("BOM Information")

notebook = ttk.Notebook(root)
notebook.pack(pady=20, padx=20)

filename = "hantla.json"

createGHPTab(notebook, bom, filename)

for item in bom['hantla_do_cwiczen']:
    if item == "ghp_params":
        continue
    else:
        createTab(notebook, bom, item, filename)

button_mrp = tk.Button(root, text=f"Show all MRPs", font=("Helvetica", 12), command=lambda: calcAllMRPs())
button_mrp.pack(pady=5)

show_json = tk.Button(root, text="Show JSON Data", font=("Helvetica", 12), command=lambda: jsonWindow(bom, filename))
show_json.pack(pady=10)

root.mainloop()
