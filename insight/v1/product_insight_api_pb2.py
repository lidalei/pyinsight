# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: insight/v1/product_insight_api.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='insight/v1/product_insight_api.proto',
  package='insight.v1',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n$insight/v1/product_insight_api.proto\x12\ninsight.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\x88\x01\n\x14GetSalesCountRequest\x12.\n\nstart_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\nproduct_id\x18\x03 \x01(\x03\"@\n\x15GetSalesCountResponse\x12\x12\n\nproduct_id\x18\x01 \x01(\x03\x12\x13\n\x0bsales_count\x18\x02 \x01(\x03\x32i\n\x11ProductInsightAPI\x12T\n\rGetSalesCount\x12 .insight.v1.GetSalesCountRequest\x1a!.insight.v1.GetSalesCountResponseb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_GETSALESCOUNTREQUEST = _descriptor.Descriptor(
  name='GetSalesCountRequest',
  full_name='insight.v1.GetSalesCountRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='start_time', full_name='insight.v1.GetSalesCountRequest.start_time', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end_time', full_name='insight.v1.GetSalesCountRequest.end_time', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_id', full_name='insight.v1.GetSalesCountRequest.product_id', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=86,
  serialized_end=222,
)


_GETSALESCOUNTRESPONSE = _descriptor.Descriptor(
  name='GetSalesCountResponse',
  full_name='insight.v1.GetSalesCountResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='product_id', full_name='insight.v1.GetSalesCountResponse.product_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sales_count', full_name='insight.v1.GetSalesCountResponse.sales_count', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=224,
  serialized_end=288,
)

_GETSALESCOUNTREQUEST.fields_by_name['start_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_GETSALESCOUNTREQUEST.fields_by_name['end_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['GetSalesCountRequest'] = _GETSALESCOUNTREQUEST
DESCRIPTOR.message_types_by_name['GetSalesCountResponse'] = _GETSALESCOUNTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetSalesCountRequest = _reflection.GeneratedProtocolMessageType('GetSalesCountRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSALESCOUNTREQUEST,
  '__module__' : 'insight.v1.product_insight_api_pb2'
  # @@protoc_insertion_point(class_scope:insight.v1.GetSalesCountRequest)
  })
_sym_db.RegisterMessage(GetSalesCountRequest)

GetSalesCountResponse = _reflection.GeneratedProtocolMessageType('GetSalesCountResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETSALESCOUNTRESPONSE,
  '__module__' : 'insight.v1.product_insight_api_pb2'
  # @@protoc_insertion_point(class_scope:insight.v1.GetSalesCountResponse)
  })
_sym_db.RegisterMessage(GetSalesCountResponse)



_PRODUCTINSIGHTAPI = _descriptor.ServiceDescriptor(
  name='ProductInsightAPI',
  full_name='insight.v1.ProductInsightAPI',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=290,
  serialized_end=395,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetSalesCount',
    full_name='insight.v1.ProductInsightAPI.GetSalesCount',
    index=0,
    containing_service=None,
    input_type=_GETSALESCOUNTREQUEST,
    output_type=_GETSALESCOUNTRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PRODUCTINSIGHTAPI)

DESCRIPTOR.services_by_name['ProductInsightAPI'] = _PRODUCTINSIGHTAPI

# @@protoc_insertion_point(module_scope)
