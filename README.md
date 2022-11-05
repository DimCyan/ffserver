# FFServer

![](https://github.com/nanarino/ffserver/blob/main/static/screenshot/ffserver.png)

Fastapi-based file service management (Python3.8+)


## Frontend

[https://github.com/mowtwo/ffserver_frontend](https://github.com/mowtwo/ffserver_frontend)

## Screenshots

- ipadmini

    ![ipadmini](https://github.com/nanarino/ffserver/blob/main/static/screenshot/ipadmini.png)

## Features

- Imitation win10 explorer

## Installation

### Installed by using source code

1. Install dependences via pip
    ```
    pip install -r requirements.txt
    ```

2. Excute `main.py`
    ```
    python -m main
    ```

3. API document: [FFServer API](http://127.0.0.1:8010/docs)

4. Open Browser With URL: [http://127.0.0.1:8010/](http://127.0.0.1:8010/)

### Installed by docker pull

1. Pull image via `docker pull`
    ```
    docker pull simonwdc/ffserver:0.1
    ```
2. Create container
    ```
    docker run -itd -p 8010:8010 --name=ffserver simonwdc/ffserver:0.1
    ```
    > Or mount `bucket` to a local path
    ```
    docker run -itd -p 8010:8010 -v <LocalPath>:/ffserver/bucket --name=ffserver simonwdc/ffserver:0.1
    ```
3. API document: [FFServer API](http://127.0.0.1:8010/docs)

4. Open Browser With URL: [http://127.0.0.1:8010/](http://127.0.0.1:8010/)

## TODO

1. [x] move and rename

2. [ ] Support QRCode

3. [x] Create folder

4. [ ] Support copy link

5. [x] Support Docker

## Special thanks

[mowtwo](https://github.com/mowtwo)

