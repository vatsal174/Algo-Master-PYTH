# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 12:05:10 2022

@author: vatsal
"""
import logging
#from kiteconnect import KiteConnect

from config.Config import getSystemConfig
from loginmgmt.BaseLogin import BaseLogin

class XTSlogin(BaseLogin):
  def __init__(self, brokerAppDetails):
    BaseLogin.__init__(self, brokerAppDetails)

  def login(self, args):
    logging.info('==> XTSLogin .args => %s', args);
    systemConfig = getSystemConfig()
    brokerHandle = XTSConnect(api_key=self.brokerAppDetails.appKey)
    redirectUrl = None
    if 'request_token' in args:
      requestToken = args['request_token']
      logging.info('XTS requestToken = %s', requestToken)
      session = brokerHandle.generate_session(requestToken, api_secret=self.brokerAppDetails.appSecret)
      
      accessToken = session['access_token']
      accessToken = accessToken
      logging.info('XTS accessToken = %s', accessToken)
      brokerHandle.set_access_token(accessToken)
      
      logging.info('XTS Login successful. accessToken = %s', accessToken)

      # set broker handle and access token to the instance
      self.setBrokerHandle(brokerHandle)
      self.setAccessToken(accessToken)

      # redirect to home page with query param loggedIn=true
      homeUrl = systemConfig['homeUrl'] + '?loggedIn=true'
      logging.info('XTS Redirecting to home page %s', homeUrl)
      redirectUrl = homeUrl
    else:
      loginUrl = brokerHandle.login_url()
      logging.info('Redirecting to XTS login url = %s', loginUrl)
      redirectUrl = loginUrl

    return redirectUrl


