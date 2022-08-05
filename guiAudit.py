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
