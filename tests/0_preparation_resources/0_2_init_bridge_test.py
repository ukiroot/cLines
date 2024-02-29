import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines
import configs.env

@pytest.mark.preparation_resources
@pytest.mark.init_db
@pytest.mark.parametrize(
    'bridge_config',
    [
        configs.env.MIGHTY_BRIDGE_1,
        configs.env.MIGHTY_BRIDGE_2,
        configs.env.MIGHTY_BRIDGE_3,
        configs.env.MIGHTY_BRIDGE_4
    ]
)
def test_init_bridge(bridge_config):
    clines.init_bridge_interface(bridge_config['name'])
