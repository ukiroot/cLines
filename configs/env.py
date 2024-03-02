ENVIRONMENT_IP='192.168.1.78'
ENVIRONMENT_LOGIN='infra'
ENVIRONMENT_PASSOWORD='infra'
CONSOLE_TEMPLATE="telnet {} {}"
# Resources description
# EUT - equipment under test
EUT_1={"name": "EUT_1", "console_port": "7001"}
EUT_2={"name": "EUT_2", "console_port": "7002"}
EUT_3={"name": "EUT_3", "console_port": "7003"}
EUT_4={"name": "EUT_4", "console_port": "7004"}
EUT_5={"name": "EUT_5", "console_port": "7005"}
EUT_6={"name": "EUT_6", "console_port": "7006"}
EUT_7={"name": "EUT_7", "console_port": "7007"}
EUT_8={"name": "EUT_8", "console_port": "7008"}
# MIGHTY_BRIDGE - linux bridge interface
MIGHTY_BRIDGE_1={'name': 'mighty_bridge_1'}
MIGHTY_BRIDGE_2={'name': 'mighty_bridge_2'}
MIGHTY_BRIDGE_3={'name': 'mighty_bridge_3'}
MIGHTY_BRIDGE_4={'name': 'mighty_bridge_4'}
# LINUXCHAN - linux VM for generate test traffic
LINUXCHAN_1={'name': 'ursamajor', "console_port": "7701"}
LINUXCHAN_2={'name': 'ursaminor', "console_port": "7702"}
LINUXCHAN_3={'name': 'lupus',     "console_port": "7703"}
LINUXCHAN_4={'name': 'virgo',     "console_port": "7704"}
LINUXCHAN_5={'name': 'vulpecula', "console_port": "7705"}
LINUXCHAN_6={'name': 'aquarius',  "console_port": "7706"}
LINUXCHAN_7={'name': 'aries',     "console_port": "7707"}
LINUXCHAN_8={'name': 'pisces',    "console_port": "7708"}
ursamajor=LINUXCHAN_1
ursaminor=LINUXCHAN_2
lupus=LINUXCHAN_3
virgo=LINUXCHAN_4
vulpecula=LINUXCHAN_5
aquarius=LINUXCHAN_6
aries=LINUXCHAN_7
pisces=LINUXCHAN_8