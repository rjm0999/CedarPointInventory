import tkinter as tk
# import pandas as pd


class Gui(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.destroy_children()

    # destroys all widgets that have the same parent as self, excluding self (alternate name - fratricide)
    def destroy_children(self):
        for i in self.parent.winfo_children():
            if i is not self:
                i.destroy()

    # base function to configure the parent widget in preparation for drawing the gui
    def configure_parent(self):
        self.parent.clear_grid()

    # creates main menu and quit buttons for this window
    def frame_buttons(self):
        frm = tk.Frame(self.parent)

        back_button = tk.Button(frm, text="Main Menu", command=self.parent.main_gui, font=("Arial", 25))
        back_button.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=50, pady=50)

        quit_button = tk.Button(frm, text="Quit", command=self.quit, font=("Arial", 25))
        quit_button.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT, padx=50, pady=50)

        return frm


class MainGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure_parent()
        self.configure_self()

        self.buttons()

    # creates the buttons for inventory, orders, requisitions, audits, and quitting the program
    def buttons(self):
        tk.Button(self, text="Quit", command=self.quit, font=("Arial", 25)) \
            .grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=50, pady=50)
        tk.Button(self, text="Current Inventory", command=lambda: self.parent.inv_gui(), font=("Arial", 25)) \
            .grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)
        tk.Button(self, text="Requisitions", command=lambda: self.parent.req_gui(), font=("Arial", 25)) \
            .grid(row=0, column=1, sticky=tk.NSEW, padx=50, pady=50)
        tk.Button(self, text="Audit", command=lambda: self.parent.audit_gui(), font=("Arial", 25)) \
            .grid(row=1, column=0, sticky=tk.NSEW, padx=50, pady=50)
        tk.Button(self, text="Orders", command=lambda: self.parent.order_gui(), font=("Arial", 25)) \
            .grid(row=1, column=1, sticky=tk.NSEW, padx=50, pady=50)

    # configures the grid of the parent widget for this frame
    def configure_parent(self):
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

    # configures grid for this frame
    def configure_self(self):
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

        self.on_order = tk.StringVar(self)
        self.on_order_label = None

        self.configure_parent()
        self.configure_self()

        self.create_listbox()

        self.frame_entry()
        self.frame_buttons().grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        # TODO Inventory gui widgets

    # configure root window for inventory gui
    def configure_parent(self):
        super().configure_parent()
 
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
 
        self.parent.rowconfigure(0, weight=14)
        self.parent.rowconfigure(1, weight=1)
        # TODO configure root for inventory gui frame

    # configure grid on inventory gui
    def configure_self(self):
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=19)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        # TODO configure inventory gui frame - figure out why right side of screen is so much larger than left

    # creates the listbox for the inventory gui
    def create_listbox(self):
        lb = tk.Listbox(self, listvariable=tk.StringVar(value=self.parent.inv["Name"].values.tolist()),
                        font=("Arial", 20))
        lb.grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)

        lb.bind("<<ListboxSelect>>", lambda e: self.listbox_change(lb))

    # creates a frame widget to hold the label widgets
    def frame_entry(self):
        frame_entry = tk.Frame(self)

        frame_entry.grid(row=0, column=1, sticky=tk.NSEW)

        frame_entry.rowconfigure(0, weight=1)
        frame_entry.rowconfigure(1, weight=1)
        frame_entry.rowconfigure(2, weight=1)
        frame_entry.rowconfigure(3, weight=1)

        frame_entry.columnconfigure(0, weight=1)

        self.item_quantity_label = tk.Label(frame_entry, text="Current Inventory: ", font=("Arial", 25))
        self.item_quantity_label.grid(row=0, column=0, sticky=tk.NSEW)

        self.frame_on_order(frame_entry)

    # create a frame to hold the order label and order buttons
    def frame_on_order(self, frame):
        frame_oo = tk.Frame(frame)
        frame_oo.grid(row=1, column=0, sticky=tk.NSEW)

        self.on_order_label = tk.Label(frame_oo, text="On Order: ", font=("Arial", 25))
        self.on_order_label.pack(expand=True, side=tk.LEFT, padx=50, pady=50)

        tk.Button(frame_oo, text="Go to Orders", command=self.parent.order_gui, font=("Arial", 25))\
            .pack(expand=True, side=tk.LEFT, padx=50, pady=50)

    # define behavior for when listbox selection changes
    def listbox_change(self, lb):
        self.item_quantity.set(self.parent.inv["Quantity"][list(self.parent.inv.index)[lb.curselection()[0]]])
        self.item_quantity_label.configure(text="Current Inventory: "+self.item_quantity.get())

        self.on_order.set(self.parent.inv["On Order"][lb.curselection()[0]])
        self.on_order_label.configure(text="On Order: " + self.on_order.get())

    # TODO add an entry widget to search listbox (only show items that contain the string in the entry box?)
    #  will also need to change how indexing in the dataframe is one if this is implemented - low priority

    # TODO add button to edit items. Need to be able to change each column of the dataframe. Store in a new dataframe,
    #  then overwrite old one (save backup of old csv?). Add a confirmation window. Make sure there aren't multiple
    #  items with the same number


class ReqGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure_parent()
        self.configure_self()

        self.frame_buttons().grid(row=0, column=0, sticky=tk.NSEW)

        # TODO reqs gui widgets

    def configure_parent(self):
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        # TODO configure root for req gui frame

    def configure_self(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # TODO configure req gui frame


class AuditGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure_parent()
        self.configure_self()

        self.items = []

        self.canvas()

        self.frame_buttons().grid(row=1, column=0, sticky=tk.NSEW)

    def configure_parent(self):
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)

        self.parent.rowconfigure(0, weight=14)
        self.parent.rowconfigure(1, weight=1)

    def configure_self(self):
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
        wid1 = tk.Label(top, text=self.parent.inv["Name"].iloc[idx], font=("Arial", 25), width=50)
        wid2 = tk.Entry(top, font=("Arial", 25))
        wid3 = tk.Entry(top, font=("Arial", 25))
        wid4 = tk.Label(top, textvariable=text_var, font=("Arial", 25))

        wid1.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=5)
        wid2.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=5)
        wid3.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=5)
        wid4.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=5)

        return [wid1, wid2, wid3, text_var]

    # creates a scroll bar with parent widget and controlling linked_widget
    @staticmethod
    def scrollbar(parent, linked_widget):
        scroll = tk.Scrollbar(parent, orient=tk.VERTICAL, command=linked_widget.yview)
        return scroll


class OrderGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure_parent()
        self.configure_self()

        self.create_listbox()

        self.frame_buttons().grid(row=1, column=0, sticky=tk.NSEW)
        # TODO order widgets

    def configure_parent(self):
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        # TODO configure root for order gui frame

    def configure_self(self):
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=14)
        self.rowconfigure(1, weight=1)
        # TODO configure order gui frame

    def create_listbox(self):
        list_var = []
        keys = list(self.parent.orders.index)
        idx = 0
        while idx <= self.parent.orders.shape[0] - 1:
            key = keys[idx]
            list_var.append(self.parent.orders["Company"][key].__str__() + ":      " +
                            self.parent.orders["Name"][key].__str__() + "      " +
                            self.parent.orders["Quantity Ordered"][key].__str__())
            # TODO align text properly by adding whitespace
            idx += 1

        lb = tk.Listbox(self, listvariable=tk.StringVar(value=list_var), font=("Arial", 20))
        lb.grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)

        lb.bind("<<ListboxSelect>>", lambda e: self.listbox_change(lb))

    def listbox_change(self, lb):
        pass
