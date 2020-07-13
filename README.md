# OVS-groups-chain-view
OVS-like switch group chain printing from dump-group output 

usage: ovs_group_chain.py [-h] [--version] [-v] [-f F] groupID

positional arguments:
groupID     Initial group ID

optional arguments:
-h, --help  show this help message and exit
--version   show program's version number and exit
-v          show program's version number and exit
-f F        read "ovs-ofctl dump-groups <bridge>" command output from file F. STDIN used if omitted.
