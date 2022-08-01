from gui import *
import logging


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

        self.sh = google_sheets_setup()
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
        # TODO audit gui -- needs: option to view old audits by date

    def order_gui(self):
        OrderGui(self)
        # TODO order gui -- needs: everything
        #                          approval for large orders (absolute limit and % limit?)

    def delivery_gui(self):
        DeliveryGui(self)
        # TODO delivery gui -- needs: buttons to add to req (go to req screen with fields already filled)

    def req_history_gui(self):
        ReqHistoryGui(self)

    def read_reqs(self):
        i = 2022
        years = []
        while i < date.today().year:
            years.append(i)
            i += 1

        indv_reqs = []
        types_dict = {"Department": int, "Date": int, "Item #": int, "Item Quantity": int}

        for i in years:
            indv_reqs.append(pd.read_csv("history/reqs/reqs" + str(i) + ".csv", index_col="Req Number")
                             .astype(dtype=types_dict, copy=False))

        try:
            indv_reqs.append(pd.read_csv("history/reqs/reqs" + str(date.today().year) + ".csv", index_col="Req Number")
                             .astype(dtype=types_dict, copy=False))
        except FileNotFoundError:
            indv_reqs.append(pd.read_csv("history/reqs/list.csv", index_col="Req Number")
                             .astype(dtype=types_dict, copy=False))

        self.reqs = pd.concat(indv_reqs, keys=years)


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
