# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:37:35 2022

@author: Vatsal Vasani
"""

class BrokerAppDetails:
  def __init__(self, broker):
    self.broker = broker
    self.appKey = None
    self.appSecret = None

  def setClientID(self, clientID):
    self.clientID = clientID

  def setAppKey(self, appKey):
    self.appKey = appKey

  def setAppSecret(self, appSecret):
    self.appSecret = appSecret

