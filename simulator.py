import tushare as ts
import DataRetriever as dr

if __name__ == '__main__':
    data_retriever = dr.DataRetriever(token='efb2687234ab87799580e022f544e5f28da8c17be5152b8c6819784a',
                                      code='600519.SH',
                                      start='20180101', end='20210403',
                                      file_name='MaoTai.json')
    data_retriever.create_json_file()


