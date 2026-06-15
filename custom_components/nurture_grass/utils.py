### Clean Site Name ###

def clean_site_name(site_name: str) -> str:
    """Return a friendly site name."""

    parts = [
        part.strip()
        for part in site_name.split(",")
        if part.strip()
        and part.strip().upper() != "NULL"
        and not part.strip().startswith("(")
    ]

    return ", ".join(parts[:3])
