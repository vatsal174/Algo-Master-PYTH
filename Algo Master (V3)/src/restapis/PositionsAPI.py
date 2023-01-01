# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 20:10:53 2022

@author: Vatsal Vasani
"""

from flask.views import MethodView
import json
import logging
from core.Controller import Controller

class PositionsAPI(MethodView):
  def get(self):
    brokerHandle = Controller.getBrokerLogin().getBrokerHandle()
    positions = brokerHandle.positions()
    logging.info('User positions => %s', positions)
    return json.dumps(positions)
  