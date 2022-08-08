import logging

import pandas as pd

from guiAudit import *
from guiInventory import *
from guiMain import *
from guiOrder import *
from guiDelivery import *
from guiReq import *


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.sh = google_sheets_setup()

        self.inv = self.read_sheet("inv")
        self.reqs = self.read_sheet("req")
        self.orders = self.read_sheet("ord")
        self.delivery = self.read_sheet("del")

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

    def req_gui(self):
        ReqGui(self)

    def audit_gui(self):
        AuditGui(self)

    def order_gui(self):
        OrderGui(self)

    def delivery_gui(self):
        DeliveryGui(self)

    def req_history_gui(self):
        ReqHistoryGui(self)

    def del_history_gui(self):
        DeliveryHistoryGui(self)

    def read_sheet(self, sheet):
        if sheet == "inv":
            records = self.sh.worksheet("Inventory-Stock Data")
            idx = records.col_values(1)[1:-1]
            cols = range(2, 12)
            dat = dict([(k, pd.Series(v)) for k, v in self.get_columns(records, cols).items()])
            return pd.DataFrame(data=dat, index=idx)
        elif sheet == "req":
            records = self.sh.worksheet("Requisitions")
            idx = records.col_values(1)[1:-1]
            cols = range(2, 9)
            dat = dict([(k, pd.Series(v)) for k, v in self.get_columns(records, cols).items()])
            return pd.DataFrame(data=dat, index=idx)
        elif sheet == "ord":
            records = self.sh.worksheet("Order Data")
            idx = records.col_values(1)[1:-1]
            cols = range(2, 8)
            dat = dict([(k, pd.Series(v)) for k, v in self.get_columns(records, cols).items()])
            return pd.DataFrame(data=dat, index=idx)
        elif sheet == "del":
            records = self.sh.worksheet("Deliveries")
            idx = records.col_values(1)[1:-1]
            cols = range(2, 7)
            dat = dict([(k, pd.Series(v)) for k, v in self.get_columns(records, cols).items()])
            return pd.DataFrame(data=dat, index=idx)
        else:
            print("uh oh, you did it wrong, ya big goof")

    @staticmethod
    def get_columns(ws, col_nums):
        list_var = {}
        for i in col_nums:
            temp = ws.col_values(i)
            list_var[temp[0]] = temp[1:-1]
        return list_var

    def write_sheet(self, sheet, df):
        if sheet == "inv":
            new_cols = df.columns.values.tolist().insert(0, "Number")
            new_vals = df.values.tolist()
            i = 0
            while i < len(new_vals):
                new_vals.insert(0, df.iloc[0][i])
            self.sh.worksheet("Inventory-Stock Data").update(new_cols + new_vals)
        elif sheet == "req":
            new_cols = df.columns.values.tolist().insert(0, "Req #")
            new_vals = df.values.tolist()
            i = 0
            while i < len(new_vals):
                new_vals.insert(0, df.iloc[0][i])
            self.sh.worksheet("Requisitions").update(new_cols + new_vals)
        elif sheet == "ord":
            new_cols = df.columns.values.tolist().insert(0, "Order Num")
            new_vals = df.values.tolist()
            i = 0
            while i < len(new_vals):
                new_vals.insert(0, df.iloc[0][i])
            self.sh.worksheet("Order Data").update(new_cols + new_vals)
        elif sheet == "del":
            new_cols = df.columns.values.tolist().insert(0, "Delivery #")
            new_vals = df.values.tolist()
            i = 0
            while i < len(new_vals):
                new_vals.insert(0, df.iloc[0][i])
            self.sh.worksheet("Deliveries").update(new_cols + new_vals)
        else:
            print("uh oh, you did it wrong, ya big goof")

    def append_row(self, sheet, list_var):
        if sheet == "req":
            self.sh.worksheet("Requisitions").append_row(list_var)
        elif sheet == "ord":
            self.sh.worksheet("Order Data").append_row(list_var)
        elif sheet == "del":
            self.sh.worksheet("Deliveries").append_row(list_var)

    def update_reqs(self):
        df = self.read_sheet("req")
        for i in df.index.tolist():
            if i < 0:
                pass
            else:
                pass
        # TODO run on startup, searches for reqs without a req # (i.e. reqs added manually to the sheet) and adds them
        # to the inventory
        pass


def log_exceptions(exception, value, tb):
    filename = str(datetime.now())
    filename = filename.replace(":", ".")
    filename = filename[0:19]
    filename = "error logs\\" + filename + ".txt"
    logging.basicConfig(filename=filename, encoding="utf-8")

    logging.exception("That's Clear: error of type " + str(exception)[8:-2])

    root.quit()


def google_sheets_setup():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("database/cpip-357717-25269ee2bedf.json", scope)
    client = gspread.authorize(creds)
    return client.open("Cedar Point Warehouse Inventory")


root = Root()
root.report_callback_exception = log_exceptions

root.mainloop()

# TODO change to menu bar at top of window, add ability to open a new window with a searchable list of all items. Might
#  need to look into basic multithreading to have both guis be usable. Shouldn't be too hard, since they won't be
#  talking to each other
