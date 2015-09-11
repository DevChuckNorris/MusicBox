import io


class NoID3HeaderError(Exception):
    pass


class ID3VersionNotSupportedError(Exception):
    pass


class InvalidID3Error(Exception):
    pass


class ID3TagNotFoundError(Exception):
    pass


class ID3(object):
    def __init__(self, fileName):
        self._file_stream = io.open(fileName, 'rb')
        self._file_stream_pos = 0
        self._frames = {}
        self._read_file_identifier()

        if self._file_identifier != [73, 68, 51]:   # = ID3
            print self._file_identifier
            raise NoID3HeaderError('No ID3 header provided in given file')

        self._read_version()

        if self._major_version != 3:
            raise ID3VersionNotSupportedError('The ID3 version %i is currently not supported' % self._major_version)

        self._read_flags()
        self._read_size()
        # Now we are at the position of the first frame (read it 4 chars)
        self._read_frames()

    def get_frame(self, frame):
        if frame not in self._frames:
            raise ID3TagNotFoundError('Failed to find frame "%s" in ID3' % frame)

        return self._frames[frame]

    def contains_frame(self, frame):
        return frame in self._frames

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

        # Remove the "7 bit" away
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

    def _read_frames(self):
        while self._file_stream_pos < self._size + 10:
            current_frame = [self._read_char(), self._read_char(), self._read_char(), self._read_char()]
            frame_size = self._read_int()
            frame_flags = [self._read_char(), self._read_char()]

            # todo implement frame_flags
            # print '%s size %i' % (current_frame, frame_size)

            if current_frame[0] == 'T':
                frame_data = self._read_text(frame_size)
            else:
                frame_data = self._read_in_chunks(frame_size)
            self._frames[bytearray(current_frame).decode('UTF8')] = frame_data

    def _read_char(self):
        self._file_stream_pos += 1
        return self._file_stream.read(1)

    def _read_byte(self):
        return ord(self._read_char())

    def _read_int(self):
        int_data = [self._read_byte(), self._read_byte(), self._read_byte(), self._read_byte()]
        byte_string = ''.join('{:02x}'.format(x) for x in int_data)

        return int(byte_string, 16)

    def _read_in_chunks(self, n):
        self._file_stream_pos += n

        ret_val = []
        for x in xrange(0, n):
            ret_val.append(self._file_stream.read(1))

        return ret_val

    def _read_text(self, length):
        data = self._read_in_chunks(length)

        ret = ''
        if data[0] == '\x01' or data[0] == '\x02':
            data.pop(0)
            ret = bytearray(data).decode('UTF16')
        elif data[0] == '\x03':
            data.pop(0)
            ret = bytearray(data).decode('UTF8')

        return ret

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
