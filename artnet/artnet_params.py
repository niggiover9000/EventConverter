"""PORT ADDRESS FOR DMX512 UNIVERSES"""
#   Bit 15  Bits 14-8   Bits 7-4    Bits 3-0
#   0       Net         Sub Net     Universe

'''LOCAL VARS'''
VERSION = 1

'''TIMEOUTS'''
ART_POLL_TIMEOUT = 3  # If the Controller doesn't receive response in time it should consider Node to be disconnected
MERGE_TIMEOUT = 10  # If, during the 10 second timeout, the failed source returns, Merge mode continues.

'''SOCKET PARAMETER'''
UDP_PORT = 6454
LIMITED_BROADCAST_ADDRESS = "255.255.255.255"
PRIMARY_ARTNET_ADDRESS = "2.255.255.255"
SECONDARY_ARTNET_ADDRESS = "10.255.255.255"

'''Art-Net Parameter'''
OEM_CODE = 0x0000
ID = (0x41, 0x72, 0x74, 0x2d, 0x4e, 0x65, 0x74, 0x00)  # = "A" "r" "t" "-" "N" "e" "t" 0x00
PROT_VER_HI = 0x0
PROT_VER_LO = 14
SPARE = 0x0

'''OP CODES'''
OP_POLL = (0x20, 0x00)            # This is an ArtPoll packet, no other data is contained in this UDP packet
OP_POLL_REPLY = (0x21, 0x00)      # This is an ArtPollReply Packet. It contains device status information.
OP_DIAG_DATA = (0x23, 0x00)       # Diagnostics and data logging packet.
OP_COMMAND = (0x24, 0x00)         # Used to send text based parameter commands.
OP_OUTPUT = (0x50, 0x00)
OP_DMX = (0x50, 0x00)             # This is an ArtDmx data packet.
# It contains zero start code DMX512 information for a single Universe.
OP_NZS = (0x51, 0x00)             # This is an ArtNzs data packet.
# It contains non-zero start code (except RDM) DMX512 information for a single Universe.
OP_SYNC = (0x52, 0x00)            # This is an ArtSync data packet.
# It is used to force synchronous transfer of ArtDmx packets to a node’s output.
OP_ADDRESS = (0x60, 0x00)         # This is an ArtAddress packet. It contains remote programming information for a Node.
OP_INPUT = (0x70, 0x00)           # This is an ArtInput packet. It contains enable – disable data for DMX inputs.
OP_TOD_REQUEST = (0x80, 0x00)     # This is an ArtTodRequest packet.
# It is used to request a Table of Devices (ToD) for RDM discovery.
OP_TOD_DATA = (0x81, 0x00)        # This is an ArtTodData packet.
# It is used to send a Table of Devices (ToD) for RDM discovery.
OP_TOD_CONTROL = (0x82, 0x00)     # This is an ArtTodControl packet. It is used to send RDM discovery control messages.
OP_RDM = (0x83, 0x00)             # This is an ArtRdm packet. It is used to send all non discovery RDM messages.
OP_RDM_SUB = (0x84, 0x00)         # This is an ArtRdmSub packet. It is used to send compressed, RDM Sub-Device data.
OP_VIDEO_SETUP = (0xa0, 0x10)     # This is an ArtVideoSetup packet.
# It contains video screen setup information for nodes that implement the extended video features.
OP_VIDEO_PALETTE= (0xa0, 0x20)     # This is an ArtVideoPalette packet.
# It contains colour palette setup information for nodes that implement the extended video features.
OP_VIDEO_DATA = (0xa0, 0x40)      # This is an ArtVideoData packet.
# It contains display data for nodes that implement the extended video features.
OP_MAC_MASTER = (0xf0, 0x00)      # This packet is deprecated.
OP_MAC_SLAVE = (0xf1, 0x00)       # This packet is deprecated.
OP_FIRMWARE_MASTER = (0xf2, 0x00) # This is an ArtFirmwareMaster packet.
# It is used to upload new firmware or firmware extensions to the Node.
OP_FIRMWARE_REPLY = (0xf3, 0x00)  # This is an ArtFirmwareReply packet.
# It is returned by the node to acknowledge receipt of an ArtFirmwareMaster packet or ArtFileTnMaster packet.
OP_FILE_TN_MASTER = (0xf4, 0x00)  # Uploads user file to node.
OP_FILE_FN_MASTER = (0xf5, 0x00)  # Downloads user file from node.
OP_FILE_FN_REPLY = (0xf6, 0x00)   # Server to Node acknowledge for download packets.
OP_IP_PROG = (0xf8, 0x00)         # This is an ArtIpProg packet.
# It is used to reprogramme the IP address and Mask of the Node.
OP_IP_PROG_REPLY = (0xf9, 0x00)   # This is an ArtIpProgReply packet.
# It is returned by the node to acknowledge receipt of an ArtIpProg packet.
OP_MEDIA = (0x90, 0x00)           # This is an ArtMedia packet.
# It is Unicast by a Media Server and acted upon by a Controller.
OP_MEDIA_PATCH = (0x91, 0x00)     # This is an ArtMediaPatch packet.
# It is Unicast by a Controller and acted upon by a Media Server.
OP_MEDIA_CONTROL = (0x92, 0x00)   # This is an ArtMediaControl packet.
# It is Unicast by a Controller and acted upon by a Media Server.
OP_MEDIA_CONTRL_REPLY= (0x93, 0x00)  # This is an ArtMediaControlReply packet.
# It is Unicast by a Media Server and acted upon by a Controller.
OP_TIME_CODE = (0x97, 0x00)       # This is an ArtTimeCode packet. It is used to transport time code over the network.
OP_TIME_SYNC = (0x98, 0x00)       # Used to synchronise real time date and clock
OP_TRIGGER = (0x99, 0x00)         # Used to send trigger macros
OP_DIRECTORY = (0x9a, 0x00)       # Requests a node's file list
OP_DIRECTORY_REPLY = (0x9b, 0x00) # Replies to OpDirectory with file list

'''NodeReport Codes'''
RC_DEBUG = 0x0000           # Booted in debug mode (Only used in development)
RC_POWER_OK = 0x0001        # Power On Tests successful
RC_POWER_FAIL = 0x0002      # Hardware tests failed at Power On
RC_SOCKET_WR1 = 0x0003      # Last UDP from Node failed due to truncated length, most likely caused by a collision.
RC_PARSE_FAIL = 0x0004      # Unable to identify last UDP transmission. Check OpCode and packet length.
RC_UDP_FAIL = 0x0005        # Unable to open Udp Socket in last transmission attempt
RC_SH_NAME_OK = 0x0006      # Confirms that Short Name programming via ArtAddress, was successful.
RC_LO_NAME_OK =0x0007       # Confirms that Long Name programming via ArtAddress, was successful.
RC_DMX_ERROR = 0x0008       # DMX512 receive errors detected.
RC_DMX_UDP_FULL = 0x0009    # Ran out of internal DMX transmit buffers.
RC_DMX_RX_FULL = 0x000a     # Ran out of internal DMX Rx buffers.
RC_SWITCH_ERR = 0x000b      # Rx Universe switches conflict.
RC_CONFIG_ERR = 0x000c      # Product configuration does not match firmware.
RC_DMX_SHORT = 0x000d       # DMX output short detected. See GoodOutput field.
RC_FIRMWARE_FAIL = 0x000e   # Last attempt to upload new firmware failed.
RC_USER_FAIL = 0x000f       # User changed switch settings when address locked by remote programming. Changes ignored.
RC_FACTORY_RES = 0x0010     # Factory reset has occurred.

'''Style Codes'''
ST_NODE = 0x00              # A DMX to / from Art-Net device
ST_CONTROLLER =0x01         # A lighting console.
ST_MEDIA = 0x02             # A Media Server.
ST_ROUTE = 0x03             # A network routing device.
ST_BACKUP = 0x04            # A backup device.
ST_CONFIG = 0x05            # A configuration or diagnostic tool.
ST_VISUAR = 0x06            # A visualiser.

'''Priority Codes'''
DP_LOW = 0x10               # Low priority message
DP_MED = 0x40               # Medium priority message
DP_HIGH = 0x80              # High priority message
DP_CRITICAL = 0xe0          # Critical priority message
DP_VOLATILE = 0xf0          # Volatile message. Messages of this universe_type are displayed on a single line
#                           # in the DMX-workshop diagnostics display. All other types are displayed in a list box.

'''Command Codes'''
SW_OUT_TEXT = "SwoutText=Playback&"     # Re-Programme the label associated with the ArtPollReply->Swout Fields
SW_IN_TEXT = "SwinText=Record&"         # Re-Programme the label associated with the ArtPollReply->Swin Fields
