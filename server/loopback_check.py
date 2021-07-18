from settings.load_settings import LoadSettings
from copy import deepcopy
from sacn.sacn_socket import SACNSocket
from artnet.artnet_socket import ArtNetSocket
from sacn.sacn_main import SACNToArtNet
from artnet.artnet_main import ArtNetTosACN
from networkx import DiGraph, simple_cycles


def make_loopback(test_dict):
    loopback = {}
    for entries in test_dict:
        for universes in test_dict[entries]:
            if test_dict[entries][universes] is True:
                if entries not in loopback:
                    loopback[entries] = []
                loopback[entries].append(universes)
    return loopback


class Loopback:
    def __init__(self):
        self.sacn_socket = SACNSocket()
        self.artnet_socket = ArtNetSocket()
        self.sacn = SACNToArtNet
        self.artnet = ArtNetTosACN

    def test_loopback(self, test_dict=None, universe_in=None):
        test_dict = make_loopback(test_dict)
        artnet_testdict = make_loopback(deepcopy(self.artnet_socket.artnetdict))
        sacn_testdict = make_loopback(deepcopy(self.sacn_socket.sacndict))
        if universe_in == "all" or (self.sacn.sacn_to_artnet is True and self.artnet.artnet_to_sacn is True):
            # Only check for loopback, if 2 or more conversion directions are enabled, since otherwise there is no
            # loopback is possible.
            if universe_in == "sACN":
                protocol_1_loopback = {f"Art-Net: {str(k)}": set(map(lambda x: f"sACN: {str(x)}", v)) for k, v in
                                       artnet_testdict.items()}
                protocol_2_loopback = {f"sACN: {str(k)}": set(map(lambda x: f"Art-Net: {str(x)}", v)) for k, v in
                                 test_dict.items()}
            elif universe_in == "Art-Net":
                protocol_1_loopback = {f"Art-Net: {str(k)}": set(map(lambda x: f"sACN: {str(x)}", v)) for k, v in
                                       test_dict.items()}
                protocol_2_loopback = {f"sACN: {str(k)}": set(map(lambda x: f"Art-Net: {str(x)}", v)) for k, v in
                                 test_dict.items()}
            elif universe_in == "All":
                protocol_1_loopback = {f"Proto 1: {str(k)}": set(map(lambda x: f"Proto 2: {str(x)}", v)) for k, v in
                                       artnet_testdict.items()}
                protocol_2_loopback = {f"Proto 1: {str(k)}": set(map(lambda x: f"Proto 2: {str(x)}", v)) for k, v in
                                 test_dict.items()}
            else:
                raise TypeError("Unknown universe_in type")

            # Merge the protocol_loopback dicts
            protocol_1_loopback.update(protocol_2_loopback)

            # Search for loopbacks
            loopbacks = DiGraph(protocol_1_loopback)
            loopbacks = list(simple_cycles(loopbacks))
            if loopbacks: # If there is a loopback, return the Universes causing the loopback
                message = str(loopbacks).replace("', ", " \u2192")  # Replace commas with an arrow
                return True, f"Loop found: {message}. This would result in packets getting infinitely converted " \
                             f"until the network is overloaded."
            else:
                return False, None
        else:
            return False, None

