# macd-strategy-simulator

---
## 安装使用方式

clone本仓库

```
    pip3 install -r requirements.txt
    python simulator.py
```
---

## 实现功能

Python实现以下简单算法：请获取贵州茅台近三年的日K线，根据日K线计算MACD，
当MACD金叉时，次日以开盘价全仓买入贵州茅台，当MACD死叉时次日以开盘价全仓卖出。
手续费为双边千分之二。初始资金为1000万元。请计算从3年前到现在，按上述MACD策略交易，
最近一个交易日收盘后持仓市值是多少？请生成相应的交易记录，以excel表格的形式记录下来，
交易记录中的每笔交易包括交易日期、成交价、成交数量、手续费。
请计算该组合的每日净值（组合份额按1000万份计，且保持不变，组合初始净值为1），
并画出组合净值曲线。

---

## 各参数定义

12日EMA的算式为
EMA（12）=前一日EMA（12）×11/13+今日收盘价×2/13

26日EMA的算式为
EMA（26）=前一日EMA（26）×25/27+今日收盘价×2/27

DIF=今日EMA（12）－今日EMA（26）

今日DEA（MACD）=前一日DEA×8/10+今日DIF×2/10

MACD金叉：DIF 由下向上突破 DEA，为买入信号

MACD死叉：DIF 由上向下突破 DEA，为卖出信号

---

## 初始各参数计算方式

第一天：

DIF=0, DEA=0, MACD=0

第二天：

EMA（12）= 前一日收盘价（12）×11/13＋今日收盘价×2/13

EMA（26）= 前一日收盘价（26）×25/27＋今日收盘价×2/27

DIF=今日EMA（12）- 今日EMA（26）

DEA（MACD）= 前一日0×8/10＋今日DIF×2/10

第三天：
正常计算