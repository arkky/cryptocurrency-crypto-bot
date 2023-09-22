from enum import Enum

import pandas as pd
import plotly.graph_objects as go


class intervalEnum(Enum):
    """Need to choose one of them"""
    min_1 = "1min"
    min_5 = "5min"
    min_15 = "15min"
    min_30 = "30min"
    hour_1 = "1h"
    hour_4 = "4h"
    hour_12 = "12h"
    day_1 = "1d"


class FinanceChart:
    """This class has an interface for constructing candles in the OHLC format 
    and with the addition of an EMA indicator"""
    def __init__(self, path: str = "prices.csv", candle_interval: str = "1h", length: int = 14):
        self.path = path
        self.candle_interval = candle_interval
        self.length = length
        if length < 1:
            raise Exception("Length can not be less than 1")
        
        self.df = self.load_data()
        self.df_ohlc = self.aggregate_candles()
        self.calc_ema()

    def load_data(self) -> pd.DataFrame:
        """Load csv file by path and return pandas.DataFrame."""
        return pd.read_csv(self.path)

    def aggregate_candles(self) -> pd.DataFrame:
        """Transform and aggregate pandas.DataFrame by candle_interval to OHLC format
        then return new pandas.DataFrame."""
        self.df.index = pd.to_datetime(self.df.TS, format="%Y-%m-%d %H:%M:%S.%f")
        self.df.drop(["TS"], axis=1, inplace=True)
        
        interval = intervalEnum(self.candle_interval).value
        df_ohlc = self.df.PRICE.resample(interval).ohlc()
        df_ohlc.fillna(method="ffill", inplace=True)
        return df_ohlc

    def calc_ema(self):
        """Calculate EMA (Exponential Moving Average) by length/period on pandas.DataFrame.
        Update pandas.DataFrame inplace."""
        if len(self.df_ohlc) < self.length:
            raise Exception(f"Length {self.length} can not be more than length of self.df_ohlc {len(self.df_ohlc)}")

        multiplicator = round(2 / (self.length + 1), 6)
        emas = [None] * (self.length - 1)
        init_ema = round(self.df_ohlc.iloc[:self.length].close.sum() / self.length, 6)
        emas.append(init_ema)
        
        for i in range(self.length, len(self.df_ohlc)):
            cur_price = self.df_ohlc.iloc[i].close
            prev_ema = emas[-1]
            cur_ema = round((cur_price * multiplicator) + (prev_ema * (1 - multiplicator)), 6)
            emas.append(cur_ema)
        
        self.df_ohlc["ema"] = emas

    def plot(self):
        """Plot figure on df and with length of EMA"""
        chart = go.Candlestick(
            x=self.df_ohlc.index,
            open=self.df_ohlc['open'],
            high=self.df_ohlc['high'],
            low=self.df_ohlc['low'],
            close=self.df_ohlc['close'],
            name="1 hour candles")
        ema_trace = go.Scatter(x=self.df_ohlc.index, y=self.df_ohlc['ema'], mode='lines', name=f'EMA({self.length})', marker={"color": "black"})
        fig = go.Figure(data=[chart])
        fig.add_trace(ema_trace)
        fig.show()


if __name__ == "__main__":
    fin_chart = FinanceChart()
    fin_chart.plot()
