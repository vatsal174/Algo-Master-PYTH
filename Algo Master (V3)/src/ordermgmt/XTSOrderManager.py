# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:56:00 2022

@author: Vatsal Vasani
"""

import logging

from ordermgmt.BaseOrderManager import BaseOrderManager
from ordermgmt.Order import Order

from models.ProductType import ProductType
from models.OrderType import OrderType
from models.Direction import Direction
from models.OrderStatus import OrderStatus

from utils.Utils import Utils

class XTSOrderManager(BaseOrderManager):
  def __init__(self):
    super().__init__("XTS")

  def placeOrder(self, orderInputParams):
    logging.info('%s: Going to place order with params %s', self.broker, orderInputParams)
    XTS = self.brokerHandle
    try:
      orderId = XTS.place_order(
        variety=XTS.VARIETY_REGULAR,
        exchange=XTS.EXCHANGE_NFO if orderInputParams.isFnO == True else XTS.EXCHANGE_NSE,
        tradingsymbol=orderInputParams.tradingSymbol,
        transaction_type=self.convertToBrokerDirection(orderInputParams.direction),
        quantity=orderInputParams.qty,
        price=orderInputParams.price,
        trigger_price=orderInputParams.triggerPrice,
        product=self.convertToBrokerProductType(orderInputParams.productType),
        order_type=self.convertToBrokerOrderType(orderInputParams.orderType))

      logging.info('%s: Order placed successfully, orderId = %s', self.broker, orderId)
      order = Order(orderInputParams)
      order.orderId = orderId
      order.orderPlaceTimestamp = Utils.getEpoch()
      order.lastOrderUpdateTimestamp = Utils.getEpoch()
      return order
    except Exception as e:
      logging.info('%s Order placement failed: %s', self.broker, str(e))
      raise Exception(str(e))

  def modifyOrder(self, order, orderModifyParams):
    logging.info('%s: Going to modify order with params %s', self.broker, orderModifyParams)
    XTS = self.brokerHandle
    try:
      orderId = XTS.modify_order(
        variety=XTS.VARIETY_REGULAR,
        order_id=order.orderId,
        quantity=orderModifyParams.newQty if orderModifyParams.newQty > 0 else None,
        price=orderModifyParams.newPrice if orderModifyParams.newPrice > 0 else None,
        trigger_price=orderModifyParams.newTriggerPrice if orderModifyParams.newTriggerPrice > 0 else None,
        order_type=orderModifyParams.newOrderType if orderModifyParams.newOrderType != None else None)

      logging.info('%s Order modified successfully for orderId = %s', self.broker, orderId)
      order.lastOrderUpdateTimestamp = Utils.getEpoch()
      return order
    except Exception as e:
      logging.info('%s Order modify failed: %s', self.broker, str(e))
      raise Exception(str(e))

  def modifyOrderToMarket(self, order):
    logging.info('%s: Going to modify order with params %s', self.broker)
    XTS = self.brokerHandle
    try:
      orderId = XTS.modify_order(
        variety=XTS.VARIETY_REGULAR,
        order_id=order.orderId,
        order_type=XTS.ORDER_TYPE_MARKET)

      logging.info('%s Order modified successfully to MARKET for orderId = %s', self.broker, orderId)
      order.lastOrderUpdateTimestamp = Utils.getEpoch()
      return order
    except Exception as e:
      logging.info('%s Order modify to market failed: %s', self.broker, str(e))
      raise Exception(str(e))

  def cancelOrder(self, order):
    logging.info('%s Going to cancel order %s', self.broker, order.orderId)
    XTS = self.brokerHandle
    try:
      orderId = XTS.cancel_order(
        variety=XTS.VARIETY_REGULAR,
        order_id=order.orderId)

      logging.info('%s Order cancelled successfully, orderId = %s', self.broker, orderId)
      order.lastOrderUpdateTimestamp = Utils.getEpoch()
      return order
    except Exception as e:
      logging.info('%s Order cancel failed: %s', self.broker, str(e))
      raise Exception(str(e))

  def fetchAndUpdateAllOrderDetails(self, orders):
    logging.info('%s Going to fetch order book', self.broker)
    XTS = self.brokerHandle
    orderBook = None
    try:
      orderBook = XTS.orders()
    except Exception as e:
      logging.error('%s Failed to fetch order book', self.broker)
      return

    logging.info('%s Order book length = %d', self.broker, len(orderBook))
    numOrdersUpdated = 0
    for bOrder in orderBook:
      foundOrder = None
      for order in orders:
        if order.orderId == bOrder['order_id']:
          foundOrder = order
          break
      
      if foundOrder != None:
        logging.info('Found order for orderId %s', foundOrder.orderId)
        foundOrder.qty = bOrder['quantity']
        foundOrder.filledQty = bOrder['filled_quantity']
        foundOrder.pendingQty = bOrder['pending_quantity']
        foundOrder.orderStatus = bOrder['status']
        if foundOrder.orderStatus == OrderStatus.CANCELLED and foundOrder.filledQty > 0:
          # Consider this case as completed in our system as we cancel the order with pending qty when strategy stop timestamp reaches
          foundOrder.orderStatus = OrderStatus.COMPLETED
        foundOrder.price = bOrder['price']
        foundOrder.triggerPrice = bOrder['trigger_price']
        foundOrder.averagePrice = bOrder['average_price']
        logging.info('%s Updated order %s', self.broker, foundOrder)
        numOrdersUpdated += 1

    logging.info('%s: %d orders updated with broker order details', self.broker, numOrdersUpdated)

  def convertToBrokerProductType(self, productType):
    XTS = self.brokerHandle
    if productType == ProductType.MIS:
      return XTS.PRODUCT_MIS
    elif productType == ProductType.NRML:
      return XTS.PRODUCT_NRML
    elif productType == ProductType.CNC:
      return XTS.PRODUCT_CNC
    return None 

  def convertToBrokerOrderType(self, orderType):
    XTS = self.brokerHandle
    if orderType == OrderType.LIMIT:
      return XTS.ORDER_TYPE_LIMIT
    elif orderType == OrderType.MARKET:
      return XTS.ORDER_TYPE_MARKET
    elif orderType == OrderType.SL_MARKET:
      return XTS.ORDER_TYPE_SLM
    elif orderType == OrderType.SL_LIMIT:
      return XTS.ORDER_TYPE_SL
    return None

  def convertToBrokerDirection(self, direction):
    XTS = self.brokerHandle
    if direction == Direction.LONG:
      return XTS.TRANSACTION_TYPE_BUY
    elif direction == Direction.SHORT:
      return XTS.TRANSACTION_TYPE_SELL
    return None

