import tkinter as tk
import pandas as pd
from datetime import date

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
        self.department = tk.StringVar()
        self.entry_parent = None

        self.configure_parent()
        self.configure_self()

        self.buttons()
        self.frame_canvas()

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
            .grid(row=0, column=0, sticky=tk.NSEW, padx=25, pady=25)
        self.dropdown(frame_buttons)
        tk.Button(frame_buttons, text="Commit", font=(FONT, 25))\
            .grid(row=2, column=0, sticky=tk.NSEW, padx=25, pady=25)
        tk.Button(frame_buttons, text="Add Row", font=(FONT, 25))\
            .grid(row=3, column=0, sticky=tk.NSEW, padx=25, pady=25)
        tk.Button(frame_buttons, text="History", font=(FONT, 25))\
            .grid(row=4, column=0, sticky=tk.NSEW, padx=25, pady=25)

    def dropdown(self, frm):
        """
        Create dropdown selection for departments for requisitions gui

        Parameters
        ----------
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
        self.entry_parent = tk.Frame(frame)
        frame.grid(row=0, column=0, rowspan=5, sticky=tk.NSEW)

        canvas = tk.Canvas(frame)
        scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)

        canvas.create_window(0, 0, anchor=tk.NW, window=self.entry_parent)
        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll.set)

        canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        scroll.pack(fill=tk.Y, side=tk.RIGHT)

        self.add_row()

    def add_row(self):
        frm = tk.Frame(self.entry_parent)

    # TODO have one csv with the list of dates, use that to get the file name for the corresponding req
    #      use something similar for orders/audits?


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

    # creates a canvas to embed the audit frame in so a scroll bar can be added, then packs the canvas into a frame
    # that is put into the grid of the main audit gui
    def canvas(self):
        audit = tk.Frame(self)

        canvas = tk.Canvas(audit)
        scroll = self.scrollbar(audit, canvas)

        canvas.create_window(0, 0, anchor=tk.NW, window=self.frame_audit(audit))
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll.set)

        canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        scroll.pack(fill=tk.Y, side=tk.RIGHT)

        audit.grid(row=0, column=0, sticky=tk.NSEW)

    # contains a while loop that iterates through the inventory and calls frame_entry for each item
    def frame_audit(self, parent):
        idx = 0
        frm = tk.Frame(parent)

        while idx < self.parent.inv.shape[0]:
            temp = tk.Frame(frm)
            self.items.append(self.frame_entry(temp, idx))
            temp.pack()
            idx += 1

        return frm

    # creates a label, two entry fields, and another label for the inventory item at index idx and packs it
    # into the widget passed to the method as top
    def frame_entry(self, top, idx):
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

    # creates a scroll bar with parent widget and controlling linked_widget
    @staticmethod
    def scrollbar(parent, linked_widget):
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
