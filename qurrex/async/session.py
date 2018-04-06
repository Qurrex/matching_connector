import asyncio
from .protocol import TcpProtocol, UdpProtocol
from qurrex.log import *
from qurrex.tools import *
from qurrex.messages import *


class QurrexSession(TcpProtocol):

    def __init__(self, ip, port):
        TcpProtocol.__init__(self, ip, port)
        self.sequence_out = 1

    async def connect(self):
        await self.connection_made()

    async def message_writer(self, msg):
        frame = Frame()
        frame.msgId = msg._msgid
        frame.msgSize = msg.get_size()
        frame.msgSeq = self.sequence_out
        data = frame.pack() + msg.pack()
        logger.debug('Message writer\n%s' % ByteToHex(data))
        await self.data_writer(data)
        self.sequence_out += 1

    def message_received(self, frame, data):
        logger.debug(ByteToHex(data))
        try:
            if frame.msgId == RejectReport._msgid:
                self.onRejectReport(data)
            elif frame.msgId == NewOrderReport._msgid:
                self.onNewOrderReport(data)
            elif frame.msgId == CancelReport._msgid:
                self.onCancelReport(data)
            elif frame.msgId == MassCancelReport._msgid:
                self.onMassCancelReport(data)
            elif frame.msgId == ExecutionReport._msgid:
                self.onExecutionReport(data)
            else:
                logger.error("Unknown msgId %s" % frame.msgId)
        except Exception as e:
            logger.error(e)

    def onRejectReport(self, data):
        reject = RejectReport(data)
        logger.error(reject)

    def onNewOrderReport(self, data):
        return data

    def onCancelReport(self, data):
        return data

    def onMassCancelReport(self, data):
        return data

    def onExecutionReport(self, data):
        return data


class QurrexBestPrices(UdpProtocol):

    def __init__(self, address):
        UdpProtocol.__init__(self, address)

        self.last_sequence = 0
        self.best_prices = {}

    def message_received(self, frame, data):
        logger.debug(ByteToHex(data))
        try:
            if frame.msgId == BestPrice._msgid:
                self.onBestPrice(data)
            else:
                logger.error("Unknown msgId %s" % frame.msgId)
        except Exception as e:
            logger.error(e)

    def onBestPrice(self, data):
        bp = BestPrice(data)
        logger.debug(bp)
        if bp.bid_valid == 1 and bp.ask_valid == 1:
            self.best_prices[bp.instrument] = bp
