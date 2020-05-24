# idena-ledger
Idena wallet application framework for Nano S and Nano X

## How to install
This app is still not available in [Ledger Live](https://www.ledger.com/ledger-live/), so you will have to build and
install it manually.

### Requirements
- [docker](https://www.docker.com/)
- [python3](https://www.python.org/download/releases/3.0/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

### 1. Install python environment
```
virtualenv .envs/ledger -p python3
source .envs/ledger/bin/activate
pip install -r requirements.txt
```

### 2. Build the app
```
make build
```

### 3. Install
```
make load
```

## Supported clients
- [idena-pocket](http://pocket.idena.dev/)

## Links
- [Documentation](https://www.idena.dev/idena-ledger)
- [Telegram](https://t.me/idenadev)

---
Consider supporting idena-ledger by donating to `0x62449c9b1029db6df55ecf215d0aaa0cea23c66d`
