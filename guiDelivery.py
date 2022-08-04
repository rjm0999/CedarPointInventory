from constants import *
from gui import Gui


class DeliveryGui(Gui):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure_parent()
        self.configure_self()

        # self.create_listbox()

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
            idx += 1

        lb = tk.Listbox(self, listvariable=tk.StringVar(value=list_var), font=(FONT, 20))
        lb.grid(row=0, column=0, sticky=tk.NSEW, padx=50, pady=50)

        lb.bind("<<ListboxSelect>>", lambda e: self.listbox_change(lb))

    def listbox_change(self, lb):
        pass
