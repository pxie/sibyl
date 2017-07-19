# coding=utf-8

import os
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt

from logger import log
from data_generator import rand
import json


class LinearPredict:

    def __init__(self):
        log.debug("init LinearPredict class")

    def linear_regression(self, data):
        df = pd.DataFrame(self.format2dataframe(data))
        log.debug("dataframe: %s", df)

        # 建立线性回归模型
        regr = linear_model.LinearRegression()

        # 拟合
        # 注意此处.reshape(-1, 1)，因为X是一维的！
        regr.fit(df["ts"].values.reshape(-1, 1), df['meas'])

        # 不难得到直线的斜率、截距
        a, b = regr.coef_, regr.intercept_

        return df, regr

    def do_predict(self, tslist, regr):
        result = {"ts": [], "meas": [], "qy": []}
        for ts in tslist:
            result["ts"].append(ts)
            result["meas"].append(float(regr.predict(ts)[0]))
            result["qy"].append(3)

        log.debug("do_predict, result: %s", result)

        return pd.DataFrame(result)

    def predict(self, json_data):
        log.debug("json data: %s", json_data)
        data = json.loads(json_data)

        # calcuate formula
        df, regr = self.linear_regression(data["values"])
        print(df)
        log.debug("df: \n%s", df)

        # predict next 25% data points
        step = df["ts"][1] - df["ts"][0]
        log.debug("step: %s", step)
        total = int(round(len(df["ts"]) / 4))
        tslist = []
        for i in range(total):
            print(df.tail(1))
            log.debug("int(df.iloc[-1]['ts']): %s", int(df.iloc[-1]["ts"]))
            tslist.append(int(df.iloc[-1]["ts"]) + step * (i + 1))
        log.debug("tslist: %s", tslist)

        predict_df = self.do_predict(tslist, regr)
        print(predict_df)

        return json.dumps({"values": self.format2ts(predict_df)})

    def format2dataframe(self, tslist):
        # format data from,
        #    [
        #       [1435556274138, 0.264158713731815, 0],
        #       [1435557118934, 0.4872329925809995, 3]
        #   ]
        # to
        #   {
        #       "ts": [1435556274138, 1435557118934],
        #       "meas": [0.264158713731815, 0.4872329925809995],
        #       "qy": [0, 3]
        #   }
        log.debug("before format, tslist: %s", tslist)
        result = {"ts": [], "meas": [], "qy": []}
        if not (type(tslist) is list):
            return result

        for item in tslist:
            log.debug("item: %s", item)
            result["ts"].append(item[0])
            result["meas"].append(item[1])
            result["qy"].append(item[2] if len(item) == 3 else 3)

        log.info("after format, dataframe: %s", result)
        return result

    def format2ts(self, dataframe):
        # format data from,
        #   {
        #       "ts": [1435556274138, 1435557118934],
        #       "meas": [0.264158713731815, 0.4872329925809995],
        #       "qy": [0, 3]
        #   }
        # to
        #    [
        #       [1435556274138, 0.264158713731815, 0],
        #       [1435557118934, 0.4872329925809995, 3]
        #   ]
        log.debug("before df2ts format, dataframe: \n%s", dataframe)
        tslist = []
        for index, item in dataframe.iterrows():
            log.debug("item in dataframe, type(item): %s, item: \n%s",
                      type(item), item)
            tslist.append([int(item["ts"]), float(
                item["meas"]), int(item["qy"])])

        log.debug("after df2ts format, tslist: %s", tslist)

        return tslist

    def draw(self, dataframe, predict_df, regr):
        # 画图
        # 1.真实的点
        plt.scatter(dataframe['ts'], dataframe['meas'], color='blue')

        # 未来的点
        plt.scatter(predict_df['ts'], predict_df['meas'], color='green')

        # 2.拟合的直线
        all_data = pd.concat([dataframe, predict_df])
        plt.plot(all_data['ts'].values.reshape(-1, 1),
                 regr.predict(all_data['ts'].values.reshape(-1, 1)), color='red', linewidth=1)
        plt.show()
