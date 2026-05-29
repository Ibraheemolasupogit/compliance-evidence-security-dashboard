# Controls Catalog

The offline controls catalog lives in `data/reference/controls_reference.csv`. It provides control identifiers, names, framework labels, control families, CIS/NIST/ISO-style mapping fields, and evidence expectations used by the compliance mapping layer.

The category mapping file, `data/reference/category_mapping.csv`, links finding categories to default controls and reporting domains. The current implementation preserves explicit finding mappings and fills missing mapping fields from these references.

Future enhancements can add control owners, testing frequency, evidence freshness expectations, and audit procedures.
