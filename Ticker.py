from tkinter import *
from pandas.core.frame import DataFrame
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

tickerArray = ['MSFT','DIS','GOOG','GME','AMC','BB','CLF']
tk = Tk()
tk.configure(bg="#1B1B1B")
tk.title("Stock Tickers for APES")
tk.attributes('-fullscreen', False)
frame = Frame(tk)
frame.pack

class Dashboard:
    def __init__(self):
        self.state = False
        tk.bind("<Escape>", self.toggle_fullscreen)
        self.enumerate_ticker(tickerArray)
        self.update_ticker_by_row()


    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        tk.attributes("-fullscreen", self.state)
    
    def add_ticker(self,index,ticker):   
        stock = yf.Ticker(ticker)
        priceArray = stock.history(period='1d',interval='2m')['Close']
        openPrice = stock.history(period='2d', interval='1d')['Close'][0]
        currPrice = stock.history(period='1d')['Close'][0]
        difference = currPrice - openPrice
        currPriceStr = "${:,.2f}".format(currPrice)
        differenceStr = "${:,.2f}".format(difference)
        tickerColor = self.get_ticker_color(difference)
        tickerName = Label(tk, text = ticker, bg="#1B1B1B", fg = "white", font=("Helvetica", 30, "bold"))
        tickerPrice = Label(tk, text = currPriceStr, bg="#1B1B1B", fg = tickerColor, font = ("Helvetica", 24, "bold"))
        tickerDiff = Label(tk, text = differenceStr, bg="#1B1B1B", fg = tickerColor, font = ("Helvetica", 20, "bold italic"))
        self.createGraph(priceArray,openPrice,index,tickerColor)

        tickerName.grid(row = index*2, column = 0, pady = 8, sticky=NW)
        tickerPrice.grid(row = index*2, column = 1, pady = 8, padx = 164, sticky=E)
        tickerDiff.grid(row = index*2+1, column = 1, padx = 188, pady=8, sticky=E)

    def get_ticker_color(self,difference):
        if float(difference) < 0:
            return "coral"
        else:
            return "cyan"
    
    def enumerate_ticker(self,tickerIn):
        for index,ticker in enumerate(tickerIn):
            self.add_ticker(index,ticker)

    def update_ticker_by_row(self):
        for index,ticker in enumerate(tickerArray):
            tickerName = tk.grid_slaves(row=index*2,column=0)[0]
            tickerPrice = tk.grid_slaves(row=index*2,column=1)[0]
            tickerDiff = tk.grid_slaves(row=index*2+1,column=1)[0]
            tk.grid_slaves(row=index*2,column=2)[0].destroy()
            self.update_ticker_item(tickerName,tickerPrice,tickerDiff,index)
        tk.after(10000,self.update_ticker_by_row)
    
    def update_ticker_item(self,name,priceLabel,diffLabel,indexIn):
        stock = yf.Ticker(name["text"])
        priceArray = stock.history(period='1d',interval='2m')['Close']
        openPrice = stock.history(period='2d',interval='1d')['Close'][0]
        currPrice = stock.history(period='1d')['Close'][0]
        difference = currPrice - openPrice
        percentChange = difference / openPrice * 100
        currPriceStr = "${:,.2f}".format(currPrice)
        differenceStr = "${:,.2f}".format(difference) + " (%{:,.2f})".format(percentChange)
        priceLabel['text']=currPriceStr
        diffLabel['text']=differenceStr
        
        tickerColor = self.get_ticker_color(difference)
        priceLabel['fg']=tickerColor
        diffLabel['fg']=tickerColor

        
        self.createGraph(priceArray,openPrice,indexIn,tickerColor)

    def createGraph(self,priceArrayIn,open,indexIn,tickerColor):
        plt.axis('off')
        figure = plt.Figure(figsize=(2,1))
        ax=figure.add_subplot(111)
        ax.axis("off")
        figure.set(facecolor = "#1B1B1B")
        ax.patch.set_alpha(0)
        canvas = FigureCanvasTkAgg(figure, tk)
        canvas.get_tk_widget().grid(row = indexIn*2, column = 2, rowspan = 2, pady = 8, sticky=W)
        df = DataFrame(priceArrayIn)
        df.plot(kind='line',ax=ax,color=tickerColor,legend=None)
        df2 = DataFrame(priceArrayIn)
        df2['Close']=open
        df2.plot(kind='line',ax=ax,linestyle='dotted',color='grey',legend=None)
        
if __name__ == '__main__':
    dash = Dashboard()
    tk.mainloop()