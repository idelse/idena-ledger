# Ledger Idena app
This repository contains:

- Ledger Nano S/X Idena app
- Specs / Documentation
- C++ unit tests

## Installing

# Building

At the moment, the only option is to build the app on your own. **Please only use a TEST DEVICE!**

Once the app is ready and we reach v1.0.0, it will be submitted to Ledger so it is published in the app Catalog.

## Dependencies

### Ledger Nano S

- This project requires Ledger firmware 1.6

- The current repository keeps track of Ledger's SDK but it is possible to override it by changing the git submodule.

### Docker CE

- Please install docker CE. The instructions can be found here: https://docs.docker.com/install/

### Ubuntu Dependencies
- Install the following packages:
   ```
   sudo apt update && apt-get -y install build-essential git wget cmake \
  libssl-dev libgmp-dev autoconf libtool
   ```

### Python Dependencies
- virtualenv must use python3
```
virtualenv .envs/ledger -p python3
source .envs/ledger/bin/activate
pip install -r requirements.txt
```

### Prepare your development device

   **Please do not use a Ledger device with funds for development purposes.**

   **Have a second device that is used ONLY for development and testing**

   There are a few additional steps that increase reproducibility and simplify development:

**1 - Ensure your device works in your OS**
- In Linux hosts it might be necessary to adjust udev rules, etc. Refer to Ledger documentation: https://support.ledger.com/hc/en-us/articles/115005165269-Fix-connection-issues
- In MaxOS Ledger Live app must be closed

**2 - Set a test mnemonic**

All our tests expect the device to be configured with a known test mnemonic.

- Plug your device while pressing the right button

- Your device will show "Recovery" in the screen

- Double click

- Run `make dev_init`. This will take about 2 minutes. The device will be initialized to:

   ```
   PIN: 5555
   Mnemonic: equip will roof matter pink blind book anxiety banner elbow sun young
   Private key index 0: dfa1be0964f736f1534e135428d5704ee2505dfae0a4075a694018d9aa7518c9
   ```

**3 - Add a development certificate**

- Plug your device while pressing the right button

- Your device will show "Recovery" in the screen

- Click both buttons at the same time

- Enter your pin if necessary

- Run `make dev_ca`. The device will receive a development certificate to avoid constant manual confirmations.


# Building the Ledger App

The Makefile will build the firmware in a docker container and leave the binary in the correct directory.

- Build

   The following command will build the app firmware inside a container and load to your device:
   ```
   source .envs/ledger/bin/activate
   make                # Builds the app
   ```

- Upload to a device
   The following command will upload the application to the ledger. _Warning: The application will be deleted before uploading._
   ```
   source .envs/ledger/bin/activate
   make load          # Builds and loads the app to the device
   ```

# Development (EMU)

## Run emulated app

### MacOS Dependencies
- Install [xQuartz](https://www.xquartz.org/)

### First time EMU execution
```
source .envs/ledger/bin/activate
open -a XQuartz
xhost + $(hostname)
export DISPLAY=docker.for.mac.localhost:0
make env
```

### EMU execution
```
source ledger/bin/activate
make env
```
