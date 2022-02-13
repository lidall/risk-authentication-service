# Risk Authentication Service

[![Build Status](https://app.travis-ci.com/lidall/risk-authentication-service.svg?branch=main)](https://app.travis-ci.com/lidall/risk-authentication-service)

This app is intended to identify the user risk level from log chunks.

## Install & Usage

If you want to build and run by using docker:

```
$ docker build -t risk_authentication:v1
$ docker run -d -p 8080:8080 --name risk_server risk_authentication:v1
```

---

If you want to install as a python package:
```
$ pip install .
```

Then, a simple example of customizing your own request link:

```
from aiohttp import web
from risk_authentication import Handler


def main():
    handler = Handler()
    app = web.Application()
    app.add_routes([web.get('/isuserknown',
                            handler.handle_user_check),
                    web.post('/upload_log', handler.handle_log)])
    web.run_app(app)


if __name__ == "__main__":
    main()
```

## Implementation Doc

Refer to [here](docs/doc.md) to see the current implementation of the risk authentication server.

## Golang Implementation

Refer to [here](https://github.com/lidall/risk_auth_go) to see the Golang implementation of the risk authentication server.

