# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 20:07:58 2022

@author: Vatsal Vasani
"""

from flask.views import MethodView
from flask import render_template, request

class HomeAPI(MethodView):
  def get(self):
    if 'loggedIn' in request.args and request.args['loggedIn'] == 'true':
      return render_template('index_loggedin.html')
    elif 'algoStarted' in request.args and request.args['algoStarted'] == 'true':
      return render_template('index_algostarted.html')
    else:
      return render_template('index.html')
  