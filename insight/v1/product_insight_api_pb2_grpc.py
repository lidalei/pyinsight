# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from insight.v1 import product_insight_api_pb2 as insight_dot_v1_dot_product__insight__api__pb2


class ProductInsightAPIStub(object):
  """ProductInsightAPI provides insight about product. 
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetSalesCount = channel.unary_unary(
        '/insight.v1.ProductInsightAPI/GetSalesCount',
        request_serializer=insight_dot_v1_dot_product__insight__api__pb2.GetSalesCountRequest.SerializeToString,
        response_deserializer=insight_dot_v1_dot_product__insight__api__pb2.GetSalesCountResponse.FromString,
        )


class ProductInsightAPIServicer(object):
  """ProductInsightAPI provides insight about product. 
  """

  def GetSalesCount(self, request, context):
    """GetSalesCount returns sales count for a product.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProductInsightAPIServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetSalesCount': grpc.unary_unary_rpc_method_handler(
          servicer.GetSalesCount,
          request_deserializer=insight_dot_v1_dot_product__insight__api__pb2.GetSalesCountRequest.FromString,
          response_serializer=insight_dot_v1_dot_product__insight__api__pb2.GetSalesCountResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'insight.v1.ProductInsightAPI', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
