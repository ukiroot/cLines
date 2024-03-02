import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines
import configs.env


def install_vyos_from_iso_to_disk(eut):
    eut_name = eut.get('name')
    eut_console = configs.env.CONSOLE_TEMPLATE.format(configs.env.ENVIRONMENT_IP, eut.get("console_port"))

    clines.destroy_vm(eut_name)
    clines.start_vm(eut_name)
    eut_spawn = clines.attach_to_cli(eut_console)
    print('Step 0. Login to EUT')
    clines.eut_get_operator(
        clines.eut_login,
        clines.eut_password,
        clines.eut_hostname,
        eut_spawn
    )
    print('Step 1. Run operator command "install image"')
    clines.eut_operator_send_raw_command(
        'install image',
        'This command will install VyOS to your permanent storage.\\r\\nWould you like to continue\? \[y/N\]',
        eut_spawn
    )
    print('Step 2. Would you like to continue? [y/N]')
    clines.eut_operator_send_raw_command(
        'Yes',
        '\(Default: [0-9]{1}\.[0-9]{1}-rolling-[0-9]{12}\) ',
        eut_spawn
    )
    print('Step 3. What would you like to name this image? (Default: 1.5-rolling-202402240021)')
    clines.eut_operator_send_raw_command(
        '',
        'Please enter a password for the "vyos" user \(Default: vyos\)',
        eut_spawn
    )
    print('Step 4. Please enter a password for the "vyos" user \(Default: vyos\)')
    clines.eut_operator_send_raw_command(
        '',
        'What console should be used by default\? \(K: KVM, S: Serial, U: USB-Serial\)\? \(Default: K\)',
        eut_spawn
    )
    print('Step 5. What console should be used by default? (K: KVM, S: Serial, U: USB-Serial)? (Default: K)')
    clines.eut_operator_send_raw_command(
        'S',
        'Which one should be used for installation\? \(Default: /dev/sda\)',
        eut_spawn
    )
    print('Step 6. Which one should be used for installation? (Default: /dev/sda)')
    clines.eut_operator_send_raw_command(
        '',
        'Installation will delete all data on the drive. Continue\? \[y/N\]',
        eut_spawn
    )
    print('Step 7. Installation will delete all data on the drive. Continue? [y/N]')
    clines.eut_operator_send_raw_command(
        'Y',
        'Would you like to use all the free space on the drive\? \[Y/n\]',
        eut_spawn
    )
    print('Step 8. Would you like to use all the free space on the drive? [Y/n]')
    clines.eut_operator_send_raw_command(
        'Y',
        clines.eut_login,
        eut_spawn,
        timeout=50
    )
    clines.destroy_vm(eut_name)


@pytest.mark.preparation_resources
@pytest.mark.parametrize(
    'eut_config',
    [
        configs.env.EUT_1,
        configs.env.EUT_2,
        configs.env.EUT_3,
        configs.env.EUT_4
    ]
)
def test_install_eut(eut_config):
    install_vyos_from_iso_to_disk(eut_config)
