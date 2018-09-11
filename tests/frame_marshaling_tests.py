# -*- encoding: utf-8 -*-
import unittest
import uuid

from pamqp import body, frame, header, heartbeat, specification


class MarshalingTests(unittest.TestCase):

    def test_protocol_header(self):
        expectation = b'AMQP\x00\x00\t\x01'
        response = header.ProtocolHeader().marshal()
        self.assertEqual(response,
                         expectation,
                         "ProtocolHeader did not match expectation")

    def test_basic_ack(self):
        expectation = (b'\x01\x00\x01\x00\x00\x00\r\x00<\x00P\x00\x00\x00'
                       b'\x00\x00\x00\x00\x01\x00\xce')
        frame_obj = specification.Basic.Ack(1, False)
        response = frame.marshal(frame_obj, 1)
        self.assertEqual(response, expectation,
                         "Basic.Ack did not match expectation")

    def test_basic_cancel(self):
        expectation = (b'\x01\x00\x01\x00\x00\x00\r\x00<\x00\x1e\x07'
                       b'ctag1.0\x00\xce')
        frame_obj = specification.Basic.Cancel(consumer_tag='ctag1.0')
        response = frame.marshal(frame_obj, 1)
        self.assertEqual(response, expectation,
                         "Basic.Cancel did not match expectation")

    def test_basic_cancelok(self):
        expectation = (b'\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x1f\x07'
                       b'ctag1.0\xce')
        frame_obj = specification.Basic.CancelOk(consumer_tag='ctag1.0')
        response = frame.marshal(frame_obj, 1)
        self.assertEqual(response, expectation,
                         "Basic.Cancel did not match expectation")

    def test_basic_consume(self):
        expectation = (b'\x01\x00\x01\x00\x00\x00\x15\x00<\x00\x14\x00'
                       b'\x00\x03bar\x05ctag0\x00\x00\x00\x00\x00\xce')
        frame_obj = specification.Basic.Consume(0, 'bar', 'ctag0',
                                                False, False, False, False)
        response = frame.marshal(frame_obj, 1)
        self.assertEqual(response, expectation,
                         "Basic.Consume did not match expectation")

    def test_heartbeat(self):
        expectation = b'\x08\x00\x00\x00\x00\x00\x00\xce'
        response = frame.marshal(heartbeat.Heartbeat(), 0)
        self.assertEqual(response, expectation,
                         "Heartbeat did not match expectation")

    def test_body(self):
        value = str(uuid.uuid4()).encode('utf-8')
        self.assertEqual(body.ContentBody(value).marshal(), value)
        self.assertEqual(len(body.ContentBody(value)), len(value))
