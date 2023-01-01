# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:25:59 2022

@author: Vatsal Vasani
"""

import logging

from config.Config import getBrokerAppConfig
from models.BrokerAppDetails import BrokerAppDetails
from loginmgmt.XTSlogin import XTSlogin
class Controller:
  brokerLogin = None # static variable
  brokerName = None # static variable

  def handleBrokerLogin(args):
    brokerAppConfig = getBrokerAppConfig()

    brokerAppDetails = BrokerAppDetails(brokerAppConfig['broker'])
    brokerAppDetails.setClientID(brokerAppConfig['clientID'])
    brokerAppDetails.setAppKey(brokerAppConfig['appKey'])
    brokerAppDetails.setAppSecret(brokerAppConfig['appSecret'])

    logging.info('handleBrokerLogin appKey %s', brokerAppDetails.appKey)
    Controller.brokerName = brokerAppDetails.broker
    if Controller.brokerName == 'XTS':
      Controller.brokerLogin = XTSlogin(brokerAppDetails)
    # Other brokers - not implemented
    #elif Controller.brokerName == 'fyers':
      #Controller.brokerLogin = FyersLogin(brokerAppDetails)

    redirectUrl = Controller.brokerLogin.login(args)
    return redirectUrl

  def getBrokerLogin():
    return Controller.brokerLogin

  def getBrokerName():
    return Controller.brokerName

