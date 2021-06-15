from tkinter import *
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

tickerArray = ['MSFT','DIS','GOOG','GME','AMC','BB','CLF']
tk = Tk()
tk.configure(bg="gray")
tk.title("Stock Tickers for APES")
tk.attributes('-fullscreen', False)
frame = Frame(tk)
frame.pack

class Dashboard:
    def __init__(self):
        self.state = False
        tk.bind("<Escape>", self.toggle_fullscreen)
        self.enumerate_ticker(tickerArray)
        self.update_every_minute()


    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        tk.attributes("-fullscreen", self.state)
    
    def add_ticker(self,index,ticker):   
        stock = yf.Ticker(ticker)
        print(stock.history(period='1d', interval='2m'))
        priceArray = stock.history(period='1d',interval='2m')['Close']
        dateArray = stock.history(period='1d',interval='2m')['DateTime'] #investigate using pandas right here and then graph with matplotlib
        priceGraph = self.createGraph(priceArray,dateArray)
        openPrice = stock.history(period='1d')['Open'][0]
        currPrice = stock.history(period='1d')['Close'][0]
        difference = currPrice - openPrice

        currPriceStr = "${:,.2f}".format(currPrice)
        differenceStr = "${:,.2f}".format(difference)
        tickerName = Label(tk, text = ticker, bg="gray", fg = "white", font=("Helvetica", 30, "bold"))
        tickerPrice = Label(tk, text = currPriceStr, bg="gray", font = ("Helvetica", 24, "bold"))
        tickerDiff = Label(tk, text = differenceStr, bg="gray", font = ("Helvetica", 20, "bold italic"))

        tickerName
        self.set_label_color(tickerPrice,tickerDiff,difference)

        tickerName.grid(row = index*2, column = 0, columnspan = 4, pady = 2, sticky=NW)
        tickerPrice.grid(row = index*2, column = 1, pady = 2, padx = 164, sticky=E)
        tickerDiff.grid(row = index*2+1, column = 1, padx = 188, sticky=E)

    def set_label_color(self,labelPrice,labelDiff,difference):
        if float(difference) < 0:
            labelPrice.configure(fg="coral1")
            labelDiff.configure(fg="coral1")
        else:
            labelPrice.configure(fg="cyan")
            labelDiff.configure(fg="cyan")

    def update_every_minute(self):
        self.update_ticker_by_row()
    
    def enumerate_ticker(self,tickerIn):
        for index,ticker in enumerate(tickerIn):
            self.add_ticker(index,ticker)

    def update_ticker_by_row(self):
        for index,ticker in enumerate(tickerArray):
            tickerName = tk.grid_slaves(row=index*2,column=0)[0]
            tickerPrice = tk.grid_slaves(row=index*2,column=1)[0]
            tickerDiff = tk.grid_slaves(row=index*2+1)[0]
            self.update_ticker_item(tickerName,tickerPrice,tickerDiff)
        tk.after(10000,self.update_ticker_by_row)
    
    def update_ticker_item(self,name,priceLabel,diffLabel):
        stock = yf.Ticker(name["text"])

        openPrice = stock.history(period='1d')['Open'][0]
        currPrice = stock.history(period='1d')['Close'][0]
        difference = currPrice - openPrice
        percentChange = difference / openPrice * 100
        currPriceStr = "${:,.2f}".format(currPrice)
        differenceStr = "${:,.2f}".format(difference) + " (%{:,.2f})".format(percentChange)
        priceLabel.configure(text=currPriceStr)
        diffLabel.configure(text=differenceStr)
        
        self.set_label_color(priceLabel,diffLabel,difference)

    def createGraph(self,priceArrayIn,dateArrayIn):
        plt.plot(dateArrayIn,priceArrayIn)
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.show()
        
if __name__ == '__main__':
    dash = Dashboard()
    tk.mainloop()