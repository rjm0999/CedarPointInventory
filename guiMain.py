from constants import *
from gui import Gui


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
