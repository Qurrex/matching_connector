import asyncio
import time
import uvloop
import logging
import ctypes
import random
from qurrex.tools import *
from qurrex.messages import *
from qurrex.async.session import *


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
logging.basicConfig(
    format='%(asctime)-22s %(levelname)-5s  %(name)s.%(funcName)s: %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class ClassicClient(QurrexSession):

    def __init__(self, ip, port):
        QurrexSession.__init__(self, ip, port)
        self.clorder = 0
        self._buff = 64000

    def onRejectReport(self, data):
        report = RejectReport(data)
        logger.error(report)

    def onNewOrderReport(self, data):
        report = NewOrderReport(data)
        logger.debug('\n%s' % report)

    def onCancelReport(self, data):
        report = CancelReport(data)
        logger.debug('\n%s' % report)

    def onMassCancelReport(self, data):
        report = MassCancelReport(data)
        logger.debug('\n%s' % report)

    def onExecutionReport(self, data):
        report = ExecutionReport(data)
        main = report.get_size()
        entry = ctypes.sizeof(DealBody())
        deals = []
        for x in range(report.deals_num):
            deal = DealBody(data[main:main+entry])
            deals.append(deal)
            main += entry
        report.deals = deals
        logger.debug('\n%s' % report)

    async def feed(self):
        while True:
            self.clorder += 1
            new = NewOrderRequest()
            new.order.client_req_id = str(self.clorder).encode()
            new.order.clearing_acc_id = "CLEARING".encode()
            new.order.trader_acc_id = "Client01".encode()
            new.order.instrument_id = 6
            new.order.type = random.randint(1,2)
            new.order.time_in_force = random.randint(1,3)
            new.order.side = random.randint(1,2)
            new.order.auto_cancel = 1
            new.order.qty = 100000000
            new.order.price = 100000000
            new.order.flags = 0
            new.order.comment = "testing".encode()
            await self.message_writer(new)
            await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tcp_session = ClassicClient('193.70.35.177', 7777)
    loop.run_until_complete(tcp_session.connect())
    loop.run_until_complete(tcp_session.feed())
    loop.run_forever()
