from tkinter import *
import yfinance as yf
import sched, time

tickerArray = ['MSFT','DIS','GOOG','GME','AMC','BB','CLF']
tk = Tk()
tk.title("Stock Tickers for APES")
tk.attributes('-zoomed', True)
frame = Frame(tk)
frame.pack

class Dashboard:
    def __init__(self):
        self.state = False
        tk.bind("<Escape>", self.toggle_fullscreen)
        self.enumerate_ticker(tickerArray)
        self.update_every_minute(tickerArray)


    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        tk.attributes("-fullscreen", self.state)
    
    def add_ticker(self,index,ticker):   
        stock = yf.Ticker(ticker)

        openPrice = stock.history(period='1d')['Open'][0]
        currPrice = stock.history(period='1d')['Close'][0]
        difference = currPrice - openPrice

        tickerName = Label(tk, text = ticker)
        tickerPrice = Label(tk, text = currPrice)
        tickerDiff = Label(tk, text = difference)

        self.set_label_color(tickerPrice,tickerDiff)

        tickerName.grid(row = index*2, column = 0, columnspan = 2, pady = 2, sticky=NW)
        tickerPrice.grid(row = index*2, column = 1, pady = 2, ipadx = 8, sticky=E)
        tickerDiff.grid(row = index*2+1, column = 0, sticky=E)

    def set_label_color(self,labelPrice,labelDiff):
        if int(labelDiff["text"]) < 0:
            labelPrice.config(fg="red")
            labelDiff.config(fg="red")
        else:
            labelPrice.config(fg="green")
            labelDiff.config(fg="green")

    def update_every_minute(self,tickerIn):
        self.update_ticker_by_row(tickerIn)
    
    def enumerate_ticker(self,tickerIn):
        for index,ticker in enumerate(tickerIn):
            self.add_ticker(index,ticker)

    def update_ticker_by_row(self,tickerIn):
        for index,ticker in enumerate(tickerIn):
            tickerName = tk.grid_slaves(row=index*2,column=0)[0]
            tickerPrice = tk.grid_slaves(row=index*2,column=1)[0]
            tickerDiff = tk.grid_slaves(row=index*2+1)[0]
            self.update_ticker_item(tickerName,tickerPrice,tickerDiff)
    
    def update_ticker_item(self,name,price,diff):
        stock = yf.Ticker(name)

        openPrice = stock.history(period='1d')['Open'][0]
        currPrice = stock.history(period='1d')['Close'][0]
        difference = currPrice - openPrice
        price.configure(text=currPrice)
        diff.configure(text=difference)

        
if __name__ == '__main__':
    dash = Dashboard()
    tk.mainloop()