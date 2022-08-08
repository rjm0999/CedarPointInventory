from constants import *
from gui import Gui


class DeliveryGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.del_list = []
        self.var_list = []
        self.department = tk.StringVar()
        self.entry_parent = None

        self.configure_parent()
        self.configure_self()

        self.frame_canvas()
        self.buttons()

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
        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)

    def buttons(self):
        """
        Create the buttons for the right side of the requisitions gui
        """
        frame_buttons = tk.Frame(self)

        frame_buttons.grid(row=0, column=1, sticky=tk.NSEW)

        frame_buttons.columnconfigure(0, weight=1)

        frame_buttons.rowconfigure(0, weight=1)
        frame_buttons.rowconfigure(1, weight=1)
        frame_buttons.rowconfigure(2, weight=1)
        frame_buttons.rowconfigure(3, weight=1)
        frame_buttons.rowconfigure(4, weight=1)
        frame_buttons.rowconfigure(5, weight=1)

        tk.Label(frame_buttons, text=date.today().isoformat(), font=(FONT, 25))\
            .grid(row=0, column=0, sticky=tk.NSEW, padx=(25, 50), pady=25)
        self.dropdown(frame_buttons)
        tk.Button(frame_buttons, text="Commit", font=(FONT, 25), command=self.commit)\
            .grid(row=2, column=0, sticky=tk.NSEW, padx=(25, 50), pady=25)
        tk.Button(frame_buttons, text="Add Row", font=(FONT, 25), command=self.add_row)\
            .grid(row=3, column=0, sticky=tk.NSEW, padx=(25, 50), pady=25)
        tk.Button(frame_buttons, text="History", font=(FONT, 25), command=self.parent.del_history_gui)\
            .grid(row=4, column=0, sticky=tk.NSEW, padx=(25, 50), pady=25)
        # tk.Button(frame_buttons, text="Stocking Items", font=(FONT, 25), command=self.daily_stocking)\
        #    .grid(row=5, column=0, sticky=tk.NSEW, padx=(25, 50), pady=25)

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
        dd.config(font=(FONT, 25), width=18)
        dd.grid(row=1, column=0, sticky=tk.NSEW, padx=(25, 50), pady=25)

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

        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll.set, highlightthickness=0)

        f = tk.Frame(self.entry_parent)

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
        e1.grid(row=0, column=0, padx=5, pady=10)
        e1.config(width=11)

        l1 = tk.Label(frm, text=item_name.get(), font=(FONT, 15))
        l1.grid(row=0, column=1, pady=10)
        l1.config(width=45)

        e2 = tk.Entry(frm, textvariable=num_items, font=(FONT, 15))
        e2.grid(row=0, column=2, padx=5, pady=10)
        e2.config(width=15)

        item_num.trace('w', lambda e, f, g: self.item_num_change(e1, l1))
        self.del_list.append((e1, l1, e2))

        frm.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

    def neg_item_quan(self):
        for i in self.var_list:
            try:
                if int(i[2].get()) < 0:
                    return True
            except ValueError:
                continue
        return False

    def check_blanks(self):
        for i in self.var_list:
            if (i[0].get() == "" and i[2].get() != "") or (i[2].get() == "" and i[0].get() != ""):
                return True
        return False

    def commit(self):
        """
        check inputs for errors (negative item quantity, no department selected, blank item number or quantity) and
        displays an appropriate error message, if applicable, call actually_commit if no errors are detected
        """
        if self.neg_item_quan():
            root = tk.Tk()
            root.title("That's Clear")
            tk.Label(root, text="Did you mean to enter a negative item quantity?", font=(FONT, 25)).pack()
            frm = tk.Frame(root)
            frm.pack()
            tk.Button(frm, text="Yes", command=lambda: self.on_purpose(root)).pack(side=tk.LEFT, padx=25, pady=25)
            tk.Button(frm, text="No", command=root.destroy).pack(side=tk.RIGHT, padx=25, pady=25)
        elif self.department.get() == "":
            root = tk.Tk()
            root.title("That's Clear")
            tk.Label(root, text="Please choose the department the items are being signed out to.", font=(FONT, 25))\
                .pack(padx=25, pady=25)
            tk.Button(root, text="Back", command=root.destroy, font=(FONT, 25)).pack(padx=25, pady=25)
        elif self.check_blanks():
            root = tk.Tk()
            root.title("That's Clear")
            tk.Label(root, text="You entered a line with either an item number and no quantity, or a quantity, but no"
                                " item number.", font=(FONT, 25)).pack(padx=25, pady=25)
            tk.Button(root, text="Back", command=root.destroy, font=(FONT, 25)).pack(padx=25, pady=25)
        else:
            self.actually_commit()

    def on_purpose(self, root):
        root.destroy()
        self.actually_commit()

    def actually_commit(self):
        """
        add current input as a new req and updates both the inventory and req history
        """
        self.parent.inv = self.parent.read_sheet("inv")
        self.parent.delivery = self.parent.read_sheet("del")
        try:
            for i in self.var_list:
                item_number = i[0].get()
                item_quantity = i[2].get()
                if item_quantity != "" and item_number != "":
                    self.parent.inv.at[int(item_number), "Quantity"] += int(item_quantity)
                    del_info = [len(self.parent.delivery.index) + 1,  # delivery num
                                item_number,  # item number
                                item_quantity,  # quantity
                                self.parent.inv.at[int(item_number), "Unit"],  # Unit
                                "Company",  # Company
                                str(date.toordinal(date.today()))]  # date
                    self.parent.append_row("del", del_info)
                    self.parent.delivery.loc[len(self.parent.delivery.index) + 1] = del_info
            self.parent.write_sheet("inv", self.parent.inv)
            self.parent.delivery_gui()
        except KeyError:
            root = tk.Tk()
            root.title("That's Clear")
            tk.Label(root, text="You've entered an invalid item number. Please try another item number.",
                     font=(FONT, 25)).pack(padx=25, pady=25)
            tk.Button(root, text="Back", command=root.destroy, font=(FONT, 25)).pack(padx=25, pady=25)

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


class DeliveryHistoryGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.delivery = self.parent.read_sheet("del")

        self.cb_item_num = []
        self.cb_all_items = tk.BooleanVar()
        self.cb_dept = []
        self.cb_all_depts = tk.BooleanVar()

        self.date_vars = [[tk.StringVar(value=str(date.today().month)), tk.StringVar(value=str(date.today().day)),
                           tk.StringVar(value=str(date.today().year))],
                          [tk.StringVar(value=str(date.today().month)), tk.StringVar(value=str(date.today().day)),
                           tk.StringVar(value=str(date.today().year))]]
        self.date_vals = [[range(1, 13), range(1, 32), range(2022, date.today().year + 1)],
                          [range(1, 13), range(1, 32), range(2022, date.today().year + 1)]]
        self.date_opts = [[], []]

        self.early = date.today()
        self.late = date.today()

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
        keys = self.parent.delivery.index.tolist()
        idx = 0
        while idx <= self.parent.delivery.shape[0] - 1:
            key = int(keys[idx])
            try:
                if not self.cb_item_num[self.parent.inv.index.tolist().index(self.parent.delivery["Item #"][key])]\
                   .get() and self.early.toordinal() <= self.parent.delivery["Ordinal"][key] <= self.late.toordinal():
                    item = str(self.parent.delivery["Item #"][key])
                    while len(item) < 10:
                        item += " "

                    item += str(self.parent.inv["Name"][self.parent.delivery["Item #"][key]])
                    item = item[0:40]
                    while len(item) < 45:
                        item += " "

                    item += str(self.parent.delivery["Quantity"][key])
                    while len(item) < 55:
                        item += " "

                    item += str(self.parent.delivery["Company"][key])
                    item = item[0:65]
                    while len(item) < 70:
                        item += " "

                    item += str(date.fromordinal(self.parent.delivery["Ordinal"][key]))

                    list_var.append(item)

            except IndexError:
                if self.early.toordinal() <= self.parent.delivery["Ordinal"][key] <= self.late.toordinal():
                    item = str(self.parent.delivery["Item #"][key])
                    while len(item) < 10:
                        item += " "

                    item += str(self.parent.inv["Name"][self.parent.delivery["Item #"][key]])
                    item = item[0:40]
                    while len(item) < 45:
                        item += " "

                    item += str(self.parent.delivery["Quantity"][key])
                    while len(item) < 55:
                        item += " "

                    item += str(self.parent.delivery["Company"][key])
                    while len(item) < 65:
                        item += " "

                    item += str(date.fromordinal(self.parent.delivery["Ordinal"][key]))

                    list_var.append(item)

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

        # TODO current does department, change to company?
        # canvas2 = self.create_canvas(frm, "dept", (50, 0))
        # canvas2.grid(row=1, column=0, sticky=tk.NSEW)

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
            all_items = tk.Checkbutton(parent, text="<Select/Deselect All>", variable=self.cb_all_items, onvalue=False,
                                       offvalue=True, anchor=tk.W, font=(FONT, 10))
            all_items.pack(fill=tk.BOTH, expand=True)
            self.cb_all_items.trace_add("write", lambda e, f, g: self.trace_all(self.cb_all_items, self.cb_item_num))

            idx = 0
            item_num_list = self.parent.inv.index.tolist()
            while idx < len(self.parent.inv.index):
                item_num = item_num_list[idx]
                boo = tk.BooleanVar()
                self.cb_item_num.append(boo)
                boo.trace_id = boo.trace_add("write", lambda e, f, g: self.bool_change(e, self.cb_item_num))
                text = str(item_num) + " - " + self.parent.inv["Name"][item_num]
                tk.Checkbutton(parent, text=text, variable=self.cb_item_num[idx], onvalue=False, offvalue=True,
                               anchor=tk.W, font=(FONT, 10)).pack(fill=tk.BOTH, expand=True)
                idx += 1
        elif string == "dept":
            # not used in this one TODO change to company?
            all_depts = tk.Checkbutton(parent, text="<Select/Deselect All>", variable=self.cb_all_depts, onvalue=False,
                                       offvalue=True, anchor=tk.W, font=(FONT, 10))
            all_depts.pack(fill=tk.BOTH, expand=True)
            self.cb_all_depts.trace_add("write", lambda e, f, g: self.trace_all(self.cb_all_depts, self.cb_dept))

            idx = 0
            depts_list = DEPARTMENTS.index.tolist()
            while idx < len(DEPARTMENTS.index.tolist()):
                boo = tk.BooleanVar()
                self.cb_dept.append(boo)
                boo.trace_id = boo.trace_add("write", lambda e, f, g: self.bool_change(e, self.cb_dept))
                text = str(depts_list[idx]) + " - " + DEPARTMENTS.iat[idx, 0]
                tk.Checkbutton(parent, text=text, variable=self.cb_dept[idx], onvalue=False, offvalue=True,
                               anchor=tk.W, font=(FONT, 10)).pack(fill=tk.BOTH, expand=True)
                idx += 1
        elif string == "date":
            frm = tk.Frame(parent)

            self.date_opts[0].append(tk.OptionMenu(frm, self.date_vars[0][0], "Month", *self.date_vals[0][0],
                                     command=lambda e: self.set_date()))
            self.date_opts[0][0].pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
            self.date_opts[0][0].config(width=5)

            self.date_opts[0].append(tk.OptionMenu(frm, self.date_vars[0][1], "Day", *self.date_vals[0][1],
                                     command=lambda e: self.set_date()))
            self.date_opts[0][1].pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
            self.date_opts[0][1].config(width=5)

            self.date_opts[0].append(tk.OptionMenu(frm, self.date_vars[0][2], "Year", *self.date_vals[0][2],
                                     command=lambda e: self.set_date()))
            self.date_opts[0][2].pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
            self.date_opts[0][2].config(width=5)

            frm.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

            to = tk.Frame(parent)

            self.date_opts[1].append(tk.OptionMenu(to, self.date_vars[1][0], "Month", *self.date_vals[1][0],
                                     command=lambda e: self.set_date()))
            self.date_opts[1][0].pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
            self.date_opts[1][0].config(width=5)

            self.date_opts[1].append(tk.OptionMenu(to, self.date_vars[1][1], "Day", *self.date_vals[1][1],
                                     command=lambda e: self.set_date()))
            self.date_opts[1][1].pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
            self.date_opts[1][1].config(width=5)

            self.date_opts[1].append(tk.OptionMenu(to, self.date_vars[1][2], "Year", *self.date_vals[1][2],
                                     command=lambda e: self.set_date()))
            self.date_opts[1][2].pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=25, pady=25)
            self.date_opts[1][2].config(width=5)

            to.pack(expand=True, fill=tk.BOTH, side=tk.BOTTOM)
        else:
            print("you forgot to program me, dum dum (" + string + ")")

    def bool_change(self, boo, var_list):
        # temp_list = []
        # for i in var_list:
        #     temp_list.append(str(i))
        # idx = temp_list.index(boo)
        # I don't remember what I was doing here. It seems to work fine without it

        self.lb = self.create_listbox()

    def trace_all(self, boo, var_list):
        temp = boo.get()
        for i in var_list:
            i.trace_vdelete("w", i.trace_id)
            i.set(temp)
            i.trace_id = i.trace_add("write", lambda e, f, g: self.bool_change(e, var_list))
        self.lb = self.create_listbox()

    def frame_buttons(self):
        """
        Create two buttons, one that closes the program and one that returns to the main menu, and pack them into a
        frame

        Returns
        -------
        Frm : tkinter.Frame
            Frame containing the "Main Menu" and "Quit" buttons
        """
        frm = super().frame_buttons()

        back_button = tk.Button(frm, text="Back", command=self.parent.delivery_gui, font=(FONT, 25))
        back_button.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=50, pady=50)
        back_button.config(width=1)

        return frm

    def set_date(self):
        e_day = int(self.date_vars[0][1].get())
        e_month = int(self.date_vars[0][0].get())
        e_year = int(self.date_vars[0][2].get())
        l_day = int(self.date_vars[1][1].get())
        l_month = int(self.date_vars[1][0].get())
        l_year = int(self.date_vars[1][2].get())

        self.date_vals[0][2] = range(2022, l_year + 1)
        self.date_vals[1][2] = range(e_year, date.today().year + 1)

        if e_year == l_year:
            self.date_vals[0][0] = range(1, l_month + 1)
            self.date_vals[1][0] = range(e_month, 13)
            if e_month == l_month:
                self.date_vals[0][1] = range(1, l_day + 1)
                if l_month in [1, 3, 5, 7, 8, 10, 12]:
                    self.date_vals[1][1] = range(e_day, 32)
                elif l_month in [4, 6, 9, 11]:
                    self.date_vals[1][1] = range(e_day, 31)
                elif l_month == 2:
                    if l_year % 4 == 0 and not l_year % 100 == 0:
                        self.date_vals[1][1] = range(e_day, 30)
                    else:
                        self.date_vals[1][1] = range(e_day, 29)
            else:
                if e_month in [1, 3, 5, 7, 8, 10, 12]:
                    self.date_vals[0][1] = range(1, 32)
                elif e_month in [4, 6, 9, 11]:
                    self.date_vals[0][1] = range(1, 31)
                elif e_month == 2:
                    if e_year % 4 == 0 and not e_year % 100 == 0:
                        self.date_vals[0][1] = range(1, 30)
                    else:
                        self.date_vals[0][1] = range(1, 29)

                if l_month in [1, 3, 5, 7, 8, 10, 12]:
                    self.date_vals[1][1] = range(1, 32)
                elif l_month in [4, 6, 9, 11]:
                    self.date_vals[1][1] = range(1, 31)
                elif l_month == 2:
                    if l_year % 4 == 0 and not l_year % 100 == 0:
                        self.date_vals[1][1] = range(1, 30)
                    else:
                        self.date_vals[1][1] = range(1, 29)
        else:
            self.date_vals[0][0] = range(1, 13)
            self.date_vals[1][0] = range(1, 13)

            if e_month in [1, 3, 5, 7, 8, 10, 12]:
                self.date_vals[0][1] = range(1, 32)
            elif e_month in [4, 6, 9, 11]:
                self.date_vals[0][1] = range(1, 31)
            elif e_month == 2:
                if e_year % 4 == 0 and not e_year % 100 == 0:
                    self.date_vals[0][1] = range(1, 30)
                else:
                    self.date_vals[0][1] = range(1, 29)

            if l_month in [1, 3, 5, 7, 8, 10, 12]:
                self.date_vals[1][1] = range(1, 32)
            elif l_month in [4, 6, 9, 11]:
                self.date_vals[1][1] = range(1, 31)
            elif l_month == 2:
                if l_year % 4 == 0 and not l_year % 100 == 0:
                    self.date_vals[1][1] = range(1, 30)
                else:
                    self.date_vals[1][1] = range(1, 29)

        self.early = date(e_year, e_month, e_day)
        self.late = date(l_year, l_month, l_day)

        self.update_options()
        self.create_listbox()

    def menu_command(self, tup):
        self.date_vars[tup[0]][tup[1]].set(tup[2])
        self.set_date()

    def update_options(self):
        menu = self.date_opts[0][0]["menu"]
        menu.delete(0, tk.END)
        for integer in self.date_vals[0][0]:
            string = str(integer)
            menu.add_command(label=string, command=lambda e=self, f=(0, 0, string): self.menu_command(f))

        menu = self.date_opts[0][1]["menu"]
        menu.delete(0, tk.END)
        for integer in self.date_vals[0][1]:
            string = str(integer)
            menu.add_command(label=string, command=lambda e=self, f=(0, 1, string): self.menu_command(f))

        menu = self.date_opts[0][2]["menu"]
        menu.delete(0, tk.END)
        for integer in self.date_vals[0][2]:
            string = str(integer)
            menu.add_command(label=string, command=lambda e=self, f=(0, 2, string): self.menu_command(f))

        menu = self.date_opts[1][0]["menu"]
        menu.delete(0, tk.END)
        for integer in self.date_vals[1][0]:
            string = str(integer)
            menu.add_command(label=string, command=lambda e=self, f=(1, 0, string): self.menu_command(f))

        menu = self.date_opts[1][1]["menu"]
        menu.delete(0, tk.END)
        for integer in self.date_vals[1][1]:
            string = str(integer)
            menu.add_command(label=string, command=lambda e=self, f=(1, 1, string): self.menu_command(f))

        menu = self.date_opts[1][2]["menu"]
        menu.delete(0, tk.END)
        for integer in self.date_vals[1][2]:
            string = str(integer)
            menu.add_command(label=string, command=lambda e=self, f=(1, 2, string): self.menu_command(f))
