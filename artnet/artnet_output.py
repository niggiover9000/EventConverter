from settings.load_settings import LoadSettings
from artnet.artnet_params import ID, OP_DMX, PROT_VER_LO, PROT_VER_HI
from artnet.artnet_socket import ArtNetSocket


def calculate_hibyte(byte: int):
    """
    Converts a byte into hibyte and lobyte
    :param byte: byte that should be converted in hibyte and lobyte
    :return: tuple: hibyte[0], lobyte[1]
    """
    hibyte = (byte >> 8)
    lobyte = (byte & 0xFF)
    return hibyte, lobyte


class ArtNetOutput:
    def __init__(self):
        self.artnet_data = None
        self.artnet_packet = None
        self.sacndict = None
        self.broadcast = False
        self.receiver_ips = []
        self.load_artnet_output()
        self.socket = ArtNetSocket()

    def load_artnet_output(self):
        loading = LoadSettings()
        loading.open_settings("sACN", "sacndict", {})
        self.sacndict = loading.load_settings()
        loading.open_settings("Art-Net", "broadcast", False)
        self.broadcast = loading.load_settings()
        loading.open_settings("Art-Net", "receiver_ips", {})
        self.receiver_ips = loading.load_settings()

    def artdmx_output(self, artnet_data, physical=0):
        self.artnet_data = artnet_data
        # 0-39 DEVICES: UNICAST, 40+ DEVICES: BROADCAST
        # 1:        ID[8] ('A''r''t''-''N''e''t' 0x00)
        # 2:        OPCode (OpOutput, see OPCode list) -> Int16!
        # 3:        ProtVerHi (0x0)
        # 4:        ProtVerLo (14)
        # 5:        Sequence (increment in the range 0x01 to 0xff. Set to 0x00 to disable the feature)
        # 6:        Physical (Phyiscal Input Port, information for the user only)
        # 7:        SubUni (Low Byte of the 15 bit Port-Address to which this packet is destined)
        # 8:        Net (Top 7 bits of the 15 bit Port-Address to which this packet is destined)
        # 9:        LengthHi (Length of the DMX512 data array. Should be between 2 and 512)
        # 10:       Lenght (Low Byte of above)
        # 11:       DMX512 data array

        length = calculate_hibyte(512)
        universe_dec = self.artnet_data["universe"]
        for universes in self.sacndict[universe_dec]:
            universe = calculate_hibyte(universes)
            artnet_packet = bytearray()
            artnet_packet.extend(ID)
            artnet_packet.append(OP_DMX[1])  # OPCode Lo
            artnet_packet.append(OP_DMX[0])  # OPCode Hi
            artnet_packet.append(PROT_VER_HI)  # ProtVerHi
            artnet_packet.append(PROT_VER_LO)  # ProtVerLo
            artnet_packet.append(self.artnet_data["sequence_number"])  # Sequence <- ToDo
            artnet_packet.append(physical)  # Physical
            artnet_packet.append(universe[1])  # SubUni
            artnet_packet.append(universe[0])  # Net
            artnet_packet.append(length[0])  # LengthHi
            artnet_packet.append(length[1])  # Length
            artnet_packet.extend(bytearray(self.artnet_data["dmx_data"]))

            self.artnet_packet = artnet_packet
            self.artnet_output()

    def artnet_output(self):
        if len(self.receiver_ips) > 40:  # If there are more than 40 receivers, send broadcast to save network capacity
            print(f"Changed to broadcast sending, since there are {len(self.receiver_ips)} Universes active and it will"
                  f"save network traffic to send broadcast.")
            self.broadcast = True
        # ToDo timeout outside of this function
        if self.broadcast is True:
            try:
                self.socket.artnet_socket.sendto(self.artnet_packet, ("255.255.255.255", self.socket.port))
            except Exception as exception:
                print(f"Socket error: {exception}")
        else:
            for ips in self.receiver_ips:
                try:
                    self.socket.artnet_socket.sendto(self.artnet_packet, (ips, self.socket.port))

                except Exception as exception:
                    print(f"Socket error: {exception}")
