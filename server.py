import argparse
import logging
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

    def GetSalesCount(
            self,
            request: product_insight_api_pb2.GetSalesCountRequest,
            context
    ) -> product_insight_api_pb2.GetSalesCountResponse:
        # FIXME! Observability.
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
    # FIXME. TLS.
    server.add_insecure_port('[::]:{port}'.format(port=args.port))
    logging.info('starting server')
    server.start()
    logging.info('server started')

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        # FIXME! Graceful stop.
        server.stop(0)


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

    # FIXME! Basic auth.
    parser.add_argument(
        '--username',
        default='dev',
        type=str,
        help='username used to setup basic authorization',
    )
    parser.add_argument(
        '--password',
        default='guess',
        type=str,
        help='password used to setup basic authorization'
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

    logging.basicConfig(
        level=log_level,
    )
    # FIXME! Add unit test.
    serve(args)
