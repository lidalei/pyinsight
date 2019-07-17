# pyinsight

Insight service in Python

* Setup a pipenv environment

```shell
pip install pipenv
pipenv --python $(which python3)
```

* [Install prototool](https://github.com/uber/prototool#installation)

* Install Python grpc

```shell
pipenv install -d grpcio-tools
```

* Define API in a proto file and init prototool

```shell
prototool config init
# lint
# prototool lint
```

* Generate Python code

```shell
pipenv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. insight/v1/product_insight_api.proto
```

* Create API server

```shell
# install grpcio
pipenv install grpcio
# install protobuf
pipenv install protobuf
```

* Run server

```shell
pipenv run python server.py --port 5000 --datafile=transactions.json
```

* Talk to server

```shell
pipenv run python client.py --address=localhost:5000
```

* TODO
  * See FIXME!
  * gRPC gateway
