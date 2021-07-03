from settings.load_settings import LoadSettings
from artnet.artnet_params import ID, PROT_VER_HI, PROT_VER_LO, OP_POLL, OP_POLL_REPLY, OP_IP_PROG, OP_IP_PROG_REPLY, \
    OP_ADDRESS, OP_DIAG_DATA, OP_TIME_CODE, OP_COMMAND, OP_TRIGGER, OP_DMX, OP_SYNC, OP_NZS, OP_INPUT, \
    OP_FIRMWARE_MASTER, OP_FIRMWARE_REPLY, OP_TOD_REQUEST, OP_TOD_DATA, OP_TOD_CONTROL, OP_RDM, OP_RDM_SUB
from sacn.sacn_output import SACNOutput


class ArtNetInput:
    def __init__(self):
        self.artnet_packet = {}
        self.artnet_data = {}
        self.artnet_to_sacn = False
        self.merge_artnet = False
        self.load_artnet_input()
        self.sacn_output = SACNOutput()

    def load_artnet_input(self):
        """
        This will load all the settings for the artnet input from the settings.dat. If no values are stored, the
        default value will be used
        :return: None
        """
        loading = LoadSettings()
        loading.open_settings("Art-Net", "artnet_to_sacn", False)
        self.artnet_to_sacn = loading.load_settings()
        loading.open_settings("Art-Net", "merge_artnet", False)
        self.merge_artnet = loading.load_settings()

    def new_packet(self, packet):
        """Updates the Art-Net data
        :param packet: The raw artnet data
        :return: None
        """
        self.artnet_packet = packet

    def merge_artnet_inputs(self):
        """
        # Todo
        Merging is not provided in the standard, but would be a useful feature to implement later on. At the moment,
        this function does nothing.
        :return: None
        """
        pass

    def identify_packet(self):
        """
        Calls the analyzer function for the identified type of packet.
        :return: Type of packet
        """
        op_code = tuple(reversed(self.artnet_packet[8:10]))
        if tuple(self.artnet_packet[0:8]) != ID:
            print("Unknown packed ID.")
        elif self.artnet_packet[10] != PROT_VER_HI or self.artnet_packet[11] != PROT_VER_LO:
            print("Unknown protocol version.")
        elif op_code == OP_POLL:
            pass
        elif op_code == OP_POLL_REPLY:
            pass
        elif op_code == OP_IP_PROG:
            pass
        elif op_code == OP_IP_PROG_REPLY:
            pass
        elif op_code == OP_ADDRESS:
            pass
        elif op_code == OP_DIAG_DATA:
            pass
        elif op_code == OP_TIME_CODE:
            pass
        elif op_code == OP_COMMAND:
            pass
        elif op_code == OP_TRIGGER:
            pass
        elif op_code == OP_DMX:
            self.artnet_dmx_input()
        elif op_code == OP_SYNC:
            pass
        elif op_code == OP_NZS:
            pass
        elif op_code == OP_INPUT:
            pass
        elif op_code == OP_FIRMWARE_MASTER:
            pass
        elif op_code == OP_FIRMWARE_REPLY:
            pass
        elif op_code == OP_TOD_REQUEST:
            pass
        elif op_code == OP_TOD_DATA:
            pass
        elif op_code == OP_TOD_CONTROL:
            pass
        elif op_code == OP_RDM:
            pass
        elif op_code == OP_RDM_SUB:
            pass

    def artnet_dmx_input(self):
        """
        Function is called if this is a normal DMX packet (Start Code = 0x00). Creates a dictionary with all the
        information we can get from this package
        :return: Dict containing the analyzed information of the artnet packet
        """
        if self.artnet_to_sacn is True:
            self.artnet_data = {"sequence_number": self.artnet_packet[12], "physical_port": self.artnet_packet[13],
                                "universe": tuple(self.artnet_packet[14:16]), "universe_lobyte": self.artnet_packet[14],
                                "universe_hibyte": self.artnet_packet[15], "length": tuple(self.artnet_packet[16:18]),
                                "dmx_data": self.artnet_packet[18:530]}
            self.merge_artnet_inputs()
            self.sacn_output.sacn_dmx_output(self.artnet_data)
        else:
            # Do nothing if converting is turned off
            pass
