# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:46:24 2022

@author: Vatsal Vasani
"""


class TickData:
  def __init__(self, tradingSymbol):
    self.tradingSymbol = tradingSymbol
    self.lastTradedPrice = 0
    self.lastTradedQuantity = 0
    self.avgTradedPrice = 0
    self.volume = 0
    self.totalBuyQuantity = 0
    self.totalSellQuantity = 0
    self.open = 0
    self.high = 0
    self.low = 0
    self.close = 0
    self.change = 0