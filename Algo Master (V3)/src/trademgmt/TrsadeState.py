# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 10:01:15 2023

@author: Vatsal Vasani
"""


class TradeState:
  CREATED = 'created' # Trade created but not yet order placed, might have not triggered
  ACTIVE = 'active' # order placed and trade is active
  COMPLETED = 'completed' # completed when exits due to SL/Target/SquareOff
  CANCELLED = 'cancelled' # cancelled/rejected comes under this state only
  DISABLED = 'disabled' # disable trade if not triggered within the time limits or for any other reason