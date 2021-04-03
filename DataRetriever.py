import tushare as ts
import json


class DataRetriever:
    def __init__(self, token, code, start, end, file_name):
        ts.set_token(token=token)
        self.api = ts.pro_api()
        self.code = code
        self.start = start
        self.end = end
        self.file_name = file_name

    def retrieve_data(self):
        data = self.api.daily(ts_code=self.code, start_date=self.start, end_date=self.end)
        return data

    def create_json_file(self):
        json_str = self.retrieve_data().to_json(orient='index', force_ascii=False)
        with open(self.file_name, 'w') as json_file:
            json_file.write(json_str)
