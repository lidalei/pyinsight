import argparse
import logging
from datetime import datetime, timezone

import grpc
from google.protobuf import timestamp_pb2

from insight.v1 import product_insight_api_pb2
from insight.v1 import product_insight_api_pb2_grpc


def run(args):
    with grpc.insecure_channel(args.address) as channel:
        while True:
            product_id = input('input a product id:')
            if product_id == '':
                logging.info('exit')
                break

            start = timestamp_pb2.Timestamp()
            end = timestamp_pb2.Timestamp()

            start.FromDatetime(
                datetime(2019, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
            )
            end.FromDatetime(
                datetime(2019, 8, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
            )

            stub = product_insight_api_pb2_grpc.ProductInsightAPIStub(channel)
            res = stub.GetSalesCount(
                product_insight_api_pb2.GetSalesCountRequest(
                    start_time=start,
                    end_time=end,
                    product_id=int(product_id)
                )
            )
            logging.info('sales count for {product} from {start} to {end} is {count}'.format(
                product=product_id,
                start=start.ToDatetime(),
                end=end.ToDatetime(),
                count=res.sales_count
            ))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--address',
        default='localhost:5000',
        type=str,
        help='server address',
    )

    args, _ = parser.parse_known_args()

    run(args)
