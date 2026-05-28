from compliance_security_dashboard.compliance.control_mapper import (
    apply_compliance_mapping,
    identify_unmapped_findings,
    load_category_mappings,
    load_controls_reference,
    map_control,
)


def test_map_control_returns_known_control():
    assert map_control("identity") == "CTRL-IAM-001"


def test_load_category_and_control_mappings():
    controls = load_controls_reference()
    mappings = load_category_mappings()

    assert "control_id" in controls.columns
    assert "cis_control" in mappings.columns
    assert len(mappings) >= 3


def test_apply_mapping_by_category():
    finding = {
        "finding_id": "TEST-001",
        "category": "identity",
        "control_mapping": "",
        "cis_control": "",
        "nist_category": "",
        "iso_domain": "",
    }

    mapped = apply_compliance_mapping(
        finding,
        controls=load_controls_reference(),
        category_mappings=load_category_mappings(),
    )

    assert mapped["control_mapping"] == "CTRL-IAM-001"
    assert mapped["cis_control"] == "CIS 6"
    assert mapped["nist_category"] == "PR.AC"
    assert mapped["iso_domain"] == "Access Control"
    assert mapped["is_mapped"]


def test_apply_mapping_preserves_explicit_values():
    finding = {
        "finding_id": "TEST-001",
        "category": "identity",
        "control_mapping": "CUSTOM-CTRL",
        "cis_control": "CIS Explicit",
        "nist_category": "",
        "iso_domain": "",
    }

    mapped = apply_compliance_mapping(
        finding,
        controls=load_controls_reference(),
        category_mappings=load_category_mappings(),
    )

    assert mapped["control_mapping"] == "CUSTOM-CTRL"
    assert mapped["cis_control"] == "CIS Explicit"
    assert mapped["nist_category"] == "PR.AC"


def test_identify_unmapped_findings():
    unmapped = identify_unmapped_findings(
        [
            {
                "finding_id": "TEST-001",
                "cis_control": "",
                "nist_category": "",
                "iso_domain": "",
            },
            {
                "finding_id": "TEST-002",
                "cis_control": "CIS 6",
                "nist_category": "",
                "iso_domain": "",
            },
        ]
    )

    assert [finding["finding_id"] for finding in unmapped] == ["TEST-001"]
