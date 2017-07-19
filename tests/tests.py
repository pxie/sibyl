# coding=utf-8

import os
import json
import sys
sys.path.append(os.getcwd())

import unittest
import sibyl.data_generator as dg
import sibyl.analytic as ax
from sibyl.logger import log
import pandas as pd
import matplotlib.pyplot as plt


class TestDataGenerator(unittest.TestCase):

    def test_rand(self):
        count = 100
        data = dg.rand(count)
        self.assertEqual(len(data["values"]), count)
        for item in data["values"]:
            self.assertFalse(self.__greater(item[1], 0.05 * item[0] + 1))

    def __greater(self, num1, num2):
        return True if num1 > num2 else False


class TestAnalytic(unittest.TestCase):

    def test_predict(self):
        count = 100
        data = dg.rand(count)
        linear_predict = ax.LinearPredict()
        predict_json = linear_predict.predict(json.dumps(data))
        log.debug("predict_json: %s", predict_json)

    def test_predict_with_data(self):
        data = {"values": [
            [1435556274138, 0.264158713731815, 0],
            [1435557118934, 0.4872329925809995, 3],
            [1435567118934, 0.7872329925809995, 3],
            [1435577118934, 0.2872329925809995, 3]]
        }
        linear_predict = ax.LinearPredict()
        predict_json = linear_predict.predict(json.dumps(data))
        log.debug("predict_json: %s", predict_json)

    def test_draw(self):
        count = 100
        data = dg.rand(count)

        # calcuate formula
        linear_predict = ax.LinearPredict()
        df, regr = linear_predict.linear_regression(data["values"])
        print(df)

        # predict next 25% data points
        step = df["ts"][1] - df["ts"][0]
        total = int(round(len(df["ts"]) / 4))
        tslist = []
        for i in range(total):
            log.debug("df.tail(1)['ts']: %s", df.tail(1)["ts"])
            tslist.append(df.tail(1)["ts"] + step * (i + 1))

        predic_df = linear_predict.do_predict(tslist, regr)

        draw(df, predic_df, regr)


def draw(dataframe, predict_df, regr):
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

if __name__ == "__main__":
    unittest.main()
