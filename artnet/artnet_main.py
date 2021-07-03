from artnet.artnet_socket import ArtNetSocket
from artnet.artnet_input import ArtNetInput
from socket import timeout
from io import BlockingIOError


class ArtNetTosACN:
    def __init__(self):
        self.socket = ArtNetSocket()
        self.artnet_input = ArtNetInput()

    def artnet_to_sacn(self):
        """
        Converts the received raw Art-Net data to raw sACN data than can be sent
        :return: None
        """
        while True:
            try:
                input_packet, input_ip = self.socket.artnet_socket.recvfrom(1143)
            except (timeout, BlockingIOError):  # Ignore timeouts and blocked socket errors
                continue
            self.artnet_input.new_packet(input_packet)
            self.artnet_input.identify_packet()


if __name__ == "__main__":
    artnet = ArtNetTosACN()
    artnet.artnet_to_sacn()
