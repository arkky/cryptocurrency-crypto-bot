import main

if __name__ == "__main__":
    length = 1
    fin_chart = main.FinanceChart(length=length)
    assert fin_chart.df_ohlc.iloc[length].ema == 1875.917881

    length = 2
    fin_chart = main.FinanceChart(length=length)
    assert fin_chart.df_ohlc.iloc[length].ema == 1876.22272

    length = 14
    fin_chart = main.FinanceChart(length=length)
    assert fin_chart.df_ohlc.iloc[length].ema == 1888.200058

    length = 20
    fin_chart = main.FinanceChart(length=length)
    assert fin_chart.df_ohlc.iloc[length].ema == 1898.395231
    print("All tests passed!")
