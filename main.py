import logging
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

    def read_sheet(self, sheet):
        if sheet == "inv":
            indices = []
            records = self.sh.worksheet("Inventory-Stock Data").get_all_records()
            for i in records:
                indices.append(i["Number"])
            return pd.DataFrame(records, index=indices)
        elif sheet == "req":
            indices = []
            records = self.sh.worksheet("Requisitions").get_all_records()
            for i in records:
                indices.append(i["Req #"])
            return pd.DataFrame(records, index=indices)
        elif sheet == "ord":
            indices = []
            records = self.sh.worksheet("Order Data").get_all_records()
            for i in records:
                indices.append(i["Order Num"])
            return pd.DataFrame(records, index=indices)
        else:
            print("uh oh, you did it wrong, ya big goof")

    def write_sheet(self, sheet, start_cell, df):
        if sheet == "inv":
            self.sh.worksheet("Inventory-Stock Data").update([df.columns.values.tolist()] + df.values.tolist())
        elif sheet == "req":
            self.sh.worksheet("Requisitions").update([df.columns.values.tolist()] + df.values.tolist())
        elif sheet == "ord":
            self.sh.worksheet("Order Data").update([df.columns.values.tolist()] + df.values.tolist())
        else:
            print("uh oh, you did it wrong, ya big goof")

    def append_row(self, sheet, list_var):
        if sheet == "req":
            self.sh.worksheet("Requisitions").append_row(list_var)
        elif sheet == "ord":
            self.sh.worksheet("Order Data").append_row(list_var)


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
