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
# generate tls certs, choose common as `localhost`. Note the private key file should never be commmited in reality.
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
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
# list all services
grpcurl -plaintext localhost:5000 list
```

gives

```text
grpc.reflection.v1alpha.ServerReflection
insight.v1.ProductInsightAPI
```

```shell
# describe ProductInsightAPI
grpcurl -plaintext localhost:5000 describe insight.v1.ProductInsightAPI
```

gives

```text
insight.v1.ProductInsightAPI is a service:
service ProductInsightAPI {
  rpc GetSalesCount ( .insight.v1.GetSalesCountRequest ) returns ( .insight.v1.GetSalesCountResponse );
}
```

```shell
grpcurl -plaintext -d '{"start_time": "2019-01-01T00:00:00Z", "end_time":"2019-08-01T00:00:00Z", "product_id": 185}' localhost:5000 insight.v1.ProductInsightAPI/GetSalesCount
```

gives

```text
{
  "product_id": 185,
  "sales_count": 97
}
```

* Add Dockerfile

```shell
# build docker image
docker build --pull -t insight:v1 .
# run docker container
docker run -p 5000:80 -v $TRANSACTION_FILE:/data/transactions.json insight:v1
```

* TODOs
  * See FIXME!
  * horizontaly scale the service with kubernetes
  * expose the service as an HTTP service with gRPC gateway
