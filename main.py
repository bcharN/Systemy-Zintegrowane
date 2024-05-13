import tkinter as tk
from tkinter import ttk
import json
import pandas as pd
from MRP import MRP
from pandastable import Table, TableModel

def jsonWindow(data, filename):
    # Create a new window to display JSON data
    newWindow = tk.Toplevel()
    newWindow.title("JSON Data")
    
    # Create a text widget to display JSON data
    text_widget = tk.Text(newWindow, width=100, height=30)
    text_widget.pack()

    # Insert the JSON data into the text widget
    text_widget.insert(tk.END, json.dumps(data, indent=4))

    # Save changes to JSON file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def calculateZelazoMRP(bom, item):
    mrp_window = tk.Toplevel(root)
    mrp_window.title("MRP Table")

    na_stanie = bom[item]['params']['available']
    czas_realizacji = bom[item]['params']['lead_time']
    wielkosc_partii = bom[item]['params']['batch_size']
    calk_zap = pd.Series(data=[0,0,0,28,0,30])

    zelazoMRP = MRP(na_stanie, czas_realizacji, wielkosc_partii, calk_zap)

    mrpTable = zelazoMRP.calculate_MRP()

    row_names = ["calkowite zapotrzebowanie", "planowane przyjecia", "przewidywane na stanie", "zapotrzebowanie netto", "planowane zamowienia", "planowane przyjecie zamowien"]
    mrpTable.index = pd.Index(row_names)
    print(mrpTable.index)


    mrpTable.columns.name = "Tygodnie"
    
    table_model = TableModel(dataframe=mrpTable)

    dataframe_table = Table(mrp_window, model=table_model)
    dataframe_table.show()

def updateParameters(entries, bom, item, filename):
    bom[item]["params"]["quantity"] = entries[0].get()
    bom[item]["params"]["lead_time"] = entries[1].get()
    bom[item]["params"]["batch_size"] = entries[2].get()
    bom[item]["params"]["available"] = entries[3].get()

    with open(filename, 'w') as f:
        json.dump(bom, f)

def updateParametersOfSubitem(entries, bom, item, subitem, filename):
    bom[item][subitem]["params"]["quantity"] = entries[0].get()
    bom[item][subitem]["params"]["lead_time"] = entries[1].get()
    bom[item][subitem]["params"]["batch_size"] = entries[2].get()
    bom[item][subitem]["params"]["available"] = entries[3].get()

    with open(filename, 'w') as f:
        json.dump(bom, f)
    
    # jsonWindow(bom,filename)

def createTab(notebook, bom, item, filename):
    frame = ttk.Frame(notebook)

    label_quantity = tk.Label(frame, text=f"{item.capitalize()} Quantity:", font=("Helvetica", 12))
    label_quantity.pack()
    entry_quantity = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_quantity.insert(0, bom[item]["params"]["quantity"])
    entry_quantity.pack(pady=5)

    label_lead_time = tk.Label(frame, text=f"Lead Time [in days]: ", font=("Helvetica", 10))
    label_lead_time.pack()
    entry_lead_time = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_lead_time.insert(0, bom[item]["params"]["lead_time"])
    entry_lead_time.pack(pady=5)

    label_batch_size = tk.Label(frame, text=f"Batch Size: ", font=("Helvetica", 10))
    label_batch_size.pack()
    entry_batch_size = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_batch_size.insert(0, bom[item]["params"]["batch_size"])
    entry_batch_size.pack(pady=5)

    label_available = tk.Label(frame, text=f"Available: ", font=("Helvetica", 10))
    label_available.pack()
    entry_available = tk.Entry(frame, font=("Helvetica", 12), width=10)
    entry_available.insert(0, bom[item]["params"]["available"])
    entry_available.pack(pady=5)

    entries = [entry_quantity, entry_lead_time, entry_batch_size, entry_available]
    
    button_update = tk.Button(frame, text="Update", font=("Helvetica", 12), command=lambda: updateParameters(entries, bom, item, filename))
    button_update.pack(pady=5)

    

    if item == "ciezarki" and isinstance(bom[item], dict):
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=10, padx=10)

        subnotebook = ttk.Notebook(sub_frame)
        subnotebook.pack(fill='both', expand=True)

        for sub_item in bom[item]:
            if sub_item != "params":
                sub_tab = ttk.Frame(subnotebook)
                sub_tab.pack(fill='both', expand=True)

                sub_label_quantity = tk.Label(sub_tab, text=f"{sub_item.capitalize()} Quantity:", font=("Helvetica", 12))
                sub_label_quantity.pack()
                sub_entry_quantity = tk.Entry(sub_tab, font=("Helvetica", 12), width=10)
                sub_entry_quantity.insert(0, bom[item][sub_item]["params"]["quantity"])
                sub_entry_quantity.pack(pady=5)

                sub_label_lead_time = tk.Label(sub_tab, text=f"Lead Time [in days]:", font=("Helvetica", 10))
                sub_label_lead_time.pack()
                sub_entry_lead_time = tk.Entry(sub_tab, font=("Helvetica", 12), width=10)
                sub_entry_lead_time.insert(0, bom[item][sub_item]["params"]["lead_time"])
                sub_entry_lead_time.pack(pady=5)

                sub_label_batch_size = tk.Label(sub_tab, text=f"Batch Size:", font=("Helvetica", 10))
                sub_label_batch_size.pack()
                sub_entry_batch_size = tk.Entry(sub_tab, font=("Helvetica", 12), width=10)
                sub_entry_batch_size.insert(0, bom[item][sub_item]["params"]["batch_size"])
                sub_entry_batch_size.pack(pady=5)

                sub_label_available = tk.Label(sub_tab, text=f"Available:", font=("Helvetica", 10))
                sub_label_available.pack()
                sub_entry_available = tk.Entry(sub_tab, font=("Helvetica", 12), width=10)
                sub_entry_available.insert(0, bom[item][sub_item]["params"]["available"])
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

for item in bom['hantla_do_cwiczen']:
    createTab(notebook, bom['hantla_do_cwiczen'], item, filename)

button_mrp = tk.Button(root, text="Show MRP", font=("Helvetica", 12), command=lambda: calculateZelazoMRP(bom, item))
button_mrp.pack(pady=5)

show_json = tk.Button(root, text="Show JSON Data", font=("Helvetica", 12), command=lambda: jsonWindow(bom, filename))
show_json.pack(pady=10)

root.mainloop()
