# coding=utf-8
import requests
from functools import wraps
from py_zipkin.zipkin import zipkin_span
from py_zipkin.transport import BaseTransportHandler
from logs import exception_logger


class HttpTransport(BaseTransportHandler):
    def get_max_payload_bytes(self):
        return None

    def send(self, encoded_span):
        try:
            requests.post(
                'http://localhost:9411/api/v1/spans',
                data=encoded_span,
                headers={'Content-Type': 'application/x-thrift'},
            )
        except Exception as e:
            exception_logger.exception('http send exception:%s' % e)


def rlog(*args, **kwargs):
    def _0(f):
        @wraps(f)
        def _1(*args, **kwargs):
            with zipkin_span(
                service_name='practice-rlog',
                span_name=f.__name__,
                transport_handler=HttpTransport(),
                port=8922,
                sample_rate=100, # Value between 0.0 and 100.0
            ):  
                ret = f(*args, **kwargs)
            return ret 
        return _1
    return  _0 


def zipkin_span_dec():
    def _0(f):
        @wraps(f)
        def _1(*args, **kwargs):
            with zipkin_span(
                service_name='practice-rlog',
                span_name=f.__name__,
            ):  
                ret = f(*args, **kwargs)
            return ret 
        return _1
    return  _0 
