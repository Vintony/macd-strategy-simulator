import os
import json
import xlwings as xw
import matplotlib.pyplot as plt


class Trader:
    def __init__(self, data_name, money, stock_name):
        self.list_dailyData = []
        self.money = money
        self.start = money
        self.hold = float()
        self.stock_name = stock_name
        self.trade_records = []

        if os.path.exists(data_name):
            with open(data_name, 'r') as json_file:
                list_data = [i for i in json.load(json_file).values()]
                list_data.reverse()
                for i in list_data:
                    data = DailyData(i)
                    self.list_dailyData.append(data)
        else:
            print("There is no " + data_name + " !")

    def trade(self):
        self.init_start_data()
        self.cal_rest_data()
        for today in self.list_dailyData[3:len(self.list_dailyData) - 2]:
            yesterday = self.list_dailyData[self.list_dailyData.index(today) - 1]
            tomorrow = self.list_dailyData[self.list_dailyData.index(today) + 1]
            today.ratio = self.money / self.start if self.money != 0 else \
                self.hold * today.close / self.start
            if today.signal != yesterday.signal:
                # 买入
                if today.signal == 1:
                    if self.money != 0:
                        self.trade_records.append([tomorrow.date, '买入', tomorrow.open,
                                                   self.money * 0.998 / tomorrow.open, self.money * 0.002])
                        self.hold += self.money * 0.998 / tomorrow.open
                        self.money = 0
                # 卖出
                else:
                    if self.hold != 0:
                        self.trade_records.append([tomorrow.date, '卖出', tomorrow.open,
                                                   self.hold, self.hold * 0.002 * tomorrow.open])
                        self.money += self.hold * 0.998 * tomorrow.open
                        self.hold = 0

        self.create_trade_record_xlsx()
        self.create_ratio_pic()

        if self.money == 0:
            print('最终持仓市值为' + str(self.hold * self.list_dailyData[len(self.list_dailyData) - 1].close))
        else:
            print('最终持仓市值为' + str(self.money))

    def init_start_data(self):
        self.list_dailyData[0].ema12 = 0
        self.list_dailyData[0].ema26 = 0
        self.list_dailyData[0].dif = 0
        self.list_dailyData[0].dea = 0

        self.list_dailyData[1].ema12 = self.list_dailyData[0].close * 11 / 13 + self.list_dailyData[1].close * 2 / 13
        self.list_dailyData[1].ema26 = self.list_dailyData[0].close * 25 / 27 + self.list_dailyData[1].close * 2 / 27
        self.list_dailyData[1].dif = self.list_dailyData[1].ema12 - self.list_dailyData[1].ema26
        self.list_dailyData[1].dea = self.list_dailyData[1].dif * 2 / 10

    def cal_rest_data(self):
        for today in self.list_dailyData[2:]:
            yesterday = self.list_dailyData[self.list_dailyData.index(today) - 1]
            today.ema12 = yesterday.close * 11 / 13 + today.close * 2 / 13
            today.ema26 = yesterday.close * 25 / 27 + today.close * 2 / 27
            today.dif = today.ema12 - today.ema26
            today.dea = yesterday.dea * 8 / 10 + today.dif * 2 / 10
            # 0指dea高于dif 1指dif高于dea 由0->1则指示dif由下向上突破dea 买入 由1->0则指示dif由上向下突破dea 卖出
            today.signal = 0 if today.dea - today.dif >= 0 else 1

    def create_trade_record_xlsx(self):
        app = xw.App(visible=True, add_book=False)
        wb = app.books.add()
        sht = wb.sheets('Sheet1')
        sht.range('a1').value = ['交易日期', '交易类型', '交易价格', '交易量', '手续费']
        sht.range('a2').expand('table').value = self.trade_records
        wb.save(self.stock_name + '.xlsx')
        wb.close()
        app.quit()

    def create_ratio_pic(self):
        dates = []
        ratios = []
        for i in self.list_dailyData[3:len(self.list_dailyData) - 2]:
            dates.append(i.date)
            ratios.append(i.ratio)
        plt.plot(dates, ratios)
        plt.savefig(self.stock_name + "-每日净值曲线.png")
        plt.show()


class DailyData:
    def __init__(self, dict_data):
        self.date = dict_data['trade_date']
        self.ema12 = None
        self.ema26 = None
        self.dif = None
        self.dea = None
        self.signal = None
        self.ratio = None
        self.data = dict_data['trade_date']
        self.open = dict_data['open']
        self.close = dict_data['close']
        self.high = dict_data['high']
        self.low = dict_data['low']
