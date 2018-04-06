# Qurrex Matching Testing Protocol
Open Source [Qurrex](https://qurrex.com/) protocol library implemented in Python 3.5

### Features
---
TCP Connection with support messaging:
- [x] NewOrderRequest / NewOrderReport
- [x] CancelRequest / CancelReport
- [x] MassCancelRequest / MassCancelReport
- [x] ExecutionReport
- [x] RejectReport

UDP Channels support:
- [ ] BestPrices
- [ ] OrderBook
- [ ] Trades

### Instalation
---
```
python3 setup.py sdist
python3 -m pip install dist/qurrex-{version}.tar.gz 
```


### Usage Example
---

```

loop = asyncio.get_event_loop()
session = QurrexSession(IP_ADDR, PORT)
loop.run_until_complete(session.connect())
loop.run_forever()

```

### Documentation of protocol
---
