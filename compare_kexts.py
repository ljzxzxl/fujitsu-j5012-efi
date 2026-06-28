import plistlib

mature_plist = plistlib.load(open(r"D:\www\fujitsu-celsius-j5012-efi\EFI_13\OC\config.plist", 'rb'))
new_plist = plistlib.load(open(r"D:\www\EFI\OC\config.plist", 'rb'))

def get_kexts(plist):
    return [k for k in plist['Kernel']['Add'] if k.get('Enabled', False)]

m_kexts = get_kexts(mature_plist)
n_kexts = get_kexts(new_plist)

print("Mature Kexts Order:")
for k in m_kexts:
    print(f" - {k['BundlePath']}")

print("\nNew Kexts Order:")
for k in n_kexts:
    print(f" - {k['BundlePath']}")

print("\nMissing in New:")
for k in m_kexts:
    if not any(nk['BundlePath'] == k['BundlePath'] for nk in n_kexts):
        print(f" - {k['BundlePath']}")

print("\nExtra in New:")
for nk in n_kexts:
    if not any(k['BundlePath'] == nk['BundlePath'] for k in m_kexts):
        print(f" - {nk['BundlePath']}")

