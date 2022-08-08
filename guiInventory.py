from constants import *
from gui import Gui

# TODO Make this part display more useful info, also clean it up


class InventoryGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.days_passed = 0
        self.days_left = 0

        self.item_quantity = tk.StringVar(self)
        self.item_quantity_label = None

        self.awaiting_delivery = tk.StringVar(self)
        self.awaiting_delivery_label = None

        self.year = tk.StringVar(self)
        self.year_label = None

        self.last_30 = tk.StringVar(self)
        self.last_30_label = None

        self.remaining = tk.StringVar(self)
        self.remaining_label = None

        self.configure_parent()
        self.configure_self()

        self.lb_frame = tk.Frame(self)

        self.search = tk.StringVar(self)
        # self.search.trace("w", lambda e, f, g: self.create_listbox(self.lb_frame))

        self.lb_frame.rowconfigure(0, weight=1)
        self.lb_frame.rowconfigure(1, weight=4)

        self.lb_frame.columnconfigure(0, weight=1)

        self.create_listbox(self.lb_frame)
        self.create_searchbox(self.lb_frame)
        self.lb_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.frame_entry()
        self.frame_buttons().grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

    def configure_parent(self):
        """
        Configure the parent widget's grid for this gui
        """
        super().configure_parent()

        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)

        self.parent.rowconfigure(0, weight=14)
        self.parent.rowconfigure(1, weight=1)

    def configure_self(self):
        """
        Configure the grid for this widget
        """
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)

    def create_listbox(self, parent):
        """
        Create a tkinter.Listbox widget for the inventory gui
        """
        self.parent.inv = self.parent.read_sheet("inv")

        list_var = []
        for i in self.parent.inv.index.tolist():
            # print(self.search.get().lower())
            # print(self.parent.inv["Name"][i])
            if self.search.get().lower() in self.parent.inv["Name"][i].lower() or self.search.get().lower() \
                    in self.parent.inv["Description"][i].lower():
                list_var.append(str(i) + " : " + self.parent.inv["Name"][i])

        lb = tk.Listbox(parent, listvariable=tk.StringVar(value=list_var), font=(FONT, 25))
        lb.grid(row=1, column=0, sticky=tk.NSEW, padx=25, pady=10)
        lb.config(width=0)

        lb.bind("<<ListboxSelect>>", lambda e: self.listbox_change(lb, list_var))

    def frame_entry(self):
        """
        Create and configure the grid of a tkinter.Frame widget to hold tkinter.Label widgets
        """
        wide = 30
        frame_entry = tk.Frame(self)

        frame_entry.grid(row=0, column=1, sticky=tk.NSEW)

        frame_entry.rowconfigure(0, weight=1)
        frame_entry.rowconfigure(1, weight=1)
        frame_entry.rowconfigure(2, weight=1)
        frame_entry.rowconfigure(3, weight=1)
        frame_entry.rowconfigure(4, weight=1)
        frame_entry.rowconfigure(5, weight=1)

        frame_entry.columnconfigure(0, weight=1)
        frame_entry.columnconfigure(1, weight=1)

        self.days_passed = date.today().toordinal() - date(date.today().year, 1, 1).toordinal()
        days_passed_label = tk.Label(frame_entry, text="Days since 1/1: " + str(self.days_passed), font=(FONT, 25))
        days_passed_label.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=25, pady=5)

        self.days_left = date(date.today().year, 12, 31).toordinal() - date.today().toordinal()
        days_left_label = tk.Label(frame_entry, text="Days left until 12/31: " + str(self.days_left), font=(FONT, 25))
        days_left_label.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=25, pady=5)

        self.item_quantity_label = tk.Label(frame_entry, text="Current Inventory: ", font=(FONT, 25))
        self.item_quantity_label.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=25, pady=5)
        self.item_quantity_label.config(width=wide)

        self.year_label = tk.Label(frame_entry, text="Used this year: ", font=(FONT, 25))
        self.year_label.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=25, pady=5)
        self.year_label.config(width=wide)

        self.last_30_label = tk.Label(frame_entry, text="Used in the last 30 days: ", font=(FONT, 25))
        self.last_30_label.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW, padx=25, pady=5)
        self.last_30_label.config(width=wide)

        self.remaining_label = tk.Label(frame_entry, text="Current stock will last\ndays at current rate",
                                        font=(FONT, 25))
        self.remaining_label.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW, padx=25, pady=5)
        self.remaining_label.config(width=wide)

        # TODO make a scrollable canvas and add labels for each column from spreadsheet

    def listbox_change(self, lb, list_var):
        """
        Define behavior for when listbox selection changes

        Parameters
        ----------
        lb : tkinter.Listbox
            the listbox widget to define behavior for
        list_var : List
        """

        if len(lb.curselection()) > 0:
            idx = int(list_var[lb.curselection()[0]][0:list_var[lb.curselection()[0]].index(":") - 1])

            item_quantity = self.parent.inv["Quantity"][idx]
            item_num = idx

            self.item_quantity.set(item_quantity)
            self.item_quantity_label.configure(text="Current Inventory: " + self.item_quantity.get())

            last_30 = 0
            year = 0

            for i in self.parent.reqs.index.tolist():
                if self.parent.reqs["Item #"][i] == item_num \
                   and date.fromordinal(self.parent.reqs["Ordinal"][i]).year == date.today().year:
                    year += self.parent.reqs["Amount Taken"][i]
                    if self.parent.reqs["Ordinal"][i] >= date.today().toordinal() - 30:
                        last_30 += self.parent.reqs["Amount Taken"][i]

            self.last_30.set(str(last_30))
            self.last_30_label.configure(text="Used in the last 30 days: " + self.last_30.get())

            if item_quantity != 0:
                if last_30 != 0:
                    days_left = math.floor(item_quantity / (last_30 / 30.0))
                    if days_left <= self.days_left:
                        self.remaining.set(str(days_left))
                        self.remaining_label.configure(text="Stock will last " + self.remaining.get()
                                                            + "\ndays at current rate")
                    else:
                        self.remaining_label.configure(
                            text="Stock will last until the end\nof the year at current rate")
                else:
                    self.remaining_label.configure(text="Stock will last until the end\nof the year at current rate")
            else:
                self.remaining_label.configure(text="No stock left")

            self.year.set(str(year))
            self.year_label.configure(text="Used this year: " + self.year.get())

    def create_searchbox(self, parent):
        frm = tk.Frame(parent)

        frm.rowconfigure(0, weight=1)

        frm.columnconfigure(0, weight=3)
        frm.columnconfigure(1, weight=1)

        sb = tk.Entry(frm, textvariable=self.search, font=(FONT, 25))
        sb.grid(row=0, column=0, sticky=tk.NSEW, padx=25, pady=25)

        b = tk.Button(frm, text="Search", font=(FONT, 25), command=lambda: self.create_listbox(self.lb_frame))
        b.grid(row=0, column=1, sticky=tk.NSEW, padx=25, pady=25)

        sb.bind("<Return>", lambda e: self.create_listbox(self.lb_frame))

        frm.grid(row=0, column=0, sticky=tk.NSEW)
    # TODO add button to edit items. Need to be able to change each column of the dataframe. Store in a new dataframe,
    #  then overwrite old one (save backup of old csv?). Add a confirmation window. Make sure there aren't multiple
    #  items with the same number
