from socket import gethostname, gethostbyname, socket as sock, AF_INET, SOCK_DGRAM, IPPROTO_UDP, SOL_SOCKET, \
    SO_BROADCAST, SO_REUSEADDR
from settings.load_settings import LoadSettings
from artnet.artnet_params import UDP_PORT


class ArtNetSocket:
    """
    Used to receive and send the raw Art-Net data

    artnet_socket = ArtNetSocket()
    artnet_socket.set_artnet_socket()
    """

    def __init__(self):
        self.ip = None
        self.port = None
        self.broadcast = None
        self.broadcast_ip = None
        self.artnetdict = {}
        self.load_artnet_socket()
        self.artnet_socket = self.set_artnet_socket()

    def load_artnet_socket(self):
        """
        This will load all the settings for the artnet socket from the settings.dat. If no values are stored, the
        default value will be used
        :return: None
        """
        loading = LoadSettings()
        loading.open_settings("Art-Net", "ip", gethostbyname(gethostname()))
        self.ip = loading.load_settings()
        loading.open_settings("Art-Net", "port", UDP_PORT)
        self.port = loading.load_settings()
        loading.open_settings("Art-Net", "broadcast", False)
        self.broadcast = loading.load_settings()
        loading.open_settings("Art-Net", "broadcast_ip", "255.255.255.255")
        self.broadcast_ip = loading.load_settings()

    def set_artnet_socket(self):
        """
        Sets up the socket for Art-Net broadcast sending and receiving
        :return: socket object
        """
        self.artnet_socket = sock(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.artnet_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        self.artnet_socket.setblocking(False)
        try:
            self.artnet_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
            self.artnet_socket.bind((self.ip, self.port))
        except OSError as error:
            print(f"Can't bind to port {self.port}. Please close all applications using this port and try again. "
                  f"{error}")
        print(f"Artnet Broadcast IP: {self.broadcast_ip}:{self.port}")
        print(f"Artnet IP: {self.ip}:{self.port}")
        return self.artnet_socket
