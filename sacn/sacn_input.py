from time import time
from artnet.artnet_output import ArtNetOutput
from sacn.sacn_output import calculate_decimal
from sacn.sacn_params import VECTOR_E131_DATA_PACKET, VECTOR_E131_EXTENDED_SYNCHRONIZATION, \
    VECTOR_E131_EXTENDED_DISCOVERY, DEFAULT_NULL_START_CODE, E120_RDM_START_CODE, \
    ELECTRONIC_THEATRE_CONTROLS_START_CODE, PREAMBLE_SIZE, POST_AMBLE_SIZE, ACN_PACKET_IDENTIFIER, \
    VECTOR_ROOT_E131_DATA, VECTOR_DMP_SET_PROPERTY, ADDRESS_TYPE_DATA_TYPE, FIRST_PROPERTY_ADDRESS, ADDRESS_INCREMENT, \
    E131_NETWORK_DATA_LOSS_TIMEOUT
from settings.load_settings import LoadSettings


def flush_buffer(buffer_size):
    """
    Create an empty bytarray with the lenght of the buffer size
    :param buffer_size: Lenght of the bytearray
    :return: Bytearray
    """
    buffer = bytearray(buffer_size)
    return buffer


class SACNInput:
    def __init__(self):
        self.sacn_packet = {}
        self.sacn_data = {}
        self.merge_dict = {}
        self.sacn_to_artnet = False
        self.merge_sacn = False
        self.per_channel_priority = True
        self.load_sacn_input()

        self.artnet_output = ArtNetOutput()

        # Merging Vars
        self.universe = 0
        self.cid = None
        self.cids = None
        self.dmx_position = 0
        self.output_dmx_data = flush_buffer(512)
        self.output_priority = flush_buffer(512)

    def load_sacn_input(self):
        """
        This will load all the settings for the sACN input from the settings.dat. If no values are stored, the
        default value will be used
        :return: None
        """
        loading = LoadSettings()
        loading.open_settings("Art-Net", "artnet_to_sacn", False)
        self.sacn_to_artnet = loading.load_settings()
        loading.open_settings("Art-Net", "merge_artnet", False)
        self.merge_sacn = loading.load_settings()
        loading.open_settings("Art-Net", "per_channel_priority", True)
        self.per_channel_priority = loading.load_settings()

    def new_packet(self, packet):
        """Updates the sACN data
        :param packet: The raw artnet data
        :return: None
        """
        self.sacn_packet = packet

    def merge_sacn_inputs(self):
        """
        Creates a list of all senders and merges their inputs together.
        The following settings are observed:
        - per_channel_priority = True/False
        - merging = True/False
        :return: None
        """
        if self.merge_sacn is True:
            self.universe = self.sacn_data["universe"]
            self.cid = self.sacn_data["cid"]
            if self.universe not in self.merge_dict:
                self.add_universe()
            if self.cid not in self.merge_dict[self.universe]:
                self.add_cid()
            if "priority" not in self.merge_dict[self.universe][self.cid]:
                self.add_priority()

            self.update_time()
            self.update_dmx_data()
            self.output_priority = flush_buffer(512)
            self.output_dmx_data = flush_buffer(512)

            for self.cids in self.merge_dict[self.universe]:
                for self.dmx_position in range(len(self.merge_dict[self.universe])):  # Check ToDo
                    if self.per_channel_priority is True:
                        self.per_channel_priority_merging()
                    else:
                        self.traditional_merging()
            for _ in self.merge_dict:
                # If a universe has a timeout, remove it from the dictionary, so it won't overwrite the priority of
                # the other active universes.
                for self.cids in self.merge_dict[self.universe]:
                    self.remove_timeout_universes()
        else:
            # If merging is turned off, do nothing.
            pass

    def add_universe(self):
        """
        Add a Universe
        Create a new entry for a universe if not already created
        :return: None
        """
        self.merge_dict[self.sacn_data["universe"]] = {}

    def add_cid(self):
        """
        Add a CID
        Create new entry for a CID if not already created
        :return: None
        """
        self.merge_dict[self.sacn_data["universe"]].update({self.sacn_data["cid"]: {}})

    def add_priority(self):
        """
        Create a new entry for a per-channel-priority if not already created
        :return: None
        """
        per_channel_priority = bytearray()  # Create empty bytearray
        for i in range(len(self.sacn_data["priority"])):
            per_channel_priority.append(self.sacn_data["priority"])  # Copy universe priority to every channel
        # Update merge_dict
        self.merge_dict[self.sacn_data["universe"]][self.sacn_data["cid"]].update(priority=per_channel_priority)

    def update_time(self):
        """
        Update the universe timeout time to the actual time. If a CID hasn't sent for more than 2 seconds, it will
        time out.
        :return: None
        """
        self.merge_dict[self.sacn_data["universe"]][self.sacn_data["cid"]].update(time=time())

    def update_dmx_data(self):
        """
        Update the DMX data with the newest DMX input from the CID
        :return: None
        """
        self.merge_dict[self.sacn_data["universe"]][self.sacn_data["cid"]].update(dmx=self.sacn_data["dmx_data"])

    def update_output_data(self):
        """
        Updates the DMX and Per-Channel-Priority values that are used for the next merging run through and for sending
        the next Art-Net packet.
        :return: None
        """
        self.sacn_data["dmx_data"] = self.output_dmx_data
        self.sacn_data["per_channel_priority"] = self.output_priority

    def remove_timeout_universes(self):
        """
        If a universe has a timeout, remove it from the dictionary, so it won't overwrite the priority of the other
        active universes.
        :return: None
        """
        if time() - self.merge_dict[self.universe][self.cids]["time"] > E131_NETWORK_DATA_LOSS_TIMEOUT:
            timeout_time = time() - self.merge_dict[self.sacn_data["universe"]][self.cids]["time"]
            print(f"Deleting universe {self.sacn_data['universe']} from {self.sacn_data['cid']}. "
                  f"Timeout after {timeout_time} seconds.")
            del self.merge_dict[self.universe][self.cids]  # Delete the Universe on this CID and leave the loop.

    def per_channel_priority_merging(self):
        """
        If per-channel-priority is activated, merging will respect these per-channel values.
        :return: None
        """
        universe = self.sacn_data["universe"]
        if self.output_priority[self.dmx_position] < self.merge_dict[universe][self.cids]["priority"][
            self.dmx_position]:
            # If priority is higher, overwrite output.
            self.output_priority[self.dmx_position] = self.merge_dict[universe][self.cids]["priority"][
                self.dmx_position]
            if "dmx" not in self.merge_dict[universe][self.cids]:
                pass
                # Do not do anything if a priority packet is received first, as we don't have any
                # dmx data yet to apply the priority to.
            else:
                # Update DMX if priority is higher.
                self.output_dmx_data[self.dmx_position] = self.merge_dict[universe][self.cids]["dmx"][self.dmx_position]
        elif self.output_priority[self.dmx_position] == self.merge_dict[universe][self.cids]["priority"][self.dmx_position]:
            # If priority is equal, check DMX value
            if "dmx" not in self.merge_dict[universe][self.cids]:
                pass
                # Do not do anything if a priority packet is received first, as we don't have any
                # dmx data yet to apply the priority to.
            elif self.output_dmx_data[self.dmx_position] < self.merge_dict[universe][self.cids]["dmx"][self.dmx_position]:
                # If priority is equal, the highest value wins.
                self.output_dmx_data[self.dmx_position] = self.merge_dict[universe][self.cids]["dmx"][self.dmx_position]
        else:
            pass

    def traditional_merging(self):
        """
        If per-channel-priority is activated, merging will ignore per-channel values.
        :return: None
        """
        universe = self.sacn_data["universe"]
        # If per channel priority is turned off, we always take the highest value.
        if "dmx" not in self.merge_dict[universe][self.cids]:
            pass
            # Do not do anything if a priority packet is received first, as we don't have any
            # dmx data yet to apply the priority to.
        elif self.output_dmx_data[self.dmx_position] < self.merge_dict[universe][self.cids]["dmx"][self.dmx_position]:
            # If priority is equal, the highest value wins.
            self.output_dmx_data[self.dmx_position] = self.merge_dict[universe][self.cids]["dmx"][self.dmx_position]
        else:
            # If output_priority is equal or lower, leave the value as it is.
            pass

    def identify_packet(self):
        """
        Identifies the universe type of the sACN packet. Raises an exception if the packet is too short.
        :return: None
        """
        try:
            len(self.sacn_packet) < 126
        except ValueError as error:
            print("Packet too short:", error)
        if tuple(self.sacn_packet[40:44]) == VECTOR_E131_DATA_PACKET:
            self.validate_dmx_packet()
            self.identify_startcode()
        elif tuple(self.sacn_packet[40:44]) == VECTOR_E131_EXTENDED_SYNCHRONIZATION:
            pass
        elif tuple(self.sacn_packet[40:44]) == VECTOR_E131_EXTENDED_DISCOVERY:
            pass

    def identify_startcode(self):
        """
        At the moment, only the default and the per-channel-priority start code are used.
        :return: None
        """
        start_code = self.sacn_packet[125]
        if start_code == DEFAULT_NULL_START_CODE:
            self.sacn_dmx_input()
        elif start_code == E120_RDM_START_CODE:
            pass
        elif start_code == ELECTRONIC_THEATRE_CONTROLS_START_CODE:
            pass
        else:
            print(f"Start Code {start_code} not supported.")

    def validate_dmx_packet(self):
        """
        E131 Data Packet:
        # # ROOT LAYER # # #
        0-1:      Preamble Size (0x0010)                                        <- Discard if not valid
        2-3:      Postable Size (0x0000)                                        <- Discard if not valid
        4-15:     ACN Packet Identifier
                  (0x41 0x53 0x43 0x2d 0x45 0x31 0x2e 0x31 0x37 0x00 0x00 0x00) <- Discard if not valid
        16-17:    Flags and length (Low 12 bits = PDU length, High 4 bits = 0x7)
        18-21:    Identifies RLP Data as 1.31 Protocol
                  (VECTOR_ROOT_E131_DATA or VECTOR_ROOT_E131_EXTENDED)          <- Discard if not valid
        22-37:    Senders unique CID
        # # DATA PACKET FRAMING LAYER # # #
        38-39     Flags and lenght (Low 12 bits = PDU length, High 4 bits = 0x7
        40-43     Identifies 1.31 data as DMP Protocol PDU (VECTOR_E131_DATA_PACKET)
        44-107:   Source Name assigned by User (UTF-8 encoded string)
        108:      Package Priority of multiple sources (0-200, 100 being default)
        109-110:  Synchronization Address (Universe on which sync packets will be sent)
        111:      Sequence Number (To detect duplicate or out of order packets)
        112:      Options (Bit 5 = Force_Synchronization, Bit 6 = Stream_Terminated, Bit 7 = Preview Data)
        113-114:  Universe Number
        # # DMP Layer # # #
        115-116:  Flags and length (Low 12 bits = PDU Length, High 4 bits = 0x7)
        117:      Identifies DMP Set Property Message PDU (VECTOR_DMP_SET_PROPERTY) <- Discard if not valid
        118:      Address Type and Data Type (0xa1)                                 <- Discard if not valid
        119-120:  First property address, Indicates DMX Start Code is at DMP address 0 (0x0000)<- Discard if not valid
        121-122:  Address Increment, Indicate each property is 1 octet (0x0001)     <- Discard if not valid
        123-124:  Property value count, Indicates +1 the number of slots in packet (0x0001 -- 0x0201)
        125-637:  Property values, DMX Start Code and data (Start Code + data)                        <- DMX DATA
        :return: None
        """

        # The following IF-Statements discard the package if it does not comply with E1.31 standards
        if tuple(self.sacn_packet[0:2]) != PREAMBLE_SIZE or tuple(self.sacn_packet[2:4]) != POST_AMBLE_SIZE or \
                tuple(self.sacn_packet[4:16]) != ACN_PACKET_IDENTIFIER or \
                tuple(self.sacn_packet[18:22]) != VECTOR_ROOT_E131_DATA or \
                tuple(self.sacn_packet[40:44]) != VECTOR_E131_DATA_PACKET or \
                self.sacn_packet[117] != VECTOR_DMP_SET_PROPERTY or \
                self.sacn_packet[118] != ADDRESS_TYPE_DATA_TYPE or \
                tuple(self.sacn_packet[119:121]) != FIRST_PROPERTY_ADDRESS or \
                tuple(self.sacn_packet[121:123]) != ADDRESS_INCREMENT:
            # Raise an error, if any of the package content is not valid. Print out what it should be and what was sent.
            raise TypeError(f"Package does not comply to E1.31 standard and will be ignored! \
            Preamble {PREAMBLE_SIZE} was {tuple(self.sacn_packet[0:2])}, \
            Postamble {POST_AMBLE_SIZE} was {tuple(self.sacn_packet[2:4])}, \
            ACN Packet Identifier {ACN_PACKET_IDENTIFIER} was {tuple(self.sacn_packet[4:16])}, \
            VECTOR E1.31 {VECTOR_ROOT_E131_DATA} was {tuple(self.sacn_packet[18:22])}, \
            VECTOR E1.31 Data {VECTOR_ROOT_E131_DATA} was {tuple(self.sacn_packet[40:44])}, \
            VECTOR DMP {VECTOR_DMP_SET_PROPERTY} was {(self.sacn_packet[117])}, \
            Address Type {ADDRESS_TYPE_DATA_TYPE} was {self.sacn_packet[118]}, \
            First Property Address {FIRST_PROPERTY_ADDRESS} was {tuple(self.sacn_packet[119:121])}, \
            Address Increment {ADDRESS_INCREMENT} was {tuple(self.sacn_packet[121:123])}")

    def sacn_dmx_input(self):
        """
        Called if this is a normal DMX packet (Start Code = 0x00).
        Creates a dictionary with all the information we can get from this package
        :return: None
        """
        if self.sacn_to_artnet is True:
            self.sacn_data = {"cid": self.sacn_packet[22:38], "source_name": str(self.sacn_packet[44:108]),
                              "priority": self.sacn_packet[108], "sync_address": tuple(self.sacn_packet[109:111]),
                              "sequence_number": self.sacn_packet[111], "option_flags": self.sacn_packet[112],
                              "universe": calculate_decimal(tuple(self.sacn_packet[113:115])),
                              "start_code": self.sacn_packet[125], "dmx_data": self.sacn_packet[126:638],
                              "universe_hibyte": self.sacn_packet[113], "universe_lobyte": self.sacn_packet[114]}
            self.merge_sacn_inputs()
            self.artnet_output.artdmx_output(self.sacn_data)
        else:
            # Do nothing if converting is turned off
            pass

    def sacn_per_channel_input(self):
        """
        Called if this is a per channel priority packet (Start Code = 0xDD)
        Creates a dictionary with all the information we can get from this package
        :return: None
        """
        self.sacn_data = {"cid": self.sacn_packet[22:38], "source_name": str(self.sacn_packet[44:108]),
                          "sync_address": tuple(self.sacn_packet[109:111]), "sequence_number": self.sacn_packet[111],
                          "option_flags": self.sacn_packet[112], "universe": tuple(self.sacn_packet[113:115]),
                          "start_code": self.sacn_packet[125], "per_channel_priority": self.sacn_packet[126:638],
                          "universe_hibyte": self.sacn_packet[113], "universe_lobyte": self.sacn_packet[114]}
