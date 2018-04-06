import binascii


def ByteToHex(byteStr):

    return binascii.hexlify(byteStr)


def HexToByte(hexStr):
    return binascii.unhexlify(hexStr)
