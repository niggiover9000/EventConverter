from sacn.sacn_socket import SACNSocket
from sacn.sacn_input import SACNInput
from socket import timeout
from io import BlockingIOError


class SACNToArtNet:
    def __init__(self):
        self.socket = SACNSocket()
        self.sacn_input = SACNInput()

    def sacn_to_artnet(self):
        """
        Converts the received raw sACN data to raw sACN data than can be sent
        :return: None
        """
        while True:
            try:
                input_packet, input_ip = self.socket.sacn_socket.recvfrom(1143)
            except(timeout, BlockingIOError):  # Ignore timeouts and blocked socket errors
                continue
            self.sacn_input.new_packet(input_packet)
            self.sacn_input.identify_packet()


if __name__ == "__main__":
    sacn = SACNToArtNet()
    sacn.sacn_to_artnet()
