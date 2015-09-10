import io
import sys


class NoID3HeaderError(Exception):
    pass


class ID3VersionNotSupportedError(Exception):
    pass


class InvalidID3Error(Exception):
    pass


class ID3(object):
    def __init__(self, fileName):
        self._file_stream = io.open(fileName, 'rb')
        self._read_file_identifier()

        if self._file_identifier != [73, 68, 51]:   # = ID3
            print self._file_identifier
            raise NoID3HeaderError('No ID3 header provided in given file')

        self._read_version()

        if self._major_version != 3:
            raise ID3VersionNotSupportedError('The ID3 version %i is currently not supported' % self._major_version)

        self._read_flags()
        self._read_size()

    def _read_file_identifier(self):
        self._file_identifier = [self._read_byte(), self._read_byte(), self._read_byte()]

    def _read_version(self):
        self._major_version = self._read_byte()
        self._minor_version = self._read_byte()

    # todo: implement correct flag reading
    def _read_flags(self):
        self._read_byte()

    def _read_size(self):
        size_bytes = [self._read_byte(), self._read_byte(), self._read_byte(), self._read_byte()]

        for byte in size_bytes:
            if byte >= 128:
                raise InvalidID3Error('Invalid byte in ID3 size')

        # Shift the bit 7 away (set to 0)
        # for byte in size_bytes
        # for more details read the ID3 documentation
        size_bits = []
        for byte in size_bytes:
            is_7_bit = True

            bits = self._to_bits(byte)
            for b in bits:
                if is_7_bit:
                    is_7_bit = False
                    continue
                size_bits.append(b)

        self._size = self._bits_to_int(size_bits)

    def _read_byte(self):
        return ord(self._file_stream.read(1))

    @staticmethod
    def _to_bits(byte):
        for i in reversed(xrange(8)):
            yield (byte >> i) & 1

    @staticmethod
    def _bits_to_int(bits):
        binary_string = ''
        for b in bits:
            binary_string += str(b)

        return int(binary_string, 2)