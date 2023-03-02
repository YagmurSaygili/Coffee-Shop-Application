import socket, threading
import copy
from tkinter import messagebox

# This function basically calculates the orders taken by baristas and store them in baristas dictionary
def calculateReport():
    orders = open("orders.txt", "r")
    ordersRecord = orders.readlines()
    # Calculating which coffee is the highest value
    for line in ordersRecord:
        fields = line.split(";")
        fields[-1] = fields[-1].replace('\n', '')
        discountAmount = int(fields[1])
        fields = [item.split('-') for item in fields]
        print(discountAmount)
        # For storing which barista has the highest order
        if ('greg' in fields[2]):
            baristas['greg'] += 1
        if ('dave' in fields[2]):
            baristas['dave'] += 1
        for i in range(3, len(fields)):
            # For storing the most popular caffe
            if ('cappuccino' in fields[i][0]):
                coffes['cappuccino'] += int(fields[i][1])
            elif ('latte' in fields[i][0]):
                coffes['latte'] += int(fields[i][1])
            elif ('americano' in fields[i][0]):
                coffes['americano'] += int(fields[i][1])
            elif ('expresso' in fields[i][0]):
                coffes['expresso'] += int(fields[i][1])

            if (discountAmount > 0):
                if ('cappuccino' in fields[i][0]):
                    product_with_discountcode['cappuccino'] += int(fields[i][1])
                elif ('latte' in fields[i][0]):
                    product_with_discountcode['latte'] += int(fields[i][1])
                elif ('americano' in fields[i][0]):
                    product_with_discountcode['americano'] += int(fields[i][1])
                elif ('expresso' in fields[i][0]):
                    product_with_discountcode['expresso'] += int(fields[i][1])
                elif ('sansebastian' in fields[i][0]):
                    product_with_discountcode['sansebastian'] += int(fields[i][1])
                elif ('mosaic' in fields[i][0]):
                    product_with_discountcode['mosaic'] += int(fields[i][1])
                elif ('carrot' in fields[i][0]):
                    product_with_discountcode['carrot'] += int(fields[i][1])
                # For calculating the most popular cake with ordered expresso
            if ('expresso' in fields[i][0]):
                for i in range(3,len(fields)):
                    x = 5
                    if ( fields[i][0] == 'sansebastian'):
                        cakes_with_expereso['sansebastian'] += int(fields[i][1])
                    elif ( fields[i][0] == 'mosaic'):
                        cakes_with_expereso['mosaic'] += int(fields[i][1])
                    elif ( fields[i][0] == 'carrot'):
                        cakes_with_expereso['carrot'] += int(fields[i][1])

# creating multithreaded server
class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
        print("New connection is added")

    def run(self):
        print("Connection from ", self.clientAddress)
        # msg = "SERVER >>> Connection successful".encode()
        # self.clientSocket.send(msg)
        clientMsg = self.clientSocket.recv(1024).decode()

        while clientMsg != "CLIENT >>> TERMINATE":
            print(clientMsg)

            # getting data from server and checking login information with datafile
            loginData = clientMsg.split(";")
            if (loginData[0] == 'login'):
                for record in userRecord:
                    fields = record.split(";")

                    if fields[0] == loginData[1] and fields[1] == loginData[2]:
                        loginCheck = "loginsuccess" + ";" + fields[0] + ";" + fields[2]
                        break
                    else:
                        loginCheck = "loginfailure"

                # sending output data (login result) to client
                msg = loginCheck
                msg = (msg).encode()
                self.clientSocket.send(msg)
                clientMsg = self.clientSocket.recv(1024).decode()
            # if the data from client is about order go here
            elif (loginData[0] == 'order'):
                # initializing datas
                i = 3
                price = 0
                discountpercentage = 0
                noCode = 0
                noDisc = 0
                # for loop for getting price from data and calculate price of product accordingly
                for record in priceRecord:
                    fields = record.split(";")
                    if (len(loginData) == 3):
                        break
                    items = loginData[i].split("-")
                    if (i < len(loginData) - 1):
                        i += 1
                    if (items[0] == fields[0]):
                        price += int(items[1]) * int(fields[1])
                # if discount code is given go here
                if (loginData[2] != "nodiscountcode"):
                    # For deleting the used discount code, basically rewrites every line except the used one
                    with open("discountcodes.txt", "r") as f:
                        # read data line by line
                        data = f.readlines()
                    f.close()
                    # open file in write mode
                    with open("discountcodes.txt", "w") as f:
                        for line in data:
                            # condition for data to be deleted
                            if loginData[2] not in line.strip("\n"):
                                f.write(line)
                    f.close()
                    # checking discount codes from files
                    for discounts in discountCodeRecord:
                        code = discounts.split(";")
                        noDisc += 1

                        if (loginData[2] == code[0]):
                            discountpercentage = int(code[1])
                            discountAmount = (int(code[1]) * price) / 100
                            price -= discountAmount
                        else:
                            noCode += 1

                    f.close()
                    # giving appropriate error if discount code is invalid
                    if(noCode == noDisc):
                        messagebox.showinfo("Error !", "Invalid Discount Code, please try again")

                orderlist = copy.deepcopy(loginData)
                # \n For new line
                orderlist[0] = ("\n" + str(price) +';')
                orderlist[1] = (str(discountpercentage)+';')
                orderlist[2] = (str(loginData[1])+';')
                # For transfering the order line into desired format
                for i in range(0,len(orderlist)):
                    if (i>2 and i< len(orderlist)-1):
                        x = str(orderlist[i]+';')
                        orderlist[i] = x

                myString = ''.join(map(str,orderlist))
                print("\n",myString)

                f = open("orders.txt", "a")
                f.write(myString)
                f.close()
                # sending data to client
                msg = "orderconfirmation;" + str(price)
                msg = (msg).encode()
                self.clientSocket.send(msg)
                clientMsg = self.clientSocket.recv(1024).decode()
            # if the data from client is starting with report
            elif (loginData[0] == "report1" or "report2" or "report3" or "report4"):
                # checking each report type and sending data to client accordingly
                # after checking datas from dictionaries that we stored to calculate report accordingly
                if (loginData[0] == "report1"):
                    max_value = max(coffes)
                    print(max_value)
                    msg = "report1;" + max_value
                    msg = (msg).encode()
                    self.clientSocket.send(msg)
                    clientMsg = self.clientSocket.recv(1024).decode()
                    print("report1")
                elif (loginData[0] == "report2"):
                    max_value = max(baristas)
                    print(max_value)
                    msg = "report2;" + max_value
                    msg = (msg).encode()
                    self.clientSocket.send(msg)
                    clientMsg = self.clientSocket.recv(1024).decode()
                    print("report2")
                elif (loginData[0] == "report3"):
                    max_value = max(product_with_discountcode)
                    print(max_value)
                    msg = "report3;" + max_value
                    msg = (msg).encode()
                    self.clientSocket.send(msg)
                    clientMsg = self.clientSocket.recv(1024).decode()
                    print("report3")
                elif (loginData[0] == "report4"):
                    max_value = max(cakes_with_expereso)
                    print(max_value)
                    msg = "report4;" + max_value
                    msg = (msg).encode()
                    self.clientSocket.send(msg)
                    clientMsg = self.clientSocket.recv(1024).decode()
                    print("report4")
        # terminate connection with client
        msg = "SERVER >>> TERMINATE".encode()
        self.clientSocket.send(msg)
        print("Connection terminated - ", self.clientAddress)
        connection.close()


HOST = "127.0.0.1"
PORT = 5000

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# initializing all dictionaries for reports
def initializeDictionaries(coffes, baristas, product_with_discountcode, cakes_with_expresso):
    # Initializing barista dictionary by checking the role is barista or not
    for line in userRecord:
        fields = line.split(";")
        if ('barista' in str(fields[2] )):
            baristas[str(fields[0])] = 0

    # Since our coffes are static we can directly do this operation
    coffes['americano'] = 0
    coffes['latte'] = 0
    coffes['expresso'] = 0
    coffes['cappuccino'] = 0

    # Since we will find the most popular product order with discount code we should keep all the products in the dictionary
    product_with_discountcode['americano'] = 0
    product_with_discountcode['latte'] = 0
    product_with_discountcode['expresso'] = 0
    product_with_discountcode['cappuccino'] = 0
    product_with_discountcode['sansebastian'] = 0
    product_with_discountcode['mosaic'] = 0
    product_with_discountcode['carrot'] = 0

    # Here we just need to keep track of cakes so
    cakes_with_expresso['sansebastian'] = 0
    cakes_with_expresso['mosaic'] = 0
    cakes_with_expresso['carrot'] = 0


# opening and closing after reading all the files
try:
    users = open("users.txt", "r")
    prices = open("prices.txt", "r")
    discountCodes = open("discountcodes.txt", "r")
    orders = open("orders.txt", "r")
except IOError:
    print("Files could not be opened")
    exit(1)

userRecord = users.readlines()  # All the lines in the file stored in users variable
priceRecord = prices.readlines()  # All the lines in the file stored in prices variable
discountCodeRecord = discountCodes.readlines()  # All the lines in the file stored in discountCodes variable
orderRecord = orders.readlines()  # All the lines in the file stored in orders variable

users.close()
prices.close()
discountCodes.close()
orders.close()

coffes = {}  # Where the popularity of coffes will be hold ( key: coffename , value: number of orders )
baristas = {}  # Where the baristas and their orders will be hold  ( key: baristaname, value: number of orders that she/he has taken )
product_with_discountcode = {}  # Where the most popular product with discount code will be held (key: cakename, value: number of order)
cakes_with_expereso = {}  # Where the ordered cakes with expresso is held (key: cakename, value: number or order)

# initialize dictionaries
initializeDictionaries(coffes,baristas,product_with_discountcode,cakes_with_expereso)

# calling functions for calculating reports
calculateReport()

try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("Call to bind failed")
    exit(1)

while True:
    mySocket.listen()
    connection, address = mySocket.accept()
    newthread = ClientThread(address, connection)
    newthread.start()
