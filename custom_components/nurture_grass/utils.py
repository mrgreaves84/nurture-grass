### Clean Site Name ###

def clean_site_name(site_name: str) -> str:
    """Return a friendly site name."""

    return site_name.split(",")[0].strip()
