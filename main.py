import tkinter.font

import constants
from gui import *


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        types_dict = {"Name": str, "Description": str, "Quantity": int, "Unit": str}
        self.inv = pd.read_csv("database/Inventory.csv", index_col="Number").astype(dtype=types_dict, copy=False)

        types_dict = {"Department": int, "Date": int, "Item #": int, "Item Quantity": int}
        try:
            self.reqs = pd.read_csv("history/reqs/reqs" + str(date.today().year) + ".csv", index_col="Req Number")\
                .astype(dtype=types_dict, copy=False)
        except FileNotFoundError:
            self.reqs = pd.read_csv("history/reqs/list.csv", index_col="Req Number")\
                .astype(dtype=types_dict, copy=False)

        #  TODO make back button go to last screen instead of main menu
        #
        #   self.last_gui = None

        self.title("Cedar Point Park Services Warehouse Inventory Manager")
        self.state("zoomed")
        self.grid()

        MainGui(self)

    def clear_grid(self):
        """
        Set all row and column weights in the grid of this widget to 0 in preparation for drawing guis
        """
        g = self.grid_size()

        self.columnconfigure(0, weight=0)
        self.rowconfigure(0, weight=0)

        if g[0] > 1:
            for i in range(1, g[0]):
                self.columnconfigure(i, weight=0)
        if g[1] > 1:
            for i in range(1, g[1]):
                self.rowconfigure(i, weight=0)

    def main_gui(self):
        MainGui(self)

    def inv_gui(self):
        InventoryGui(self)
        # TODO inventory gui -- needs: ability to add/remove/edit items

    def req_gui(self):
        ReqGui(self)

    def audit_gui(self):
        AuditGui(self)
        # TODO audit gui -- needs: gui-dataframe interaction
        #                          option to view old audits by date

    def order_gui(self):
        OrderGui(self)
        # TODO order gui -- needs: everything
        #                          approval for large orders (absolute limit and % limit?)

    def delivery_gui(self):
        DeliveryGui(self)
        # TODO delivery gui -- needs: buttons to add to req (go to req screen with fields already filled)

    def req_history_gui(self):
        ReqHistoryGui(self)


root = Root()
root.mainloop()
