from ctypes import *
from enum import Enum


class BinaryStructure(Structure):
    _pack_ = 1

    def __str__(self):
        rows = []
        for field in self._fields_:
            value = getattr(self, field[0])
            if isinstance(value, bytes):
                value = value.decode()
            rows.append("{0}: {1}\n".format(field[0], value))
        if hasattr(self, 'deals'):
            for item in self.deals:
                rows.append("deal:\n")
                for field in item._fields_:
                    value = getattr(item, field[0])
                    rows.append("  {0}: {1}\n".format(field[0], value))
        return ''.join(rows)

    def __init__(self, data=None):
        if data:
            self.unpack(data)

    def unpack(self, raw):
        fit = sizeof(self)
        memmove(addressof(self), raw[:fit], fit)

    def pack(self):
        return bytearray(self)[:]

    def get_size(self):
        return sizeof(self)


class eOrderSide(Enum):
    BUY = c_char(1)
    SELL = c_char(1)


class eOrderType(Enum):
    LIMIT = c_char(1)
    HIDDEN = c_char(2)


class eTimeInForce(Enum):
    GTK = c_char(1)
    IOC = c_char(2)
    FOK = c_char(3)


class eAutoCancel(Enum):
    ON = c_char(1)


class eMassCancelMode(Enum):
    BY_CONNECT = c_char(1)
    CONNECT_INSTRUMENT = c_char(2)


class DealBody(BinaryStructure):

    _fields_ = [
        ('deal_id', c_ulonglong),
        ('price', c_longlong),
        ('amount', c_ulonglong)
    ]


class BestLevel(BinaryStructure):
    _fields_ = [
        ('type', c_byte),
        ('price', c_longlong),
        ('qty', c_int)
    ]


class OrderBody(BinaryStructure):

    _fields_ = [
        ('client_req_id', c_char * 16),
        ('clearing_acc_id', c_char * 16),
        ('trader_acc_id', c_char * 16),
        ('instrument_id', c_int),
        ('type', c_byte),
        ('time_in_force', c_byte),
        ('side', c_byte),
        ('auto_cancel', c_byte),
        ('qty', c_longlong),
        ('price', c_longlong),
        ('flags', c_ulonglong),
        ('comment', c_char * 16)
    ]


class CancelBody(BinaryStructure):

    _fields_ = [
        ('client_req_id', c_char * 16),
        ('clearing_acc_id', c_char * 16),
        ('trader_acc_id', c_char * 16),
        ('instrument_id', c_int),
        ('exchange_order_id', c_ulonglong),
        ('order_client_req_id', c_char * 16),
        ('side', c_byte)
    ]


class Frame(BinaryStructure):

    _fields_ = [
        ('msgId', c_ushort),
        ('msgSize', c_ushort),
        ('msgSeq', c_ulonglong)
    ]


class NewOrderRequest(BinaryStructure):
    _msgid = 1

    _fields_ = [
        ('order', OrderBody)
    ]


class NewOrderReport(BinaryStructure):
    _msgid = 2

    _fields_ = [
        ('system_time_input', c_ulonglong),
        ('system_time_output', c_ulonglong),
        ('order', OrderBody),
        ('system_time', c_longlong),
        ('exchange_order_id', c_ulonglong),
        ('liquidity_pool_id', c_ushort),
        ('order_routing_rule', c_ushort)
    ]


class CancelRequest(BinaryStructure):
    _msgid = 3

    _fields_ = [
        ('cancel', CancelBody)
    ]


class CancelReport(BinaryStructure):
    _msgid = 4

    _fields_ = [
        ('system_time_input', c_ulonglong),
        ('system_time_output', c_ulonglong),
        ('cancel', CancelBody),
        ('system_time', c_ulonglong),
        ('amount_cancelled', c_longlong),
        ('amount_rest', c_longlong),
        ('cancel_reason', c_int)
    ]


class MassCancelRequest(BinaryStructure):
    _msgid = 12

    _fields_ = [
        ('client_req_id', c_char * 16),
        ('clearing_acc_id', c_char * 16),
        ('trader_acc_id', c_char * 16),
        ('instrument_id', c_int),
        ('cancel_mode', c_byte)
    ]


class MassCancelReport(BinaryStructure):
    _msgid = 14

    _fields_ = [
        ('system_time_input', c_ulonglong),
        ('system_time_output', c_ulonglong),
        ('system_time', c_ulonglong),
        ('client_req_id', c_char * 16),
        ('clearing_acc_id', c_char * 16),
        ('trader_acc_id', c_char * 16),
        ('instrument_id', c_int),
        ('cancel_mode', c_byte),
        ('cancel_status', c_byte),
        ('cancelled_orders', c_int)
    ]


class ExecutionReport(BinaryStructure):
    _msgid = 5

    _fields_ = [
        ('order', OrderBody),
        ('system_time', c_ulonglong),
        ('exchange_order_id', c_ulonglong),
        ('amount_rest', c_longlong),
        ('deals_num', c_byte)
    ]
    deals = []


class RejectReport(BinaryStructure):
    _msgid = 10

    _fields_ = [
        ('system_time_input', c_ulonglong),
        ('system_time_output', c_ulonglong),
        ('system_time', c_ulonglong),
        ('client_req_id', c_char * 16),
        ('error_code', c_ushort)
    ]


class BestPrice(BinaryStructure):
    _msgid = 20

    _fields_ = [
        ('system_time', c_ulonglong),
        ('instrument_id', c_int),
        ('levels_count', c_int)
    ]
    levels = []


class OrderBook(BinaryStructure):
    _msgid = 20

    _fields_ = [
        ('system_time', c_ulonglong),
        ('instrument_id', c_int),
        ('levels_count', c_int)
    ]
    levels = []
