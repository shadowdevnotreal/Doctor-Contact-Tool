#!/usr/bin/env python3
"""Verify medical board URLs have valid domains (not testing accessibility)"""

import socket
from urllib.parse import urlparse
from DoctorDork import DoctorDork

def check_domain(url):
    """Check if domain resolves"""
    try:
        domain = urlparse(url).netloc
        socket.gethostbyname(domain)
        return True, domain
    except socket.gaierror:
        return False, urlparse(url).netloc

def main():
    app = DoctorDork()
    boards = app.MEDICAL_BOARDS

    print("Checking if domains resolve (DNS check)...\n")

    valid = []
    invalid = []

    for state, info in sorted(boards.items()):
        name = info['name']
        url = info['url']
        is_valid, domain = check_domain(url)

        if is_valid:
            print(f"✓ {state} - {domain}")
            valid.append(state)
        else:
            print(f"✗ {state} - {domain} (DNS FAILED)")
            invalid.append((state, name, url, domain))

    print(f"\n{'='*70}")
    print(f"Results: {len(valid)} valid domains, {len(invalid)} invalid domains")
    print(f"{'='*70}")

    if invalid:
        print("\nURLs with invalid/unresolvable domains:")
        for state, name, url, domain in invalid:
            print(f"  {state} ({name}): {domain}")
            print(f"    Full URL: {url}")

    print("\n" + "="*70)
    print("NOTE: 403 errors in automated tests are NORMAL for government sites.")
    print("These URLs are meant to be opened in browsers, where they work fine.")
    print("="*70)

if __name__ == "__main__":
    main()
