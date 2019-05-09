# CCTV GIF Buffer

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/natm/cctv-gif-buffer/master/LICENSE)
[![Build Status](https://travis-ci.org/natm/cctv-gif-buffer.svg?branch=master)](https://travis-ci.org/natm/cctv-gif-buffer)
[![Coverage Status](https://coveralls.io/repos/github/natm/cctv-gif-buffer/badge.svg?branch=master)](https://coveralls.io/github/natm/cctv-gif-buffer?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/natm/cctv-gif-buffer/badges/quality-score.png)](https://scrutinizer-ci.com/g/natm/cctv-gif-buffer/)
[![Docker build](https://img.shields.io/docker/automated/natmorris/cctv-gif-buffer.svg)](https://hub.docker.com/r/natmorris/cctv-gif-buffer/)

Polls IP CCTV cameras every X time (configurable), stores the last X frames in an in-memory ring buffer per camera. Provides a simple HTTP endpoint to retrieve a GIF. This service is designed to be easily integrated with home automation systems.

Example uses:

* Send you a private message containing the last X frames of motion when the door opens
* Post a GIF to a private slack channel when the door bell is rang

`GET http://<ip_address>:8080/gif?camera=<camera_name>&duration=60&interval=0.25`

![Screenshot](https://raw.github.com/natm/cctv-gif-buffer/master/docs/demo1.gif)

## Configuration

Cameras are listed in YAML configuration file. The poll interval is specified per camera, optionally HTTP basic authentication can be used.

```yaml
cameras:
  frontdoor:
    url: http://192.168.0.9/ISAPI/Streaming/channels/101/picture
    interval: 2
    store: 30
  backdoor:
    url: http://192.168.0.10/jpg/1/image.jpg
    interval: 2
    store: 30
    auth: basic
    username: admin
    password: letmein
server:
  web:
    port: 8080
    listen: 0.0.0.0
```

Per camera fields:

  * `url`: URL to retrieve a JPEG from the camera from. (required)
  * `interval`: Time in seconds between polls (default = 1)
  * `store` : Number of frames to store in the ring buffer (default = 30)
  * `auth`: HTTP authentication type, only `basic` is supported (optional)
  * `username`: HTTP basic authentication username
  * `password`: HTTP basic authentication password

## Usage

`python2.7 buffer.py -c config.yaml`

## Deployment

### Quick and easy - Docker!

```
docker pull e2m32/cctv-gif-buffer:latest
docker run -d --name cctvgifbuffer --rm -v /etc/cctvgifbuffer:/config -p 8080:8080 -t e2m32/cctv-gif-buffer
```

### Dependencies

libjpeg, install on Mac `brew install libjpeg`

### Installation

```
git@github.com:e2m32/cctv-gif-buffer.git
cd cctv-gif-buffer
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## License and Copyright

Copyright 2017 Nat Morris nat@nuqe.net

Licensed under the MIT License.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
