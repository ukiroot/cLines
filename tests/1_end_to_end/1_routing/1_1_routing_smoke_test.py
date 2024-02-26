import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import lib.clines as clines


euts=clines.get_euts(1)
linuxchans=clines.get_linuxchans(1)
bridges=clines.get_bridges(1)
topology="eth0:br0,eth1:br0,eth2:br0,eth3:br0|eth0:br0"


@pytest.fixture(autouse=True)
def init():
    clines.release_all_resource()
    clines.init_topology(euts, linuxchans, bridges, topology)
    yield
    clines.destroy_topology(euts, linuxchans)


@pytest.mark.end_to_end_routing_smoke
def test_routing_smoke():
    True
