import DataRetriever as dr
import Trader as tr

if __name__ == '__main__':
    # api token 股票代码 起始日期 结束日期 数据存储名
    data_retriever = dr.DataRetriever(token='efb2687234ab87799580e022f544e5f28da8c17be5152b8c6819784a',
                                      code='600519.SH',
                                      start='20180101', end='20210403',
                                      file_name='MaoTai.json')
    data_retriever.create_json_file()

    # 读取json文件名 初始资本 股票名称
    trader = tr.Trader('MaoTai.json', 10000000.0, '贵州茅台')
    trader.trade()
