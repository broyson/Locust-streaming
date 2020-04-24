[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3765401.svg)](https://doi.org/10.5281/zenodo.3765401)

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

In the command-line move to directory path `load_generator/`, add
the env variables, and run locust command as follows.

```
cd load_generator
```

Replace the `${ORIGIN_IP}` variable with the IP of the Origin host that will
be stressed.
```
export HOST=${ORIGIN_IP}
```

## Run a load test example with web UI enabled

In this example will run locally the Origin sever in port `80` Locust web UI
in port `8089`.

Set host of Orign server to stress test.
```
export HOST=localhost
```

Run MPEG-DASH example script(`dash_sequence.py`):
```
HOST_URL=http://${HOST} \
MANIFEST_FILE=tears-of-steel-avc1.ism \
mode=vod locust  -f locustfiles/dash_sequence.py
```

Run HLS example script(`hls_player.py`):
```
HOST_URL=http://${HOST} \
MANIFEST_FILE=tears-of-steel-avc1.ism \
mod=vod locust  -f locustfiles/hls_player.py
```

After runnin one of the previous commands, access Lucust web UI in
`http://localhost:8089`, type the number of total users to spawn and the hatch
rate. Then run the test by clicking `Start swarming` button.


## Run a load test example without web UI locally

Set host of Orign server to stress test.
```
export HOST=localhost
```

1) Create a MPEG-DASG stress test by providing the `.ism` file in
`dash_sequence.py`.
 

```
HOST_URL=http://${HOST}  \ 
  MANIFEST_FILE=tears-of-steel-avc1.ism \
  mode=vod locust \
  -f locustfiles/dash_sequence.py \
  --no-web -c 1 -r 1 --run-time 10s --only-summary
```

### Create a stress test(`vod_dash_hls_sequence.py`) to a VOD endpoint by providing an `.mpd` MPEG-DASH manifest or an HLS`.m3u8` master playlist.

1) MPEG-DASH test example that requests all available segments with the lowest
bit-rate.
```
HOST_URL=http://${HOST} \
  MANIFEST_FILE=tears-of-steel-avc1.ism/.mpd \
  mode=vod \
  play_mode=full_playback \
  bitrate=lowest_bitrate \
  locust -f locustfiles/vod_dash_hls_sequence.py \
  --no-web -c 1 -r 1 --run-time 10s --only-summary
```

2) MPEG-DASH test example that requests all available segments with the highest
bit-rate.
```
HOST_URL=http://${HOST} \
  MANIFEST_FILE=tears-of-steel-avc1.ism/.mpd \
  mode=vod \
  play_mode=random_segments \
  bitrate=highest_bitrate \
  locust -f locustfiles/vod_dash_hls_sequence.py \
  --no-web -c 1 -r 1 --run-time 10s --only-summary
```

3) HLS test example that requests all available segments with highest bit-rate.
```
HOST_URL=http://${HOST} \
  MANIFEST_FILE=tears-of-steel-avc1.ism/.m3u8 \
  mode=vod \
  play_mode=full_playback \
  bitrate=highest_bitrate \
  locust -f locustfiles/vod_dash_hls_sequence.py \
  --no-web -c 1 -r 1 --run-time 10s --only-summary
```

4) MEPG-DASH test example that requests all live segments of a Live publishing
point with the highest bit-rates available.

In this example, our publishing point to stress is located in
`test/test.isml/.mpd ` with IP `192.168.178.233` and  port `8818`. Therefore,
we replace the HOST IP from the environment variables and the `MANIFEST_FILE`
variable from the command-line.

```
export HOST=192.168.178.233:8818
```

```
HOST_URL=http://${HOST} \
  MANIFEST_FILE=test/test.isml/.mpd \
  mode=live \
  play_mode=full_playback \
  bitrate=highest_bitrate \
  locust -f locustfiles/vod_dash_hls_sequence.py \
  --no-web -c 1 -r 1 --run-time 10s --only-summary
```

## Using a Locust-streaming Docker image from Docker-hub
In order to run the following examples you will need to have Docker installed
in your computer and pull the following image from Docker Hub.
```
docker pull broyson/locust-streaming:latest
```
Replace the environment variables ORIGIN_IP  and MANIFEST_FILE  with the
Manifest url points that you would like to stress test.

Example using Docker image with external MPEG-DASH manifest
```
External MPEG-DASH manifest
docker run \
    -e "HOST_URL=https://demo.unified-streaming.com" \
    -e "MANIFEST_FILE=/video/ateam/ateam.ism/ateam.mpd" \
    -e "mode=vod" \
    -e "play_mode=full_playback" \
    -e "bitrate=lowest_bitrate" \
    broyson/locust-streaming:latest \
    -f /load_generator/locustfiles/vod_dash_hls_sequence.py \
    --no-web -c 1 -r 1 --run-time 10s --only-summary
```

Example using Docker image with MPEG-DASH Manifest 
```
docker run \
    -e "HOST_URL=http://${ORIGIN_IP}" \
    -e "MANIFEST_FILE=tears-of-steel-avc1.ism/.mpd" \
    -e "mode=vod" \
    -e "play_mode=full_playback" \
    -e "bitrate=lowest_bitrate" \
    broyson/locust-streaming:latest \
    -f /load_generator/locustfiles/vod_dash_hls_sequence.py \
    --no-web -c 1 -r 1 --run-time 10s --only-summary
```

Example using Docker image with local HLS manifest

```
docker run \
    -e "HOST_URL=http://${ORIGIN_IP}" \
    -e "MANIFEST_FILE=tears-of-steel-avc1.ism/.m3u8" \
    -e "mode=vod" \
    -e "play_mode=full_playback" \
    -e "bitrate=lowest_bitrate" \
    -v ${PWD}/:/test/ \
    broyson/locust-streaming:latest  \
    -f /test/load_generator/locustfiles/vod_dash_hls_sequence.py \
    --no-web -c 1 -r 1 --run-time 10s --only-summary
```

# Locust set in distributed mode

##  Run Locust client emulator in distributed mode for Ubuntu 18.04
To emulate clients in distributed mode you will need to have at least one
master and one slave node in your cloud infrastructure. In each of these nodes 
you will need to pull this repository and install the dependencies software
from `requirements.txt`.


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
HOST_URL=http://${ORIGIN} \
  MANIFEST_FILE=tears-of-steel/tears-of-steel-en.ism \ 
  locust  -f dash_sequence.py \ 
  --master --expect-slaves=${EXPECTED_SLAVES} \
  --step-load --csv=example
```

Slave node
```
HOST_URL=http://${ORIGIN} \ 
  MANIFEST_FILE=tears-of-steel/tears-of-steel-en.ism locust \
  -f dash_sequence.py 
  --slave --master-host=${MASTER_CLIENT} 
  --step-load

```
Access to your master node in port `8089` to visualise Locust UI and to run a
test.

Example test from Locust UI
```
200 users
20 hatch rate
10 users step
2s seconds new step
```

## Run HLS example without UI
Master node
```
HOST_URL=http://${ORIGIN} \ 
  MANIFEST_FILE=tears-of-steel/tears-of-steel-en.ism \ 
  locust  -f hls.py \ 
  --master --expect-slaves=${EXPECTED_SLAVES}  \
  --no-web -c 100 -r 10 --run-time 2m \ 
  --step-load --step-clients 10 \
  --step-time 10s --csv=example
```

Slave node
```
HOST_URL=http://${ORIGIN} \ 
  MANIFEST_FILE=tears-of-steel/tears-of-steel-en.ism \ 
  locust  -f hls.py \ 
  --slave --master-host=${MASTER_CLIENT} --step-load
```
