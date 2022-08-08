from constants import *
from gui import Gui

# TODO approval for large orders (absolute limit and % limit?)


class OrderGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.department = tk.StringVar()

        self.configure_parent()
        self.configure_self()

        self.var_list = []
        self.req_list = []

        self.lb_list = []
        self.order_num = None

        self.lb1 = None
        self.create_lb1()

        self.lb2_frame = None
        self.lb2 = None
        self.create_lb2()

        [self.checks, self.check_vars] = self.frame_checks()
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

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def create_lb1(self):
        lb_list = []
        if self.order_num is not None:
            order = self.parent.orders.loc[self.order_num]
            if type(order["Item Num"]) is str:
                item_num = order["Item Num"].split(", ")
                quantity = order["Quantity"].split(", ")
                for i in item_num:
                    idx = item_num.index(i)
                    string = self.parent.inv["Name"][int(i)]
                    while len(string) < 50:
                        string += " "
                    string += quantity[idx]
                    lb_list.append(string)
            else:
                item_num = order["Item Num"]
                quantity = order["Quantity"]
                string = self.parent.inv["Name"][item_num]
                while len(string) < 50:
                    string += " "
                string += str(quantity)
                lb_list.append(string)

        self.lb1 = tk.Listbox(self, listvariable=tk.StringVar(value=lb_list), font=(FONT, 25))
        self.lb1.grid(row=1, column=0, sticky=tk.NSEW, padx=25, pady=10)

    def create_lb2(self):
        if self.lb2_frame is not None:
            self.lb2_frame.destroy()

        self.lb2_frame = tk.Frame(self)

        self.lb_list = []
        for i in self.parent.orders.index.tolist():
            string = str(i)
            while len(string) < 10:
                string += " "
            string += "Current Status: "
            if self.parent.orders["Built"][i] == "FALSE" or not self.parent.orders["Built"][i]:
                string += "needs assembly"
            elif self.parent.orders["Fulfilled"][i] == "FALSE" or not self.parent.orders["Fulfilled"][i]:
                string += "awaiting pickup or delivery"
            elif self.parent.orders["Req"][i] == "FALSE" or not self.parent.orders["Req"][i]:
                string += "fulfilled"
            else:
                string += "complete"
            self.lb_list.append(string)

        self.lb2_frame.rowconfigure(0, weight=1)
        self.lb2_frame.rowconfigure(1, weight=4)
        self.lb2_frame.columnconfigure(0, weight=1)

        tk.Label(self.lb2_frame, text="Order Number", font=(FONT, 25))\
            .grid(row=0, column=0, sticky=tk.NSEW, pady=(5, 0))
        self.lb2 = tk.Listbox(self.lb2_frame, listvariable=tk.StringVar(value=self.lb_list), font=(FONT, 25))
        self.lb2.grid(row=1, column=0, sticky=tk.NSEW, pady=(0, 5))

        # TODO add checkbox to show/hide completed orders

        self.lb2_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=25, pady=10)
        self.lb2.config(width=50)

        self.lb2.bind("<<ListboxSelect>>", lambda e: self.lb_change())

    def lb_change(self):
        if len(self.lb1.curselection()) != 0:
            # TODO behavior for listbox that lists items on an order. Maybe add editing capabilities here?
            pass

        if len(self.lb2.curselection()) != 0:
            string = self.lb_list[self.lb2.curselection()[0]]
            self.order_num = int(string[0:string.index(" ")])

            temp = self.parent.orders["Built"][self.order_num]
            if temp == "TRUE":
                self.check_vars[0].set(1)
            else:
                self.check_vars[0].set(0)

            temp = self.parent.orders["Fulfilled"][self.order_num]
            if temp == "TRUE":
                self.check_vars[1].set(1)
            else:
                self.check_vars[1].set(0)

            temp = self.parent.orders["Req"][self.order_num]
            if temp == "TRUE":
                self.check_vars[2].set(1)
            else:
                self.check_vars[2].set(0)

            self.create_lb1()

    def frame_checks(self):
        frm = tk.Frame(self)

        frm.rowconfigure(0, weight=1)
        frm.rowconfigure(1, weight=1)
        frm.rowconfigure(2, weight=1)
        frm.rowconfigure(3, weight=1)
        frm.rowconfigure(4, weight=1)
        frm.rowconfigure(5, weight=1)

        frm.columnconfigure(0, weight=1)

        built_var = tk.IntVar(self)
        built = tk.Checkbutton(frm, text="Built", variable=built_var, font=(FONT, 25), command=self.update_built)
        built.grid(row=0, column=0, sticky=tk.NSEW, pady=(0, 5))

        fulfilled_var = tk.IntVar(self)
        fulfilled = tk.Checkbutton(frm, text="Fulfilled", variable=fulfilled_var, font=(FONT, 25),
                                   command=self.update_fulfilled)
        fulfilled.grid(row=1, column=0, sticky=tk.NSEW, pady=5)

        req_var = tk.IntVar(self)
        req = tk.Checkbutton(frm, text="Entered in Req", variable=req_var, font=(FONT, 25), command=self.update_req)
        req.grid(row=2, column=0, sticky=tk.NSEW, pady=5)

        add = tk.Button(frm, text="Add new order", font=(FONT, 25), command=self.add_order)
        add.grid(row=3, column=0, sticky=tk.NSEW, pady=5)

        edit = tk.Button(frm, text="Edit selected order", font=(FONT, 25))
        edit.grid(row=4, column=0, sticky=tk.NSEW, pady=5)

        enter = tk.Button(frm, text="Add selected order to requisitions", font=(FONT, 25))
        enter.grid(row=5, column=0, sticky=tk.NSEW, pady=(5, 0))

        frm.grid(row=0, column=1, sticky=tk.NSEW, rowspan=2, padx=25, pady=10)

        return [[built, fulfilled, req, add, edit, enter], [built_var, fulfilled_var, req_var]]

    def update_built(self, orders=None):
        flag = False
        if len(self.lb1.curselection()) != 0:
            pass

        if len(self.lb2.curselection()) != 0:
            if orders is None:
                orders = self.parent.read_sheet("ord")
                flag = True

            orders.loc[self.order_num, "Built"] = str(bool(self.check_vars[0].get())).upper()
            self.parent.write_sheet("ord", orders) if flag else None
            self.create_lb2()
            self.lb2.select_set(orders.index.tolist().index(self.order_num))

    def update_fulfilled(self, orders=None):
        flag = False
        if len(self.lb1.curselection()) != 0:
            pass

        if len(self.lb2.curselection()) != 0:
            if orders is None:
                orders = self.parent.read_sheet("ord")
                flag = True

            if not bool(self.check_vars[0].get()):
                self.check_vars[0].set(1)
                self.update_built(orders)

            orders.loc[self.order_num, "Fulfilled"] = str(bool(self.check_vars[1].get())).upper()
            self.parent.write_sheet("ord", orders) if flag else None
            self.create_lb2()
            self.lb2.select_set(orders.index.tolist().index(self.order_num))

    def update_req(self, orders=None):
        flag = False
        if len(self.lb1.curselection()) != 0:
            pass

        if len(self.lb2.curselection()) != 0:
            if orders is None:
                orders = self.parent.read_sheet("ord")
                flag = True

            if not bool(self.check_vars[1].get()):
                self.check_vars[1].set(1)
                self.update_fulfilled(orders)

            orders.loc[self.order_num, "Req"] = str(bool(self.check_vars[2].get())).upper()
            self.parent.write_sheet("ord", orders) if flag else None
            self.create_lb2()
            self.lb2.select_set(orders.index.tolist().index(self.order_num))

    def add_order(self):
        self.frame_canvas()

    def edit_order(self):
        pass

    def enter_order(self):
        pass

    # add order stuff
    def frame_canvas(self):
        """
        Create canvas to hold entry fields for requisitions gui
        """

        root = tk.Tk()
        root.title("Add new warehouse request")
        root.state("zoomed")

        root.columnconfigure(0, weight=4)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)

        frame = tk.Frame(root)

        canvas = tk.Canvas(frame)
        scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)

        entry_parent = tk.Frame(canvas)
        entry_parent.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window(0, 0, anchor=tk.NW, window=entry_parent)
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll.set, highlightthickness=0)

        f = tk.Frame(entry_parent)

        item_num = tk.Label(f, text="Item Number", font=(FONT, 25))
        item_num.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=5, pady=25)
        item_num.config(width=11)

        item_name = tk.Label(f, text="Item Name", font=(FONT, 25))
        item_name.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, pady=25)
        item_name.config(width=35)

        item_quan = tk.Label(f, text="Item Quantity", font=(FONT, 25))
        item_quan.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=5, pady=25)
        item_quan.config(width=15)

        f.pack(expand=True, fill=tk.BOTH, side=tk.TOP, padx=25, pady=25)

        self.var_list = []

        self.add_row(entry_parent)

        canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
        scroll.pack(fill=tk.Y, side=tk.RIGHT, padx=25, pady=25)

        frame.grid(row=0, column=0, rowspan=4, sticky=tk.NSEW)

        self.dropdown(root)
        tk.Button(root, text="Add row", command=lambda: self.add_row(entry_parent), font=(FONT, 25))\
            .grid(row=1, column=1, sticky=tk.NSEW, padx=25, pady=25)
        tk.Button(root, text="Done", command=lambda: self.commit(root), font=(FONT, 25))\
            .grid(row=2, column=1, sticky=tk.NSEW, padx=25, pady=25)
        tk.Button(root, text="Cancel", command=root.destroy, font=(FONT, 25))\
            .grid(row=3, column=1, sticky=tk.NSEW, padx=25, pady=25)

    def dropdown(self, frm):
        """
        Create dropdown selection for departments for requisitions gui

        Parameter
        ---------
        frm : the parent frame to contain the dropdown
        """
        # FIXME text doesn't appear in option menu, still changes the string in the string var
        dept_list = []
        for i in self.parent.departments.index.tolist():
            dept_list.append(str(i) + " - " + self.parent.departments["Dept"][i])

        dd = tk.OptionMenu(frm, self.department, *dept_list)
        dd.config(font=(FONT, 25), width=18)
        dd.grid(row=0, column=1, sticky=tk.NSEW, padx=25, pady=25)

    def add_row(self, entry_parent):
        """
        Add a row to the req gui and handle input to the entry widgets
        """
        frm = tk.Frame(entry_parent)

        item_num = tk.StringVar(entry_parent)
        item_name = tk.StringVar(entry_parent, value="Unknown Item Number")
        num_items = tk.StringVar(entry_parent)

        self.var_list.append((item_num, item_name, num_items))

        frm.rowconfigure(0, weight=1)

        frm.columnconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)
        frm.columnconfigure(2, weight=1)

        e1 = tk.Entry(frm, textvariable=item_num, font=(FONT, 15))
        e1.grid(row=0, column=0, padx=5, pady=10)
        e1.config(width=11)

        l1 = tk.Label(frm, text=item_name.get(), font=(FONT, 15))
        l1.grid(row=0, column=1, pady=10)
        l1.config(width=45)

        e2 = tk.Entry(frm, textvariable=num_items, font=(FONT, 15))
        e2.grid(row=0, column=2, padx=5, pady=10)
        e2.config(width=15)

        item_num.trace('w', lambda e, f, g: self.item_num_change(e1, l1))
        self.req_list.append((e1, l1, e2))

        frm.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

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

    def commit(self, root):
        """
        add current input as a new order
        """
        # TODO rewrite to add to order data sheet
        self.parent.inv = self.parent.read_sheet("inv")
        self.parent.reqs = self.parent.read_sheet("req")
        try:
            department = self.department.get()
            department_num = self.department.get()
            for j in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                department = department.replace(j, "")
            for j in department:
                department_num = department_num.replace(j, "")

            item_nums = ""
            item_quantities = ""
            for i in self.var_list:
                item_number = i[0].get()
                item_quantity = i[2].get()
                if item_quantity != "" and item_number != "":
                    item_nums += item_number + ", "
                    item_quantities += item_quantity + ", "

            order_num = self.parent.orders.index.tolist()[len(self.parent.orders.index) - 1] + 1
            order_info = [order_num,  # order num
                          department_num,  # department number
                          False,  # Built
                          False,  # Fulfilled
                          False,  # Req
                          item_nums[0:-2],  # Item Numbers
                          item_quantities[0:-2]]  # Item Quantities

            self.parent.append_row("ord", order_info)
            self.parent.orders.loc[order_num] = order_info
            self.create_lb2()
            root.destroy()
        except KeyError:
            root = tk.Tk()
            root.title("That's Clear")
            tk.Label(root, text="You've entered an invalid item number. Please try another"
                                " item number.", font=(FONT, 25)).pack(padx=25, pady=25)
            tk.Button(root, text="Back", command=root.destroy, font=(FONT, 25)).pack(padx=25, pady=25)
