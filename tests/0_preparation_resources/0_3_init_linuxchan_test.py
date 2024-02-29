import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines
import configs.env


@pytest.mark.preparation_resources
@pytest.mark.parametrize(
    'linuxchan_config',
    [
        configs.env.LINUXCHAN_1,
        configs.env.LINUXCHAN_2,
        configs.env.LINUXCHAN_3,
        configs.env.LINUXCHAN_4,
        configs.env.LINUXCHAN_5,
        configs.env.LINUXCHAN_6,
        configs.env.LINUXCHAN_7,
        configs.env.LINUXCHAN_8
    ]
)
def test_init_linuxchan(linuxchan_config):
    lin_name = linuxchan_config.get('name')
    lin_console = configs.env.CONSOLE_TEMPLATE.format(configs.env.ENVIRONMENT_IP, linuxchan_config.get("console_port"))
    try:
        clines.start_vm(lin_name)
        linuxchan_1_spawn = clines.attach_to_cli(lin_console)
        clines.linuxchan_grub(lin_name, linuxchan_1_spawn)
        clines.linuxchan_get_shell(lin_name, linuxchan_1_spawn)
    finally:
        clines.destroy_vm(lin_name)
