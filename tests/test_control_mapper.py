from compliance_security_dashboard.compliance.control_mapper import map_control


def test_map_control_returns_known_control():
    assert map_control("identity") == "CTRL-IAM-001"
