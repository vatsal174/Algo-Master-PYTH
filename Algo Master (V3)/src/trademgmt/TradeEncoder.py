# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 20:54:02 2022

@author: Vatsal Vasani
"""


from json import JSONEncoder

class TradeEncoder(JSONEncoder):
  def default(self, o):
    return o.__dict__