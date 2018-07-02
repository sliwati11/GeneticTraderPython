import asyncio
import parser
import serializer

class RedisServerProtokol(asyncio.Protocol):

    def __init__(self, db):
        self._db = db

    def connection_made(self, transport):
        self.transport = transport
        '''peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport'''

    def data_received(self, data):
        parsed = parser.parse_wire_protocol(data)
        command = parsed[0].lower()
        if command == b'get':
            response = self._db.get(parsed[1])
        elif command == b'set':
            response = self._db.get(parsed[2])
        elif command == b'subscribe' :
            response = self._pubsub.subscribe(parsed[1], self.transport)
        elif command == b'publish' :
            response = self._pubsub.publish(parsed[1], parsed[2])

        wire_response = serializer.serialize_to_wire(response)
        self.transport.write(wire_response)

        '''message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()'''