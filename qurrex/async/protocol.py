import struct
import socket
import asyncio
from qurrex.log import *
from qurrex.tools import *
from qurrex.messages import *


class TcpProtocol(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.reader = None
        self.writer = None
        self.queue = asyncio.Queue()
        self._ready = asyncio.Event()
        asyncio.ensure_future(self._send_from_queue())
        asyncio.ensure_future(self._receiving_data())

        self.chunk = b''
        self.frame = None

    async def connection_made(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.ip,
            self.port)
        logger.info('Connection made')
        self._ready.set()

    async def _receiving_data(self):
        await self._ready.wait()
        logger.debug('Ready for receive')
        while not self.writer.transport.is_closing():
            data = await self.reader.read(100)
            self.data_received(data)

    def data_received(self, data):
        if self.chunk != b'':
            data = self.chunk + data
            self.chunk = b''
        while len(data) > 0:
            if len(data) >= 12:
                if not self.frame:
                    self.frame = Frame(data[:12])
                    logger.debug("Received Frame:\n%s" % self.frame)
                if len(data) >= 12 + self.frame.msgSize:
                    self.message_received(
                        self.frame,
                        data[12:self.frame.msgSize+12])
                    data = data[12 + self.frame.msgSize:]
                    self.frame = None
                else:
                    self.chunk += data
                    logger.debug("Data chunked:\n%s" % self.chunk)
                    data = b''
            else:
                self.chunk += data
                logger.debug("Data chunked:\n%s" % self.chunk)
                data = b''

    def message_received(self, frame, msg):
        return frame, msg

    async def data_writer(self, data):
        await self.queue.put(data)

    async def _send_from_queue(self):
        await self._ready.wait()
        logger.debug('Ready for send')
        while not self.writer.transport.is_closing():
            data = await self.queue.get()
            self.writer.write(data)


class UdpProtocol(asyncio.DatagramProtocol):

    def __init__(self, address):
        self.address = address
        self.chunk = b''

        self.frame = None

    def connection_made(self, transport):
        self.transport = transport
        sock = self.transport.get_extra_info('socket')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mreqn = struct.pack("=4sl", socket.inet_aton(self.address), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreqn)

    def connection_close(self):
        sock = self.transport.get_extra_info('socket')
        mreqn = struct.pack("=4sl", socket.inet_aton(self.address), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreqn)
        sock.close()
        self.transport.close()

    def datagram_received(self, data, addr):
        if self.chunk != b'':
            data = self.chunk + data
        while len(data) >= 12:
            if not self.frame:
                self.frame = Frame(data[:12])
            if len(data) >= self.frame.msgSize + 12:
                logger.debug('got message from %s msgid %s, size %s, seq %s' \
                    % (format(self.address), msgid, msglen, msgseq))
                self.message_received(
                    self.frame,
                    data[12:self.frame.msgSize+12])
                data = data[self.frame.msgSize+12:]
                self.frame = None
            else:
                self.chunk = data
                data = b''
        else:
            self.chunk = data

    def message_received(self, msgseq, msgid, data):
        return msgid, msgseq, data

    def connection_lost(self, exc):
        logger.error(exc)

    def error_received(self, exc):
        logger.error(exc)
