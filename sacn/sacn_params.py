"""E131 DEFINED PARAMETERS"""

PREAMBLE_SIZE = (0, 0x10)
POST_AMBLE_SIZE = (0, 0)
ACN_PACKET_IDENTIFIER = (0x41, 0x53, 0x43, 0x2d, 0x45, 0x31, 0x2e, 0x31, 0x37, 0x00, 0x00, 0x00)

VECTOR_ROOT_E131_DATA = (0, 0, 0, 0x4)
VECTOR_ROOT_E131_EXTENDED = (0, 0, 0, 0x8)

VECTOR_DMP_SET_PROPERTY = 0x02
ADDRESS_TYPE_DATA_TYPE = 0xa1
FIRST_PROPERTY_ADDRESS = (0, 0)
ADDRESS_INCREMENT = (0, 0x1)

VECTOR_E131_DATA_PACKET = (0, 0, 0, 0x02)

VECTOR_E131_EXTENDED_SYNCHRONIZATION = (0, 0, 0, 0x1)
VECTOR_E131_EXTENDED_DISCOVERY = (0, 0, 0, 0x2)

VECTOR_UNIVERSE_DISCOVERY_UNIVERSE_LIST = (0, 0, 0, 0x1)

E131_E131_UNIVERSE_DISCOVERY_INTERVAL = 10  # 10 seconds
E131_NETWORK_DATA_LOSS_TIMEOUT = 2.5  # 2.5 seconds
E131_DISCOVERY_UNIVERSE = 64214

ACN_SDT_MULTICAST_PORT = 5568


"""START CODES"""

DEFAULT_NULL_START_CODE = 0x00  # Default Null Start Code for Dimmers per DMX512 & DMX512/1990
T_RECURSIVE_DOUBLE_PRECISION_START_CODE = 0x01
SOUNDLIGHT_START_CODE = 0x01
MODE_LIGHTING = 0x01
T_RECURSIVE_16BIT_WORDS_START_CODE = 0x02
THE_WHITE_RABBIT_COMPANY_START_CODE = 0x03
T_RECURSIVE_CHECKSUM_MESSAGE_START_CODE = 0x04
T_RECURSIVE_ANSWERBACK_QUERY_START_CODE = 0x05
T_RECURSIVE_16BIT_LO_BYTE_START_CODE = 0x06
T_RECURSIVE_COMPRESSED_DATA_START_CODE = 0x07
T_RECURSIVE_COMPRESSED_16BIT_DATA_START_CODE = 0x08
ENTERTAINMENT_TECHNOLOGY_START_CODE = 0x09
MODE_LIGHTING_START_CODE = 0x0A
GODDARD_DESIGN_START_CODE = 0x0B
SGM_ELETTRONICA_START_CODE = 0x0C
ENGINEERING_ARTS_START_CODE = 0x0D
CI_TRONICS_LIGHTING_START_CODE = 0x0E
MORPHEUS_LIGHTS_START_CODE = 0x0F
ADB_START_CODE = 0x10
TOKYO_BROADCAST_SYSTEMS_START_CODE = 0x11
BJA_ELECTRONICS_START_CODE = 0x12
ZERO_88_START_CODE = 0x13
SOUNDSCULPTURE_INCORPORATED_START_CODE = 0x14
CDCA_START_CODE = 0x15
PERADISE_START_CODE = 0x16
ARTISTIC_LICENCE_START_CODE = 0x17  # Text Packet (matches use in ANSI E1.11)
E111_TEXT_PACKET_START_CODE = 0x17
ANDERA_START_CODE = 0x18
HUBBELL_ENTERTAINMENT_START_CODE = 0x19
INTEGRATED_THEATRE_START_CODE = 0x1A
ESPACE_CONCEPT_START_CODE = 0x1B
KLH_ELECTRONICS_PLC_START_CODE = 0x1C
DANGEROSS_DESIGN_START_CODE = 0x1D
ROBERT_JULIAT_START_CODE = 0x1E
ELETTROLAB_START_CODE = 0x21
GLOBAL_DESIGN_SOLUTIONS = 0x22
HIGH_END_SYSTEMS_START_CODE = 0x26
JOHNSON_SYSTEMS_START_CODE = 0x2A
PR_LIGHTING_START_CODE = 0x30
ACME_START_CODE = 0x32
TESI_ELETTRONICA_START_CODE = 0x33
TIR_SYSTEMS_START_CODE = 0x37
AVAB_INTERNAL_FUNCTIONS_START_CODE = 0x3C
AVAB_SMART_16BIT_FORMAT_START_CODE = 0x3D
AVAB_AMERICA_START_CODE = 0x3E
SAND_NETWORK_SYSTEMS_START_CODE = 0x3F
MICROLITE_START_CODE = 0x41
LSC_LIGHTING_SYSTEMS_START_CODE = 0x42
CITY_ELECTRICAL_START_CODE = 0x43
COEMAR_STA_START_CODE = 0x44
GVA_LIGHTING_START_CODE = 0x47
ENFIS_START_CODE = 0x48
PHOENIX_SERVICE_START_CODE = 0x4C
AVOLITES_START_CODE = 0x4D
OSCAR_LIGHTING_START_CODE = 0x4F
LIGHTPROCESSOR_START_CODE = 0x50
TEST_PACKET_START_CODE = 0x55  # Test Packet
WYBRON_START_CODE = 0x57
ANYTRONICS_START_CODE = 0x83
CLAY_PAKY_START_CODE = 0x8A
MARTIN_PROFESSIONAL_START_CODE = 0x8B
UTF8_TEXT_PACKET_START_CODE = 0x90  # PLASA UTF-8 Text Packet
MANUFACTURER_ID_START_CODE = 0x91  # 2-byte Manufacturer ID serves as an identifier that the data following in that
# packet is proprietary to that entity and should be ignored by all others
E145_BSR_START_CODE = 0x92  # PLASA BSR E1.45 Alternate START Code

# 0x92 to 0xA9 Reserved for Future Expansion of the DMX512 Standard
SUN_START_CODE = 0xAA
# 0xAB to 0xCB Reserved for Future Expansion of the DMX512 Standard
MARTIN_PROFESSIONAL_AS_START_CODE = 0xBB
MARTIN_PROFESSIONAL_START_CODE_2 = 0xCB

E120_RDM_START_CODE = 0xCC  # E1.20 (RDM) start code
# 0xCD and 0xCE Reserved for Future Expansion of the DMX512 Standard

E111_SYSTEM_INFORMATION_PACKET_START_CODE = 0xCF  # ANSI E1.11 System Information Packet
EVOLED_START_CODE = 0xD0
ELECTRONIC_THEATRE_CONTROLS_START_CODE = 0xDD  # Alternate start code DD is for use in transmitting per channel priority
# for use in merging streams in multi-source DMX applications. Priorities will range from 0 at the low end, which means
# do not use the data in the corresponding slot, to 200, which means use this data over any slot data supplied with a
# priority between 0 and 199. Values above 200 are reserved for future use.
MARTIN_PROFESSIONAL_START_CODE_3 = 0xDE
DOUG_FLEENOR_DESIGN_START_CODE = 0xDF
MARTIN_PROFESSIONAL_AS_START_CODE_2 = 0xDF
NSI_COLORTRAN_ENR_MODE_CONTROL_START_CODE = 0xE0
MARTIN_PROFESSIONAL_AS_START_CODE_3 = 0xE0
NSI_COLORTRAN_DIM_NONDIM_CONTROL_START_CODE = 0xE1
ECUE_CONTROL_START_CODE = 0xEC
ELECTRONIC_DIVERSIFIED_START_CODE = 0xED
MARTIN_PROFESSIONAL_START_CODE_4 = 0xED
PROTOTYPING_START_CODE_1 = 0xF0
PROTOTYPING_START_CODE_2 = 0xF1
PROTOTYPING_START_CODE_3 = 0xF2
PROTOTYPING_START_CODE_4 = 0xF3
PROTOTYPING_START_CODE_5 = 0xF4
PROTOTYPING_START_CODE_6 = 0xF5
PROTOTYPING_START_CODE_7 = 0xF6
PROTOTYPING_START_CODE_8 = 0xF7
AVO_START_CODE = 0xFF
