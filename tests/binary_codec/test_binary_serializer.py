import unittest

from xrpl.binary_codec.binary_wrappers.binary_parser import BinaryParser
from xrpl.binary_codec.binary_wrappers.binary_serializer import BinarySerializer
from xrpl.binary_codec.types.blob import Blob


class TestBinarySerializer(unittest.TestCase):
    # TODO: update this test when write_length_encoded is fully complete.
    # This is currently a sanity check for private _encode_variable_length_prefix,
    # which is called by BinarySerializer.write_length_encoded
    def test_write_length_encoded(self):
        # length ranges: 0 - 192, 193 - 12480, 12481 - 918744
        for case in [100, 1000, 20_000]:
            bytestring = "A2" * case
            blob = Blob.from_value(bytestring)
            self.assertEqual(len(blob), case)  # sanity check
            binary_serializer = BinarySerializer()
            binary_serializer.write_length_encoded(blob)

            binary_parser = BinaryParser(binary_serializer.to_bytes().hex())
            decoded_length = binary_parser._read_length_prefix()
            self.assertEqual(case, decoded_length)
