from gui import *
import pandas as pd


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.inv = pd.read_csv("Inventory.csv", index_col="Number")
        self.deliveries = pd.read_csv("Deliveries.csv", index_col="Internal Product Number")

        #  TODO make back button go to last screen instead of main menu
        #
        #   self.last_gui = None

        self.title("Cedar Point Park Services Warehouse Inventory Manager")
        self.state("zoomed")
        self.grid()

        MainGui(self)

    def clear_grid(self):
        g = self.grid_size()

        self.columnconfigure(0, weight=0)
        self.rowconfigure(0, weight=0)

        if g[0] > 1:
            for i in range(1, g[0]):
                self.columnconfigure(i, weight=0)
        if g[1] > 1:
            for i in range(1, g[0]):
                self.rowconfigure(i, weight=0)

    def main_gui(self):
        MainGui(self)

    def inv_gui(self):
        InventoryGui(self)
        # TODO inventory gui -- needs: ability to add/remove/edit items

    def req_gui(self):
        ReqGui(self)
        # TODO req gui -- needs: ability to enter a req
        #                        gui-dataframe interaction

    def audit_gui(self):
        AuditGui(self)
        # TODO audit gui -- needs: gui-dataframe interaction
        #                          option to view old audits by date

    def order_gui(self):
        OrderGui(self)
        # TODO order gui -- needs: everything
        #                          approval for large orders (absolute limit and % limit)

    def delivery_gui(self):
        DeliveryGui(self)
        # TODO delivery gui -- needs: buttons to add to req (go to req screen with fields already filled)


# TODO have an error screen that says "that's clear"


root = Root()
root.mainloop()
