import tkinter as tk
import pandas as pd  # pandas has a pivot table method
from datetime import date
# import googleapiclient
# TODO google api to connect to sheets

# google account info username: CedarPointInventory
#                     password: CedarPoint2022
#                     birthday: 1 January 1902

from constants import FONT
from constants import DEPARTMENTS


class Gui(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.destroy_children()

    def destroy_children(self):
        """
        Retrieve the parent of this widget and call the destroy method on all children of the parent, excluding itself
        """
        for i in self.parent.winfo_children():
            if i is not self:
                i.destroy()

    def configure_parent(self):
        """
        Call the clear_grid method on the parent object of this widget. Acts as default configure_parent for all
        classes that inherit from this one
        """
        self.parent.clear_grid()

    def frame_buttons(self):
        """
        Create two buttons, one that closes the program and one that returns to the main menu, and pack them into a
        frame

        Returns
        -------
        Frm : tkinter.Frame
            Frame containing the "Main Menu" and "Quit" buttons
        """
        frm = tk.Frame(self.parent)

        back_button = tk.Button(frm, text="Main Menu", command=self.parent.main_gui, font=(FONT, 25))
        back_button.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=50, pady=50)
        back_button.config(width=1)

        quit_button = tk.Button(frm, text="Quit", command=self.quit, font=(FONT, 25))
        quit_button.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT, padx=50, pady=50)
        quit_button.config(width=1)

        return frm


class MainGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure_parent()
        self.configure_self()

        self.buttons()

    def buttons(self):
        """
        Create the buttons that open each gui of the program and pack them into a grid
        """
        cur_inv = tk.Button(self, text="Current Inventory", command=self.parent.inv_gui, font=(FONT, 25))
        cur_inv.grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)
        cur_inv.config(width=1)

        req = tk.Button(self, text="Requisitions", command=self.parent.req_gui, font=(FONT, 25))
        req.grid(row=0, column=1, sticky=tk.NSEW, padx=50, pady=50)
        req.config(width=1)

        audit = tk.Button(self, text="Audit", command=self.parent.audit_gui, font=(FONT, 25))
        audit.grid(row=1, column=0, sticky=tk.NSEW, padx=50, pady=50)
        audit.config(width=1)

        deliveries = tk.Button(self, text="Deliveries", command=self.parent.delivery_gui, font=(FONT, 25))
        deliveries.grid(row=1, column=1, sticky=tk.NSEW, padx=50, pady=50)
        deliveries.config(width=1)

        orders = tk.Button(self, text="Orders", command=self.parent.order_gui, font=(FONT, 25))
        orders.grid(row=2, column=0, sticky=tk.NSEW, padx=50, pady=50)
        orders.config(width=1)

        quit_button = tk.Button(self, text="Quit", command=self.quit, font=(FONT, 25))
        quit_button.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=50, pady=50)
        quit_button.config(width=1)

    def configure_parent(self):
        """
        Configure the grid of the parent widget for this frame
        """
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

    def configure_self(self):
        """
        Configure the grid of this frame
        """
        self.grid(sticky=tk.NSEW)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)


class InventoryGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.item_quantity = tk.StringVar(self)
        self.item_quantity_label = None

        self.awaiting_delivery = tk.StringVar(self)
        self.awaiting_delivery_label = None

        self.configure_parent()
        self.configure_self()

        self.create_listbox()

        self.frame_entry()
        self.frame_buttons().grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        # TODO Inventory gui widgets

    def configure_parent(self):
        """
        Configure the parent widget's grid for this gui
        """
        super().configure_parent()
 
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
 
        self.parent.rowconfigure(0, weight=14)
        self.parent.rowconfigure(1, weight=1)
        # TODO configure root for inventory gui frame

    def configure_self(self):
        """
        Configure the grid for this widget
        """
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)

    def create_listbox(self):
        """
        Create a tkinter.Listbox widget for the inventory gui
        """
        lb = tk.Listbox(self, listvariable=tk.StringVar(value=self.parent.inv["Name"].values.tolist()),
                        font=(FONT, 25))
        lb.grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)
        lb.config(width=0)

        lb.bind("<<ListboxSelect>>", lambda e: self.listbox_change(lb))

    def frame_entry(self):
        """
        Create and configure the grid of a tkinter.Frame widget to hold tkinter.Label widgets
        """
        frame_entry = tk.Frame(self)

        frame_entry.grid(row=0, column=1, sticky=tk.NSEW)

        frame_entry.rowconfigure(0, weight=1)
        frame_entry.rowconfigure(1, weight=1)
        frame_entry.rowconfigure(2, weight=1)

        frame_entry.columnconfigure(0, weight=1)

        self.item_quantity_label = tk.Label(frame_entry, text="Current Inventory: ", font=(FONT, 25))
        self.item_quantity_label.grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)
        self.item_quantity_label.config(width=1)

        self.awaiting_delivery_label = tk.Label(frame_entry, text="Awaiting Delivery: ", font=(FONT, 25))
        self.awaiting_delivery_label.grid(row=1, column=0, sticky=tk.NSEW, padx=50, pady=50)
        self.awaiting_delivery_label.config(width=1)

        deliveries = tk.Button(frame_entry, text="Go to Deliveries", command=self.parent.delivery_gui, font=(FONT, 25))
        deliveries.grid(row=2, column=0, sticky=tk.NSEW, padx=50, pady=50)

    def listbox_change(self, lb):
        """
        Define behavior for when listbox selection changes

        Parameters
        ----------
        lb : tkinter.Listbox
            the listbox widget to define behavior for
        """
        self.item_quantity.set(self.parent.inv["Quantity"][self.parent.inv.index.tolist()[lb.curselection()[0]]])
        self.item_quantity_label.configure(text="Current Inventory: "+self.item_quantity.get())

        if self.parent.inv.index.tolist()[lb.curselection()[0]] in self.parent.deliveries.index.tolist():
            self.awaiting_delivery.set(self.parent.deliveries["Quantity Ordered"]
                                       [self.parent.inv.index.tolist()[lb.curselection()[0]]])
        else:
            self.awaiting_delivery.set("0")

        self.awaiting_delivery_label.configure(text="Awaiting Delivery: " + self.awaiting_delivery.get())

    # TODO add an entry widget to search listbox (only show items that contain the string in the entry box?)
    #  will also need to change how indexing in the dataframe is done if this is implemented - low priority

    # TODO add button to edit items. Need to be able to change each column of the dataframe. Store in a new dataframe,
    #  then overwrite old one (save backup of old csv?). Add a confirmation window. Make sure there aren't multiple
    #  items with the same number


class ReqGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.req_list = []
        self.var_list = []
        self.department = tk.StringVar()
        self.entry_parent = None

        self.configure_parent()
        self.configure_self()

        self.frame_canvas()
        self.buttons()

        self.frame_buttons().grid(row=1, column=0, sticky=tk.NSEW)
        # TODO reqs gui widgets

    def configure_parent(self):
        """
        Configure the grid of the parent widget for this frame
        """
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)

        self.parent.rowconfigure(0, weight=14)
        self.parent.rowconfigure(1, weight=1)
        # TODO configure root for req gui frame

    def configure_self(self):
        """
        Configure the grid of this frame
        """
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        # TODO configure req gui frame

    def buttons(self):
        """
        Create the buttons for the right side of the requisitions gui
        """
        frame_buttons = tk.Frame(self)

        frame_buttons.grid(row=0, column=1, sticky=tk.NSEW)

        frame_buttons.rowconfigure(0, weight=1)
        frame_buttons.columnconfigure(0, weight=1)
        frame_buttons.columnconfigure(1, weight=1)
        frame_buttons.columnconfigure(2, weight=1)
        frame_buttons.columnconfigure(3, weight=1)

        tk.Label(frame_buttons, text=date.today().isoformat(), font=(FONT, 25))\
            .grid(row=0, column=0, sticky=tk.NSEW, padx=(25, 0), pady=25)
        self.dropdown(frame_buttons)
        tk.Button(frame_buttons, text="Commit", font=(FONT, 25), command=self.commit)\
            .grid(row=2, column=0, sticky=tk.NSEW, padx=(25, 0), pady=25)
        tk.Button(frame_buttons, text="Add Row", font=(FONT, 25), command=self.add_row)\
            .grid(row=3, column=0, sticky=tk.NSEW, padx=(25, 0), pady=25)
        tk.Button(frame_buttons, text="History", font=(FONT, 25), command=self.parent.req_history_gui)\
            .grid(row=4, column=0, sticky=tk.NSEW, padx=(25, 0), pady=25)

    def dropdown(self, frm):
        """
        Create dropdown selection for departments for requisitions gui

        Parameter
        ---------
        frm : the parent frame to contain the dropdown
        """
        dept_list = []
        for i in DEPARTMENTS.index.tolist():
            dept_list.append(str(i) + " - " + DEPARTMENTS["Dept"][i])

        dd = tk.OptionMenu(frm, self.department, *dept_list)
        dd.config(font=(FONT, 25), width=15)
        dd.grid(row=1, column=0, sticky=tk.NSEW, padx=25, pady=25)

    def frame_canvas(self):
        """
        Create canvas to hold entry fields for requisitions gui
        """
        frame = tk.Frame(self)

        canvas = tk.Canvas(frame)
        scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)

        self.entry_parent = tk.Frame(canvas)
        self.entry_parent.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window(0, 0, anchor=tk.NW, window=self.entry_parent)
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll.set)

        f = tk.Frame(frame)

        item_num = tk.Label(f, text="Item Number", font=(FONT, 25))
        item_num.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
        item_num.config(width=10)

        item_name = tk.Label(f, text="Item Name", font=(FONT, 25))
        item_name.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=5, pady=25)
        item_name.config(width=10)

        item_quan = tk.Label(f, text="Item Quantity", font=(FONT, 25))
        item_quan.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
        item_quan.config(width=10)

        f.pack(expand=False, fill=tk.BOTH, side=tk.TOP, padx=25, pady=25)

        self.add_row()

        canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
        scroll.pack(fill=tk.Y, side=tk.RIGHT, padx=25, pady=25)

        frame.grid(row=0, column=0,  sticky=tk.NSEW)

    def add_row(self):
        """
        Add a row to the req gui and handle input to the entry widgets
        """
        frm = tk.Frame(self.entry_parent)

        item_num = tk.StringVar(self.parent)
        item_name = tk.StringVar(self.parent, value="Unknown Item Number")
        num_items = tk.StringVar(self.parent)

        self.var_list.append((item_num, item_name, num_items))

        frm.rowconfigure(0, weight=1)

        frm.columnconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)
        frm.columnconfigure(2, weight=1)

        e1 = tk.Entry(frm, textvariable=item_num, font=(FONT, 15))
        e1.grid(row=0, column=0, sticky=tk.NSEW, padx=(110, 75), pady=10)
        e1.config(width=15)

        l1 = tk.Label(frm, text=item_name.get(), font=(FONT, 15))
        l1.grid(row=0, column=1, sticky=tk.NSEW, padx=0, pady=10)
        l1.config(width=40)

        e2 = tk.Entry(frm, textvariable=num_items, font=(FONT, 15))
        e2.grid(row=0, column=2, sticky=tk.NSEW, padx=(65, 100), pady=10)
        e2.config(width=15)

        item_num.trace('w', lambda e, f, g: self.item_num_change(e1, l1))
        self.req_list.append((e1, l1, e2))

        frm.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

    def commit(self):
        """
        Update the dataframe with the information currently in the req, clear current inputs by redrawing the gui
        """
        for i in self.var_list:
            self.parent.inv.at[int(i[0].get()), "Quantity"] -= int(i[2].get())
            department = self.department.get()
            for j in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", " "]:
                department = department.replace(j, "")

            self.parent.reqs.loc[len(self.parent.reqs.index)] = [department, date.today().__str__(), i[0].get(),
                                                                 i[2].get()]
        self.parent.inv.to_csv("database/Inventory.csv")
        self.parent.reqs.to_csv("history/reqs/reqs" + str(date.today().year) + ".csv")
        # TODO figure out why commit overwrites last req instead of adding to the list
        self.parent.req_gui()

    def item_num_change(self, e1, l1):
        """
        Define behavior for when user input in an entry is changed
        :param e1: the entry widget to define behavior for
        :param l1: the label widget to change
        """
        if e1.get() != "":
            try:
                l1.config(text=self.parent.inv["Name"][int(e1.get())])
            except KeyError:
                l1.config(text="Unknown Item Number")

    # TODO be able to view req history, include pivot table type view to see usage by department


class AuditGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure_parent()
        self.configure_self()

        self.items = []

        self.canvas()

        self.frame_buttons().grid(row=1, column=0, sticky=tk.NSEW)

    def configure_parent(self):
        """
        Configure the grid of the parent widget for this frame
        """
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)

        self.parent.rowconfigure(0, weight=14)
        self.parent.rowconfigure(1, weight=1)

    def configure_self(self):
        """
        Configure the grid of this frame
        """
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.grid(row=0, column=0, sticky=tk.NSEW)

    def canvas(self):
        """
        Create a canvas to embed a frame in, so a scroll bar can be added
        """
        audit = tk.Frame(self)

        canvas = tk.Canvas(audit)
        scroll = self.scrollbar(audit, canvas)

        canvas.create_window(0, 0, anchor=tk.NW, window=self.frame_audit(canvas))
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll.set)

        canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        scroll.pack(fill=tk.Y, side=tk.RIGHT)

        audit.grid(row=0, column=0, sticky=tk.NSEW)

    def frame_audit(self, parent):
        """
        Iterate through the inventory and calls frame_entry for each item in the inventory

        Parameter
        ---------
        parent : the parent widget of the frame where the entry and label widgets are embedded
        """
        idx = 0
        frm = tk.Frame(parent)

        while idx < self.parent.inv.shape[0]:
            temp = tk.Frame(frm)
            self.items.append(self.frame_entry(temp, idx))
            temp.pack()
            idx += 1

        return frm

    def frame_entry(self, top, idx):
        """
        Create two label and two entry widgets for the item at index idx in the inventory

        Parameter
        ---------
        top - parent widget to pack the widgets in
        idx - the integer index to use to get the row label

        Return
        ------
        [wid1, wid2, wid3, text_var]
        wid1 - a label widget with an item name
        wid2 - an entry widget
        wid3 - an entry widget
        text_var - a tkinter.StringVar() object tied to a label widget, wid4
        """
        text_var = tk.StringVar()
        wid1 = tk.Label(top, text=self.parent.inv["Name"].iloc[idx], font=(FONT, 25), width=50)
        wid2 = tk.Entry(top, font=(FONT, 25))
        wid3 = tk.Entry(top, font=(FONT, 25))
        wid4 = tk.Label(top, textvariable=text_var, font=(FONT, 25))

        wid1.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
        wid2.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
        wid3.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
        wid4.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)

        return [wid1, wid2, wid3, text_var]

    @staticmethod
    def scrollbar(parent, linked_widget):
        """
        Create a scrollbar widget
        """
        scroll = tk.Scrollbar(parent, orient=tk.VERTICAL, command=linked_widget.yview)
        return scroll


class OrderGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.frame_buttons().grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        # TODO order widgets

    def configure_parent(self):
        """
        Configure the grid of the parent widget for this frame
        """
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        # TODO configure root for order gui frame

    def configure_self(self):
        """
        Configure the grid of this frame
        """
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # TODO configure order gui frame


class DeliveryGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure_parent()
        self.configure_self()

        self.create_listbox()

        self.frame_buttons().grid(row=1, column=0, sticky=tk.NSEW)

    def configure_parent(self):
        """
        Configure the grid of the parent widget for this frame
        """
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

    def configure_self(self):
        """
        Configure the grid of this frame
        """
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=14)
        self.rowconfigure(1, weight=1)

    def create_listbox(self):
        """
        Create a tkinter listbox
        """
        list_var = []
        keys = self.parent.deliveries.index.tolist()
        idx = 0
        while idx <= self.parent.deliveries.shape[0] - 1:
            key = keys[idx]
            list_var.append(self.parent.deliveries["Company"][key].__str__() + ":      " +
                            self.parent.deliveries["Name"][key].__str__() + "      " +
                            self.parent.deliveries["Quantity Ordered"][key].__str__())
            # TODO align text properly by adding whitespace
            idx += 1

        lb = tk.Listbox(self, listvariable=tk.StringVar(value=list_var), font=(FONT, 20))
        lb.grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)

        lb.bind("<<ListboxSelect>>", lambda e: self.listbox_change(lb))

    def listbox_change(self, lb):
        pass


class ReqHistoryGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.early = date(2000, 1, 1)
        self.late = date(2100, 12, 31)

        self.cb_item_num = []
        self.cb_dept = []

        self.lb = self.create_listbox()

        self.configure_parent()
        self.configure_self()

        self.filters_frame().grid(row=0, column=1, sticky=tk.NSEW)
        self.frame_buttons().grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

    def configure_parent(self):
        """
        Configure the grid of the parent widget for this frame
        """
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

    def configure_self(self):
        """
        Configure the grid of this frame
        """
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=14)
        self.rowconfigure(1, weight=1)

    def create_listbox(self):
        """
        Create a tkinter listbox
        """
        try:
            self.lb.destroy()
        except AttributeError:
            pass

        list_var = []
        keys = self.parent.reqs.index.tolist()
        idx = 0
        while idx <= self.parent.reqs.shape[0] - 1:
            key = keys[idx]
            item = self.parent.reqs["Item #"][key].__str__()
            while len(item) < 10:
                item += " "

            item += self.parent.inv["Name"][self.parent.reqs["Item #"][key]].__str__()
            item = item[0:40]
            while len(item) < 45:
                item += " "

            item += self.parent.reqs["Item Quantity"][key].__str__()
            while len(item) < 55:
                item += " "

            item += self.parent.reqs["Department"][key].__str__()
            while len(item) < 65:
                item += " "

            item += self.parent.reqs["Date"][key].__str__()

            list_var.append(item)
            # TODO align text properly by adding whitespace
            idx += 1

        lb = tk.Listbox(self, listvariable=tk.StringVar(value=list_var), font=(FONT, 20))
        lb.grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)

        return lb

    def filters_frame(self):
        frm = tk.Frame(self)
        frm.grid(row=0, column=1, sticky=tk.NSEW)

        frm.columnconfigure(0, weight=1)

        frm.rowconfigure(0, weight=1)
        frm.rowconfigure(1, weight=1)
        frm.rowconfigure(2, weight=1)

        canvas1 = self.create_canvas(frm, "itemnum", (50, 0))
        canvas1.grid(row=0, column=0, sticky=tk.NSEW)

        canvas2 = self.create_canvas(frm, "dept", (50, 0))
        canvas2.grid(row=1, column=0, sticky=tk.NSEW)

        canvas3 = self.create_canvas(frm, "date", (50, 50))
        canvas3.grid(row=2, column=0, sticky=tk.NSEW)

        return frm

    def create_canvas(self, parent, string, pady):
        frm = tk.Frame(parent)
        canvas = tk.Canvas(frm)
        frm2 = tk.Frame(canvas)
        scroll = tk.Scrollbar(frm, orient=tk.VERTICAL, command=canvas.yview)

        self.create_widgets(frm2, string)

        canvas.create_window(0, 0, anchor=tk.NW, window=frm2)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox(tk.ALL), yscrollcommand=scroll.set)

        canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=50, pady=(pady[0], pady[1]))
        scroll.pack(fill=tk.Y, side=tk.RIGHT, padx=50, pady=(pady[0], pady[1]))

        return frm

    def create_widgets(self, parent, string):
        if string == "itemnum":
            idx = 0
            while idx < len(self.parent.inv.index):
                item_num = self.parent.inv.index.tolist()[idx]
                self.cb_item_num.append(tk.BooleanVar())
                text = str(item_num) + " - " + self.parent.inv["Name"][item_num]
                tk.Checkbutton(parent, text=text, variable=self.cb_item_num[idx], onvalue=True, offvalue=False,
                               anchor=tk.W, font=(FONT, 10)).pack(fill=tk.BOTH, expand=True)
                idx += 1

        elif string == "dept":
            idx = 0
            while idx < len(DEPARTMENTS.index.tolist()):
                self.cb_dept.append(tk.BooleanVar())
                text = str(DEPARTMENTS.index.tolist()[idx]) + " - " + DEPARTMENTS.iat[idx, 0]
                tk.Checkbutton(parent, text=text, variable=self.cb_dept[idx], onvalue=True, offvalue=False,
                               anchor=tk.W, font=(FONT, 10)).pack(fill=tk.BOTH, expand=True)
                idx += 1

        elif string == "date":
            print("you forgot to program me, dum dum (date)")

        else:
            print("you forgot to program me, dum dum (" + string + ")")
