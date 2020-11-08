
from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

data_gui = Tk()
data_gui.title("My Cryptocurrency Portfolio")

data_gui.iconbitmap("favicon.ico")

con = sqlite3.connect("coin.db")
cObj = con.cursor()

cObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()


# Resets the application by destroying each frame then rebuilding it
def reset():
    for cell in data_gui.winfo_children():
        cell.destroy()

    app_navigation()
    app_header()
    my_portfolio()


# Creates a navigation system

def app_navigation():
    def clear_all():
        cObj.execute("delete from coin")
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Portfolio Cleared")
        reset()

    def close_app():
        data_gui.destroy()

    menu = Menu(data_gui)
    file_item = Menu(menu)
    file_item.add_command(label="Clear Portfolio", command=clear_all)
    file_item.add_command(label="Close App", command=close_app)
    # Little Easter egg that says "Hello Papa"
    # hi_papa = Menu(menu)
    # hi_papa.add_command(label="HELLO PAPA", )
    menu.add_cascade(label="File", menu=file_item)
    # menu.add_cascade(label="Hi Papa", menu=hi_papa)
    data_gui.config(menu=menu)


def my_portfolio():
    api_request = requests.get(
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=9c541bed-c932-4b79-880a-8aa09bf88602")

    api = json.loads(api_request.content)

    cObj.execute("SELECT * FROM coin")
    coins = cObj.fetchall()

    def font_color(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"

    def insert_coin():
        cObj.execute("insert into coin(symbol, price, amount) VALUES (?,?,?)",
                     (symbol_txt.get(), price_txt.get(), amount_txt.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin Added Successfully!")
        reset()

    def update_coin():
        cObj.execute("update coin set symbol=?, price=?, amount=? where id =?",
                     (symbol_update.get(), price_update.get(), amount_update.get(), port_id_update.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin Updated Successfully!")
        reset()

    def delete_coin():
        cObj.execute("delete from coin where id=?", (port_id_delete.get(),))
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin Deleted Successfully!")
        reset()

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0, 300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_per_coin = (api["data"][i]["quote"]["USD"]["price"] - coin[3])
                total_pl_coin = pl_per_coin * coin[2]

                total_pl += total_pl_coin
                total_current_value += current_value
                total_amount_paid += total_paid

                # Commented out because we don't need anymore but safe to keep previous operations

                # print(api["data"][i]["name"] + " - " + api["data"][i]["symbol"])
                # print("Current value - ${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("Amount owned of", coin[1], " - ", coin[2], "at", "$", coin[3])
                # print("Total Paid for", coin[1], "=", "${0:.2f}".format(total_paid))
                # print("Current value of", coin[1], "=", "${0:.2f}".format(current_value))
                # print("Amount gained/lost per coin = ", "${0:.2f}".format(pl_per_coin))
                # print("Total amount gained/lost = ", "${0:.2f}".format(total_pl_coin))
                # print("--------------")####

                portfolio_id = Label(data_gui, text=coin[0], bg="#F3F4F6", fg="black", font="Lato 12",
                                     padx="5", pady="5", borderwidth=2, relief="groove")
                portfolio_id.grid(row=coin_row, column=0, sticky=N + S + E + W)

                name = Label(data_gui, text=api["data"][i]["symbol"], bg="#F3F4F6", fg="black", font="Lato 12",
                             padx="5", pady="5", borderwidth=2, relief="groove")
                name.grid(row=coin_row, column=1, sticky=N + S + E + W)

                price = Label(data_gui, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6",
                              fg="black", font="Lato 12", padx="5", pady="5", borderwidth=2, relief="groove")
                price.grid(row=coin_row, column=2, sticky=N + S + E + W)

                no_coins = Label(data_gui, text=coin[2], bg="#F3F4F6", fg="black", font="Lato 12", padx="5", pady="5",
                                 borderwidth=2, relief="groove")
                no_coins.grid(row=coin_row, column=3, sticky=N + S + E + W)

                amount_paid = Label(data_gui, text="${0:.2f}".format(total_paid), bg="#F3F4F6", fg="black",
                                    font="Lato 12", padx="5", pady="5", borderwidth=2, relief="groove")
                amount_paid.grid(row=coin_row, column=4, sticky=N + S + E + W)

                current_val = Label(data_gui, text="${0:.2f}".format(current_value), bg="#F3F4F6", fg="black",
                                    font="Lato 12", padx="5", pady="5", borderwidth=2, relief="groove")
                current_val.grid(row=coin_row, column=5, sticky=N + S + E + W)

                pl_coin = Label(data_gui, text="${0:.2f}".format(pl_per_coin), bg="#F3F4F6",
                                fg=font_color(float("{0:.2f}".format(pl_per_coin))), font="Lato 12", padx="5", pady="5",
                                borderwidth=2, relief="groove")
                pl_coin.grid(row=coin_row, column=6, sticky=N + S + E + W)

                total_prof_loss = Label(data_gui, text="${0:.2f}".format(total_pl_coin), bg="#F3F4F6",
                                        fg=font_color(float("{0:.2f}".format(total_pl_coin))), font="Lato 12", padx="5",
                                        pady="5", borderwidth=2, relief="groove")
                total_prof_loss.grid(row=coin_row, column=7, sticky=N + S + E + W)

                coin_row += 1
    ### How to insert data
    symbol_txt = Entry(data_gui, borderwidth=2, relief="groove")
    symbol_txt.grid(row=coin_row + 1, column=1)

    price_txt = Entry(data_gui, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row + 1, column=2)

    amount_txt = Entry(data_gui, borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row + 1, column=3)
    ##############################################################

    # Add Coin

    add_coin = Button(data_gui, text="Add Coin", bg="#142E54", fg="black", command=insert_coin, font="Lato 12 bold",
                      padx="5", pady="5",
                      borderwidth=2, relief="groove")
    add_coin.grid(row=coin_row + 1, column=4, sticky=N + S + E + W)

    # Update Coin

    port_id_update = Entry(data_gui, borderwidth=2, relief="groove")
    port_id_update.grid(row=coin_row + 2, column=0)

    symbol_update = Entry(data_gui, borderwidth=2, relief="groove")
    symbol_update.grid(row=coin_row + 2, column=1)

    price_update = Entry(data_gui, borderwidth=2, relief="groove")
    price_update.grid(row=coin_row + 2, column=2)

    amount_update = Entry(data_gui, borderwidth=2, relief="groove")
    amount_update.grid(row=coin_row + 2, column=3)

    update_coin_txt = Button(data_gui, text="Update Coin", bg="#142E54", fg="black", command=update_coin,
                             font="Lato 12 bold",
                             padx="5", pady="5",
                             borderwidth=2, relief="groove")
    update_coin_txt.grid(row=coin_row + 2, column=4, sticky=N + S + E + W)

    # Delete coin

    port_id_delete = Entry(data_gui, borderwidth=2, relief="groove")
    port_id_delete.grid(row=coin_row + 3, column=0)

    delete_coin_txt = Button(data_gui, text="Delete Coin", bg="#142E54", fg="black", command=delete_coin,
                             font="Lato 12 bold",
                             padx="5", pady="5",
                             borderwidth=2, relief="groove")
    delete_coin_txt.grid(row=coin_row + 3, column=4, sticky=N + S + E + W)

    # Refresh the application

    totalap = Label(data_gui, text="${0:.2f}".format(total_amount_paid), bg="#F3F4F6", fg="black",
                    font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    totalap.grid(row=coin_row, column=4, sticky=N + S + E + W)

    totalcv = Label(data_gui, text="${0:.2f}".format(total_current_value), bg="#F3F4F6", fg="black",
                    font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    totalcv.grid(row=coin_row, column=5, sticky=N + S + E + W)

    final_prof = Label(data_gui, text="${0:.2f}".format(total_pl), bg="#F3F4F6",
                       fg=font_color(float("{0:.2f}".format(total_pl))), font="Lato 12 bold", padx="5", pady="5",
                       borderwidth=2, relief="groove")
    final_prof.grid(row=coin_row, column=7, sticky=N + S + E + W)

    api = ""

    refresh = Button(data_gui, text="Refresh", bg="#142E54", fg="black", command=reset, font="Lato 12 bold",
                     padx="5", pady="5",
                     borderwidth=2, relief="groove")
    refresh.grid(row=coin_row + 1, column=7, sticky=N + S + E + W)


# Header for the application

def app_header():
    portfolio_id = Label(data_gui, text="Portfolio ID", bg="#142E54", fg="white", font="Lato 12 bold", padx="5",
                         pady="5",
                         borderwidth=2, relief="groove")
    portfolio_id.grid(row=0, column=0, sticky=N + S + E + W)

    name = Label(data_gui, text="Coin Name", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                 borderwidth=2, relief="groove")
    name.grid(row=0, column=1, sticky=N + S + E + W)

    price = Label(data_gui, text="Price", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                  borderwidth=2, relief="groove")
    price.grid(row=0, column=2, sticky=N + S + E + W)

    no_coins = Label(data_gui, text="Coin Owned", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                     borderwidth=2, relief="groove")
    no_coins.grid(row=0, column=3, sticky=N + S + E + W)

    amount_paid = Label(data_gui, text="Total Amount Paid", bg="#142E54", fg="white", font="Lato 12 bold", padx="5",
                        pady="5", borderwidth=2, relief="groove")
    amount_paid.grid(row=0, column=4, sticky=N + S + E + W)

    current_val = Label(data_gui, text="Current value", bg="#142E54", fg="white", font="Lato 12 bold", padx="5",
                        pady="5", borderwidth=2, relief="groove")
    current_val.grid(row=0, column=5, sticky=N + S + E + W)

    pl_coin = Label(data_gui, text="P/L per Coin", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                    borderwidth=2, relief="groove")
    pl_coin.grid(row=0, column=6, sticky=N + S + E + W)

    total_pl = Label(data_gui, text="Total Coin P/L", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                     borderwidth=2, relief="groove")
    total_pl.grid(row=0, column=7, sticky=N + S + E + W)


# Calling all the functions
app_navigation()
app_header()
my_portfolio()
data_gui.mainloop()

# Closing the cursor object and the connection
cObj.close()
con.close()
