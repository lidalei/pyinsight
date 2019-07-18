import argparse
import functools
import logging
import signal
import threading
import time
from concurrent import futures
import grpc
from grpc_reflection.v1alpha import reflection
import json
import typing
from datetime import datetime
from google.protobuf import timestamp_pb2

from insight.v1 import product_insight_api_pb2
from insight.v1 import product_insight_api_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_SERVER_GRACEFUL_STOP_PERIOD = 10

_LOGGER = logging.getLogger('insight/v1')


# ProductInsightServicer implements methods of the ProductInsightAPIServicer service.
class ProductInsightServicer(product_insight_api_pb2_grpc.ProductInsightAPIServicer):
    def __init__(self, datafile: str):
        """
        Init setup the server. It parses data from datafile and pre-processes it properly to enable fast query.
        Each line of the file looks like {"id": 0, "products": [185, 30, 77, 188, 78, ...]}
        In reality, it usually establishes a connection to DB and initializes other services.
        """
        products_inverted_index = {}  # type: typing.Dict[int, typing.List]
        # use UTC now as default timestamp of a transaction.
        now = datetime.utcnow().timestamp()
        with open(datafile) as f:
            for line in f:
                transaction = json.loads(line)
                # FIXME! Dulicates in a transaction.
                for product_id in transaction['products']:
                    if product_id in products_inverted_index:
                        products_inverted_index[product_id].append(now)
                    else:
                        products_inverted_index[product_id] = [now]

        self.products_inverted_index = products_inverted_index
        self.access_token = args.access_token

    def GetSalesCount(
            self,
            request: product_insight_api_pb2.GetSalesCountRequest,
            context: grpc.ServicerContext
    ) -> product_insight_api_pb2.GetSalesCountResponse:
        # FIXME! Observability.
        # authorization
        client_access_token = ''
        for metadata in context.invocation_metadata():
            if 'authorization' == metadata.key:
                client_access_token = str(metadata.value).replace('Bearer ', '', 1)
        if client_access_token != self.access_token:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return product_insight_api_pb2.GetSalesCountResponse()

        start_time = request.start_time  # type: timestamp_pb2.Timestamp
        end_time = request.end_time  # type: timestamp_pb2.Timestamp
        product_id = request.product_id  # type: int

        start_time_epoch = start_time.seconds + start_time.nanos / 1e9  # type: float
        end_time_epoch = end_time.seconds + end_time.nanos / 1e9  # type: float

        if product_id not in self.products_inverted_index:
            return product_insight_api_pb2.GetSalesCountResponse(
                product_id=product_id,
                sales_count=0,
            )

        sales_count = 0  # type: int

        sales_times = self.products_inverted_index[product_id]
        for t in sales_times:
            if start_time_epoch <= t <= end_time_epoch:
                sales_count += 1

        return product_insight_api_pb2.GetSalesCountResponse(
            product_id=product_id,
            sales_count=sales_count,
        )


def serve(args):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    product_insight_api_pb2_grpc.add_ProductInsightAPIServicer_to_server(
        ProductInsightServicer(args.datafile), server)
    # the reflection service will be aware of "ProductInsightAPI" and "ServerReflection" services.
    service_names = (
        product_insight_api_pb2.DESCRIPTOR.services_by_name['ProductInsightAPI'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    # read key and certificate
    with open(args.tls_key, 'rb') as f:
        tlskey = f.read()

    with open(args.tls_cert, 'rb') as f:
        tlscert = f.read()

    # create server credentials
    credentials = grpc.ssl_server_credentials([[tlskey, tlscert]])

    server.add_secure_port('[::]:{port}'.format(port=args.port), server_credentials=credentials)

    _LOGGER.info('starting server')
    server.start()
    _LOGGER.info('server started')

    # stop gracefully
    graceful_stop_handler = functools.partial(handler, server=server)
    signal.signal(signal.SIGINT, graceful_stop_handler)
    signal.signal(signal.SIGTERM, graceful_stop_handler)

    # loop forever
    while True:
        time.sleep(_ONE_DAY_IN_SECONDS)


def handler(signum, frame, server: grpc.Server = None) -> None:
    _LOGGER.info('received signal {}'.format(signum))

    if server is not None:
        event = server.stop(_SERVER_GRACEFUL_STOP_PERIOD)  # type: threading.Event
        # wait until server stops all in-flight rpcs or graceful period expires
        event.wait()
        exit(0)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--port',
        default=5000,
        type=int,
        help='port to listen on',
    )

    parser.add_argument(
        '--datafile',
        default="transactions.json",
        type=str,
        help='data file to parse data, it is usually a DB in a real service',
    )

    parser.add_argument(
        '--tls-key',
        default='key.pem',
        type=str,
        help='TLS private key file, never commit'
    )
    parser.add_argument(
        '--tls-cert',
        default='certificate.pem',
        type=str,
        help='TLS certificate file'
    )

    parser.add_argument(
        '--access-token',
        default='guess',
        type=str,
        help='access token used to setup authorization'
    )

    parser.add_argument(
        '--verbose',
        default=False,
        type=bool,
        help='verbose output',
    )

    args, _ = parser.parse_known_args()

    log_level = logging.WARNING
    if args.verbose:
        log_level = logging.INFO

    _LOGGER.setLevel(log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    _LOGGER.addHandler(ch)

    # FIXME! Add unit test.
    serve(args)
