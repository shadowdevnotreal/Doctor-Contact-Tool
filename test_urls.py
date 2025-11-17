#!/usr/bin/env python3
"""Test all medical board URLs to verify they're working"""

import urllib.request
import urllib.error
import ssl
from DoctorDork import DoctorDork

# Create SSL context that doesn't verify certificates (some sites have issues)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def test_url(state, name, url):
    """Test if a URL is accessible"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10, context=ctx)
        status = response.getcode()
        if status == 200:
            print(f"✓ {state} - {name}: OK")
            return True
        else:
            print(f"✗ {state} - {name}: Status {status}")
            return False
    except urllib.error.HTTPError as e:
        print(f"✗ {state} - {name}: HTTP {e.code} - {url}")
        return False
    except urllib.error.URLError as e:
        print(f"✗ {state} - {name}: URL Error - {e.reason}")
        return False
    except Exception as e:
        print(f"✗ {state} - {name}: {type(e).__name__} - {str(e)}")
        return False

def main():
    app = DoctorDork()
    boards = app.MEDICAL_BOARDS

    print(f"Testing {len(boards)} medical board URLs...\n")

    working = []
    broken = []

    for state, info in sorted(boards.items()):
        name = info['name']
        url = info['url']
        if test_url(state, name, url):
            working.append(state)
        else:
            broken.append((state, name, url))

    print(f"\n{'='*70}")
    print(f"Results: {len(working)} working, {len(broken)} broken")
    print(f"{'='*70}")

    if broken:
        print("\nBroken URLs that need fixing:")
        for state, name, url in broken:
            print(f"  {state} ({name}): {url}")

if __name__ == "__main__":
    main()
