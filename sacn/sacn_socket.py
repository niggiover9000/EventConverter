from settings.load_settings import LoadSettings
from socket import gethostname, gethostbyname, socket as sock, AF_INET, SOCK_DGRAM, IPPROTO_UDP, SOL_SOCKET, SO_REUSEADDR, SOL_IP, IP_ADD_MEMBERSHIP, inet_aton
from sacn.sacn_params import ACN_SDT_MULTICAST_PORT


def calculate_multicast_address(universe):
    """
    Calcutates the multicast address needed to send to the sACN universe
    :param universe: universe number
    :return: String: Universe Multicast Address
    """
    hibyte = universe >> 8
    lobyte = universe & 0xFF
    return f"239.255.{hibyte}.{lobyte}"


class SACNSocket:
    """
    Used to receive and send the raw sACN data

    sacn_socket = SACNSocket()
    sacn_socket.set_sacn_socket()
    """
    def __init__(self):
        self.ip = None
        self.port = None
        self.sacndict = {}
        self.load_sacn_socket()
        self.sacn_socket = self.set_sacn_socket()

    def load_sacn_socket(self):
        """
        This will load all the settings for the sacn socket from the settings.dat. If no values are stored, the
        default value will be used
        :return: None
        """
        loading = LoadSettings()
        loading.open_settings("sACN", "ip", gethostbyname(gethostname()))
        self.ip = loading.load_settings()
        loading.open_settings("sACN", "port", ACN_SDT_MULTICAST_PORT)
        self.port = loading.load_settings()
        loading.open_settings("sACN", "sacndict", {})
        self.sacndict = loading.load_settings()

    def set_sacn_socket(self):
        """
        Sets up the socket for sACN multicast sending and receiving
        :return: socket object
        """
        self.sacn_socket = sock(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        try:
            self.sacn_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
            self.sacn_socket.bind((self.ip, self.port))
        except OSError as error:
            print("Can't bind to port {self.port}. Please close all applications using this port and try again. "
                  f"{error}")
        multicast_list = []
        for universe in self.sacndict:  # Add membership to Multicast Adresses for every universe
            multicast_address = calculate_multicast_address(universe)
            self.sacn_socket.setsockopt(SOL_IP, IP_ADD_MEMBERSHIP, inet_aton(multicast_address) + inet_aton(self.ip))
            multicast_list.append(multicast_address)
        print(f"Added Membership to Multicast Adresses: {multicast_list}")
        print(f"sACN IP {self.ip}:{self.port}")
        return self.sacn_socket
