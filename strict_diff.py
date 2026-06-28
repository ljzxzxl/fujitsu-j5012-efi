import plistlib

def compare_plists():
    p1 = plistlib.load(open(r"D:\www\fujitsu-celsius-j5012-efi\EFI_13\OC\config.plist", 'rb'))
    p2 = plistlib.load(open(r"D:\www\EFI\OC\config.plist", 'rb'))

    # Normalize some known differences
    p1['PlatformInfo']['Generic']['SystemSerialNumber'] = ""
    p1['PlatformInfo']['Generic']['SystemUUID'] = ""
    p1['PlatformInfo']['Generic']['MLB'] = ""
    p1['PlatformInfo']['Generic']['ROM'] = ""
    p2['PlatformInfo']['Generic']['SystemSerialNumber'] = ""
    p2['PlatformInfo']['Generic']['SystemUUID'] = ""
    p2['PlatformInfo']['Generic']['MLB'] = ""
    p2['PlatformInfo']['Generic']['ROM'] = ""

    def compare_dicts(d1, d2, path=""):
        diffs = []
        for k in d1:
            if k not in d2:
                diffs.append(f"MISSING in New: {path}[{k}]")
            else:
                if isinstance(d1[k], dict):
                    diffs.extend(compare_dicts(d1[k], d2[k], path + f"[{k}]"))
                elif isinstance(d1[k], list):
                    if len(d1[k]) != len(d2[k]):
                        diffs.append(f"LEN DIFF at {path}[{k}]: mature={len(d1[k])}, new={len(d2[k])}")
                    else:
                        for i, (v1, v2) in enumerate(zip(d1[k], d2[k])):
                            if isinstance(v1, dict) and isinstance(v2, dict):
                                diffs.extend(compare_dicts(v1, v2, path + f"[{k}][{i}]"))
                            elif v1 != v2:
                                diffs.append(f"LIST ITEM DIFF at {path}[{k}][{i}]: mature={v1}, new={v2}")
                elif d1[k] != d2[k]:
                    diffs.append(f"VALUE DIFF at {path}[{k}]: mature={d1[k]}, new={d2[k]}")
        
        for k in d2:
            if k not in d1:
                diffs.append(f"EXTRA in New: {path}[{k}]")
        
        return diffs

    diffs = compare_dicts(p1, p2)
    for d in diffs:
        print(d)

compare_plists()
