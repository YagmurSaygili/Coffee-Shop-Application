import tkinter
from tkinter import *
from tkinter import messagebox
import socket, threading


class LoginPanel(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Login")

        # ---------------------- USERNAME

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.username = Label(self.frame1, text="Username: ")
        self.username.pack(padx=5, pady=5, side=LEFT)

        self.textUsername = Entry(self.frame1, name="textUsername")
        self.textUsername.pack(padx=5, pady=5, side=LEFT)

        # ---------------------- PASSWORD

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.password = Label(self.frame2, text="Password: ")
        self.password.pack(padx=5, pady=5, side=LEFT)

        self.textPassword = Entry(self.frame2, name="textPassword")
        self.textPassword.pack(padx=5, pady=5, side=LEFT)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.loginButton = Button(self.frame3, text="Login", command=self.pressedLogin)
        self.loginButton.pack(padx=5, pady=5)

    # function for login button
    def pressedLogin(self):
        # getting inputs from user
        usernameCheck = self.textUsername.get()
        passwordCheck = self.textPassword.get()

        outString = "login;" + str(usernameCheck) + ";" + str(passwordCheck)

        while True:
            # sending data to server
            out_data = outString
            client.send(out_data.encode())

            # getting data from server
            in_data = client.recv(1024).decode()
            print("From server: ", in_data)

            # checking the data from server
            data_check = in_data.split(";")
            if (data_check[0] == "loginsuccess"):
                if (data_check[2] == "barista\n"):
                    # if the login is for barista open barista panel
                    self.master.destroy()
                    BaristaPanel(usernameCheck).mainloop()
                elif (data_check[2] == "manager"):
                    # if the login is for manager open manager panel
                    self.master.destroy()
                    ManagerPanel().mainloop()
            else:
                # error for invalid login
                messagebox.showinfo("Error !", "Invalid login, please try again")
                break



class BaristaPanel(Frame):
    def __init__(self, username):
        Frame.__init__(self)

        # login username
        self.username = username

        self.pack()
        self.master.title("Barista Panel")

        # ------------------------------------------ COFFEES

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.coffees = Label(self.frame1, text="COFFEES")
        self.coffees.pack(padx=5, pady=5)

        # ------------------------------------------ COFFEE ORDERS

        self.frame10 = Frame(self)
        self.frame10.pack(anchor=W)

        self.latteVar = tkinter.BooleanVar()
        self.latteCheckButton = Checkbutton(self.frame10, text="Latte", variable=self.latteVar)
        self.latteCheckButton.pack(padx=5, pady=5, side=tkinter.LEFT)

        self.textLatte = Entry(self.frame10, name="textLatte")
        self.textLatte.pack(padx=50, pady=5, side=RIGHT)

        self.frame2 = Frame(self)
        self.frame2.pack(anchor=W)

        self.cappuccinoVar = tkinter.BooleanVar()
        self.cappuccinoCheckButton = Checkbutton(self.frame2, text="Cappuccino", variable=self.cappuccinoVar)
        self.cappuccinoCheckButton.pack(padx=5, pady=5, side=LEFT)

        self.textCappuccino = Entry(self.frame2, name="textCappuccino")
        self.textCappuccino.pack(padx=50, pady=5, side=LEFT)

        self.frame3 = Frame(self)
        self.frame3.pack(anchor=W)

        self.americanoVar = tkinter.BooleanVar()
        self.americanoCheckButton = Checkbutton(self.frame3, text="Americano", variable=self.americanoVar)
        self.americanoCheckButton.pack(padx=5, pady=5, side=LEFT)

        self.textAmericano = Entry(self.frame3, name="textAmericano")
        self.textAmericano.pack(padx=0, pady=5, side=LEFT)

        self.frame4 = Frame(self)
        self.frame4.pack(anchor=W)

        self.expressoVar = tkinter.BooleanVar()
        self.expressoCheckButton = Checkbutton(self.frame4, text="Expresso", variable=self.expressoVar)
        self.expressoCheckButton.pack(padx=5, pady=5, side=LEFT)

        self.textExpresso = Entry(self.frame4, name="textExpresso")
        self.textExpresso.pack(padx=0, pady=5, side=LEFT)

        # ------------------------------------------ CAKES

        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5)

        self.cakes = Label(self.frame5, text="CAKES")
        self.cakes.pack(padx=5, pady=5)

        # ------------------------------------------- CAKE ORDERS

        self.frame11 = Frame(self)
        self.frame11.pack(anchor=W)

        self.sebastianVar = tkinter.BooleanVar()
        self.sebastianCheckButton = Checkbutton(self.frame11, text="San Sebastian Cheesecake", variable=self.sebastianVar)
        self.sebastianCheckButton.pack(padx=5, pady=5, side=tkinter.LEFT)

        self.textSebastian = Entry(self.frame11, name="textSebastian")
        self.textSebastian.pack(padx=0, pady=5, side=LEFT)

        self.frame6 = Frame(self)
        self.frame6.pack(anchor=W)

        self.mosaicVar = tkinter.BooleanVar()
        self.mosaicCheckButton = Checkbutton(self.frame6, text="Mosaic Cake", variable=self.mosaicVar)
        self.mosaicCheckButton.pack(padx=5, pady=5, side=LEFT)

        self.textMosaic = Entry(self.frame6, name="textMosaic")
        self.textMosaic.pack(padx=0, pady=5, side=LEFT)

        self.frame7 = Frame(self)
        self.frame7.pack(anchor=W)

        self.carrotVar = tkinter.BooleanVar()
        self.carrotCheckButton = Checkbutton(self.frame7, text="Carrot Cake", variable=self.carrotVar)
        self.carrotCheckButton.pack(padx=5, pady=5, side=LEFT)

        self.textCarrot = Entry(self.frame7, name="textCarrot")
        self.textCarrot.pack(padx=0, pady=5, side=LEFT)

        self.frame8 = Frame(self)
        self.frame8.pack(anchor=W)

        # ------------------------------------------ DISCOUNT CODE

        self.discount = Label(self.frame8, text="Discount code, if any: ")
        self.discount.pack(padx=5, pady=5, side=LEFT)

        self.textDiscount = Entry(self.frame8, name="textDiscount")
        self.textDiscount.pack(padx=5, pady=5, side=LEFT)

        # ------------------------------------------ BUTTONS

        self.frame9 = Frame(self)
        self.frame9.pack(padx=5, pady=5)

        self.createButton = Button(self.frame9, text="Create", command=self.pressedCreate, width=22)
        self.createButton.grid(row=0, column=0, sticky="NSEW")

        self.closeButton = Button(self.frame9, text="Close", command=self.pressedClose, width=22)
        self.closeButton.grid(row=0, column=1, sticky="NSEW")

    # function for creating order
    def pressedCreate(self):

        # getting inputs from user and converting them into string format
        order = "order;" + self.username
        if(self.textDiscount.get() != ""):
            order = order + ";" + self.textDiscount.get()
        else:
            order = order + ";" + "nodiscountcode"

        # getting datas from user if the checkbuttons are clicked
        # coffees
        if (self.latteVar.get()):
            order = order + ";" + "latte-" + self.textLatte.get()
        if (self.cappuccinoVar.get()):
            order = order + ";" + "cappuccino-" + self.textCappuccino.get()
        if (self.americanoVar.get()):
            order = order + ";" + "americano-" + self.textAmericano.get()
        if (self.expressoVar.get()):
            order = order + ";" + "expresso-" + self.textExpresso.get()

        # cakes
        if (self.sebastianVar.get()):
            order = order + ";" + "sansebastian-" + self.textSebastian.get()
        if (self.mosaicVar.get()):
            order = order + ";" + "mosaic-" + self.textMosaic.get()
        if (self.carrotVar.get()):
            order = order + ";" + "carrot-" + self.textCarrot.get()

        while True:
            # sending data to server
            out_data = order
            client.send(out_data.encode())

            # getting data from server
            in_data = client.recv(1024).decode()
            print("From server: ", in_data)

            # checking datas from server
            data_check = in_data.split(";")
            if (data_check[0] == "orderconfirmation"):
                # messagebox for confirmation total price
                messagebox.showinfo("Confirmation", "Total Price: "+data_check[1])
                break
            else:
                messagebox.showinfo("Error !", "Invalid order, please try again")
                break


    def pressedClose(self):
        # destroy panel
        self.master.destroy()
        # terminate server connection
        out_data = "CLIENT >>> TERMINATE"
        client.send(out_data.encode())
        client.close()


class ManagerPanel(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.pack()
        self.master.title("Manager Panel")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.report = Label(self.frame1, text="REPORTS")
        self.report.pack(padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(anchor=W)
        self.svar = StringVar(self.frame2, "1")

        # Radiobutton reports with for loops
        reports = {"(1) What is the most popular coffee overall?": "1",
                   "(2) Which barista has the highest number of orders?": "2",
                   "(3) What is the most popular product for the orders with the discount code?": "3",
                   "(4) What is the most popular cake that is bought with expresso?": "4"}

        for (text, report) in reports.items():
            self.reportButton = Radiobutton(self.frame2, text=text, variable=self.svar, value=report,)
            self.reportButton.pack(anchor=W)

        self.frame9 = Frame(self)
        self.frame9.pack(padx=5, pady=5)

        self.createButton = Button(self.frame9, text="Create", command=self.createPanel, width=67)
        self.createButton.grid(row=0, column=0, sticky="NSEW")

        self.closeButton = Button(self.frame9, text="Close", command=self.pressedClose, width=8)
        self.closeButton.grid(row=0, column=1, sticky="NSEW")

    def createPanel(self):
        # getting datas from radiobuttons
        if(self.svar.get() == "1"):
            report = "report1"
        elif(self.svar.get() == "2"):
            report = "report2"
        elif (self.svar.get() == "3"):
            report = "report3"
        elif (self.svar.get() == "4"):
            report = "report4"

        while True:
            # sending data to server
            out_data = report
            client.send(out_data.encode())

            # getting data from server
            in_data = client.recv(1024).decode()
            print("From server: ", in_data)

            # checking data from server
            # and printing with messageboxes
            data_check = in_data.split(";")
            if (data_check[0] == "report1"):
                messagebox.showinfo("Report", "Most popular coffee overall: " + data_check[1])
                break
            elif (data_check[0] == "report2"):
                messagebox.showinfo("Report", "Barista with highest number of orders: " + data_check[1])
                break
            elif (data_check[0] == "report3"):
                messagebox.showinfo("Report", "Most popular product with discount: " + data_check[1])
                break
            elif (data_check[0] == "report4"):
                messagebox.showinfo("Report", "Most popular cake bought with expresso: " + data_check[1])
                break
            else:
                messagebox.showinfo("Error !", "Invalid report, please try again")
                break

    def pressedClose(self):
        # terminate panel and connection if pressed close
        self.master.destroy()
        out_data = "CLIENT >>> TERMINATE"
        client.send(out_data.encode())
        client.close()

if __name__ == "__main__":
    # client initialization
    SERVER = "127.0.0.1"
    PORT = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    # calling login panel
    LoginPanel().mainloop()

    # closing client
    client.close()
