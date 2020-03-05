# Locust-streaming

Load generation tool for evaluation of DASH and HLS video streaming setups


# Local testing for MacOS
Requirements:

```
brew install python3
```

Install the pip3 requirements as follows:
```
pip3 install -r requirements.txt
```

Move to the folder `load_generator/locustfiles/`, add the env variables,
and run locust command.

Replace the ${ORIGIN} with the IP of your Origin the load test.
```
export HOST=${ORIGIN}
```
Run MPEG-DASH script:
```
HOST_URL=http://${HOST} MANIFEST_FILE=tears-of-steel-avc1.ism locust  -f dash_sequence.py
```

Run HLS script:
```
HOST_URL=http://${HOST} MANIFEST_FILE=tears-of-steel-avc1.ism locust  -f hls_player.py
```


# Run Locust client emulator in distributed mode for Ubuntu 18.04
To emulate clients in distributed mode you will need to have at least one master
and one slave node in your cloud infrastructure. In each of these nodes you will
need to pull this repository and install the software from `requirements.txt`.


Pull Github repository to each of the node and install the following
requirements.
```
sudo apt-get update
```

```
sudo apt-get install python3-pip
```


Install the pip3 requirements as follows:
```
pip3 install -r requirements.txt
```


Master/slave ENV configuration variables example:
```
export ORIGIN=ip-172-31-3-3.eu-central-1.compute.internal

export MASTER_CLIENT=ip-172-31-11-128.eu-central-1.compute.internal

export EXPECTED_SLAVES=4
```


## DASH emulator using step load with Locust UI
Master node
```
HOST_URL=http://${ORIGIN} MANIFEST_FILE=tears-of-steel/tears-of-steel-en.ism locust  -f dash_sequence.py --master --expect-slaves=${EXPECTED_SLAVES} --step-load --csv=example
```

Slave node
```
HOST_URL=http://${ORIGIN} MANIFEST_FILE=tears-of-steel/tears-of-steel-en.ism locust  -f dash_sequence.py --slave --master-host=${MASTER_CLIENT} --step-load

```
Access to your http://${ORIGIN}:8089 to visualise Locust UI and to run a
test.


Example test from Locust UI
```
200 users
20 hatch rate
10 users step
2s seconds new step
```


## DASH emulator using step load with Locust UI
Master node
```
HOST_URL=http://${ORIGIN} MANIFEST_FILE=tears-of-steel/tears-of-steel-en.ism locust  -f hls.py --master --expect-slaves=${EXPECTED_SLAVES} --step-load --csv=example
```

Slave node
```
HOST_URL=http://${ORIGIN} MANIFEST_FILE=tears-of-steel/tears-of-steel-en.ism locust  -f hls.py --slave --master-host=${MASTER_CLIENT} --step-load

```
Access to your http://${ORIGIN}:8089 to visualise Locust UI and to run a
test.

Example test from Locust UI
```
200 users
20 hatch rate
10 users step
2s seconds new step
```
