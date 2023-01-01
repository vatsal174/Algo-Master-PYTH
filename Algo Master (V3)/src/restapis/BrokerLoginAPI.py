# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 20:05:33 2022

@author: Vatsal Vasani
"""


import logging
from flask.views import MethodView
from flask import request, redirect

from core.Controller import Controller 

class BrokerLoginAPI(MethodView):
  def get(self):
    redirectUrl = Controller.handleBrokerLogin(request.args)
    return redirect(redirectUrl, code=302)