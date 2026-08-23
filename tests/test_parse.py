from emergence.sourcing.parse import normalize_domain, slugify, split_title


def test_split_show_hn_with_dash():
    assert split_title("Show HN: Acme – AI bookkeeping for dentists") == (
        "Acme",
        "AI bookkeeping for dentists",
    )


def test_split_launch_hn_with_yc_suffix():
    assert split_title("Launch HN: Foo (YC W26) – AI agents for SMB payroll") == (
        "Foo (YC W26)",
        "AI agents for SMB payroll",
    )


def test_split_hyphen_separator():
    assert split_title("Show HN: Dispatchly - AI dispatch") == (
        "Dispatchly",
        "AI dispatch",
    )


def test_split_no_separator_gives_empty_one_liner():
    assert split_title("Show HN: SoloName") == ("SoloName", "")


def test_split_rejects_non_launch_titles():
    assert split_title("Ask HN: best books?") is None
    assert split_title("AI agents are coming") is None
    assert split_title("") is None


def test_split_rejects_empty_body():
    assert split_title("Show HN:") is None


def test_normalize_domain_strips_www_scheme_path():
    assert normalize_domain("https://www.Acme.io/pricing?x=1") == "acme.io"
    assert normalize_domain("acme.io") == "acme.io"
    assert normalize_domain("http://sub.acme.io") == "sub.acme.io"


def test_slugify():
    assert slugify("Acme Agents!") == "acme-agents"
    assert slugify("acme.io") == "acme-io"
    assert slugify("!!!") == "unknown"
