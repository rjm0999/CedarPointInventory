from constants import *
from gui import Gui

# TODO redo audit so it works like doing a req, but you put in the totals for each item
# TODO audit gui -- needs: option to view old audits by date


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

        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll.set, highlightthickness=0)

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

        commit = tk.Button(frm, text="Commit", command=self.commit, font=(FONT, 25))
        commit.pack(expand=True, fill=tk.BOTH, padx=(50, 0))

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
        text_var1 = tk.StringVar()
        text_var2 = tk.StringVar()
        text_var3 = tk.StringVar()

        text_var1.trace_add("write", lambda e, f, g: self.update_labels(text_var1, text_var2, text_var3))

        wid1 = tk.Label(top, text=self.parent.inv["Name"].iloc[idx], font=(FONT, 25), width=50)
        wid2 = tk.Entry(top, textvariable=text_var1, font=(FONT, 25), width=15)
        wid3 = tk.Label(top, textvariable=text_var2, font=(FONT, 25), width=5)
        wid4 = tk.Label(top, textvariable=text_var3, font=(FONT, 25), width=25)

        wid1.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
        wid2.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
        wid3.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
        wid4.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)

        return [text_var1, text_var2, text_var3]

    @staticmethod
    def scrollbar(parent, linked_widget):
        """
        Create a scrollbar widget
        """
        scroll = tk.Scrollbar(parent, orient=tk.VERTICAL, command=linked_widget.yview)
        return scroll

    def update_labels(self, tv1, tv2, tv3):
        idx = self.items.index([tv1, tv2, tv3])
        current = self.parent.inv["Quantity"].iloc[idx]

        try:
            variance = current - int(tv1.get())
            tv2.set(str(variance))
            if current != 0:
                if abs(variance/current) > 0.1:
                    tv3.set("Recount")
            else:
                tv3.set("")
        except ValueError:
            tv1.set("")
            tv2.set("")
            tv3.set("Must be a number")

    def commit(self):
        quantities = self.parent.inv["Quantity"].tolist()
        diff = [0]*168
        flag = False

        for i in self.items:
            try:
                idx = self.items.index(i)
                current = self.parent.inv["Quantity"].iloc[idx]
                quantities[idx] = int(i[0].get())
                diff[idx] = current - int(i[0].get())
            except ValueError:
                flag = True

        if flag:
            root = tk.Tk()
            root.title("That's Clear")
            tk.Label(root, text="You've left an item count blank. Items with no count will be "
                                "assumed to be correct. Click confirm to push the audit.", font=(FONT, 25)).pack()
            frm = tk.Frame(root)
            frm.pack()
            tk.Button(frm, text="Back", command=self.destroy).pack(side=tk.LEFT, padx=25, pady=25)
            tk.Button(frm, text="Confirm", command=lambda: self.confirm(diff, root=root)) \
                .pack(side=tk.LEFT, padx=25, pady=25)
        else:
            self.confirm(diff)

    def confirm(self, diff, root=None):
        self.parent.write_sheet("inv", self.parent.inv)
        diff.insert(0, date.today().toordinal())
        diff.insert(0, "Drag formula from above!")
        self.parent.append_row("aud", diff)
        if root is not None:
            root.destroy()
