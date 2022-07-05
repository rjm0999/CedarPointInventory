import tkinter as tk


def clear_root():
    for i in root.winfo_children():
        i.destroy()


def button_frame():
    frm = tk.Frame(root)

    back = tk.Button(frm, text="Back", command=main_gui)
    back.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=50, pady=50)

    quit_button = tk.Button(frm, text="Quit", command=root.quit)
    quit_button.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT, padx=50, pady=50)

    return frm


def inv_listbox_update(count, test_dict, lb):
    index = lb.curselection()
    if len(index) == 1:
        count.set(test_dict[int(index[0])])


def inventory_gui():
    # destroy existing frames
    clear_root()

    # configure root grid for inventory
    root.columnconfigure(0, weight=3)
    root.columnconfigure(1, weight=2)
    root.rowconfigure(0, weight=14)
    root.rowconfigure(1, weight=1)

    # frame for listbox containing list of all items
    frm_inv_list = tk.Frame(root)
    frm_inv_list.grid(row=0, column=0, sticky=tk.NSEW)

    # Listbox
    test_list = tk.StringVar(value=[*range(1, 50, 1)].__str__())
    keys = [*range(1, 50, 1)]
    values = [*range(100, 5000, 100)]
    test_dict = {keys[i]: values[i] for i in range(len(keys))}
    lb = tk.Listbox(frm_inv_list, listvariable=test_list, height=10)
    lb.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
    count = tk.StringVar()
    lb.bind("<<ListboxSelect>>", inv_listbox_update(count, test_dict, lb))

    # frame for listing current counts and for changing count
    frm_inv_entry = tk.Frame(root)
    frm_inv_entry.grid(row=0, column=1, stick=tk.NSEW)
    tk.Label(frm_inv_entry, text="Current Inventory: "+str(count)).pack(expand=True, fill=tk.BOTH)

    # frame for back and quit buttons
    frm_buttons = button_frame()
    frm_buttons.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)


def main_gui():
    # destroy any existing frames
    clear_root()
    # configure root grid for main menu
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=0)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)

    frm = tk.Frame(root)
    frm.grid(sticky=tk.NSEW)

    frm.columnconfigure(0, weight=1)
    frm.columnconfigure(1, weight=1)

    frm.rowconfigure(0, weight=1)
    frm.rowconfigure(1, weight=1)
    frm.rowconfigure(2, weight=1)
    frm.rowconfigure(3, weight=1)

    tk.Button(frm, text="Quit", command=frm.quit)\
        .grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=50, pady=50)

    tk.Button(frm, text="Current Inventory", command=inventory_gui)\
        .grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)
    tk.Button(frm, text="Requisitions")\
        .grid(row=0, column=1, sticky=tk.NSEW, padx=50, pady=50)
    tk.Button(frm, text="Audit")\
        .grid(row=1, column=0, sticky=tk.NSEW, padx=50, pady=50)
    tk.Button(frm, text="Orders")\
        .grid(row=1, column=1, sticky=tk.NSEW, padx=50, pady=50)
    tk.Button(frm, text="Deliveries")\
        .grid(row=2, column=0, sticky=tk.NSEW, padx=50, pady=50)


if __name__ == '__main__':
    # create the root tk interpreter
    root = tk.Tk()
    root.title("Cedar Point Park Services Warehouse Inventory Manager")
    root.state("zoomed")
    root.grid()
    # draw the main menu gui
    main_gui()
    # main loop
    root.mainloop()
