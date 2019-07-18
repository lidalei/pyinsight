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
# install grpcio-reflection
pipenv install grpcio-reflection
```

* Run server

```shell
pipenv run python server.py --port 5000 --datafile=transactions.json
```

* Talk to server

```shell
pipenv run python client.py --address=localhost:5000
```

or use [grpcurl](https://github.com/fullstorydev/grpcurl#installation)


```shell
grpcurl -plaintext -d '{"start_time": "2019-01-01T00:00:00Z", "end_time":"2019-08-01T00:00:00Z", "product_id": 185}' localhost:5000 insight.v1.ProductInsightAPI/GetSalesCount
#{
#  "product_id": 185,
#  "sales_count": 97
#}
```

* TODO
  * See FIXME!
  * gRPC gateway
