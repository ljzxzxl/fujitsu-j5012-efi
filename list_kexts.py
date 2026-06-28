import plistlib
import sys

try:
    with open('OC/config.plist', 'rb') as f:
        p = plistlib.load(f)
    for i, k in enumerate(p['Kernel']['Add']):
        print(f"{i}: {k['BundlePath']}")
except Exception as e:
    print(e)
