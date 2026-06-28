import plistlib

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
                            pass # We don't care about list item deep diff here if length matches, keep it simple
            elif d1[k] != d2[k]:
                diffs.append(f"VALUE DIFF at {path}[{k}]: mature={d1[k]}, new={d2[k]}")
    
    for k in d2:
        if k not in d1:
            diffs.append(f"EXTRA in New: {path}[{k}]")
    return diffs

mature_plist = plistlib.load(open(r"D:\www\fujitsu-celsius-j5012-efi\EFI_13\OC\config.plist", 'rb'))
new_plist = plistlib.load(open(r"D:\www\EFI\OC\config.plist", 'rb'))

diffs = compare_dicts(mature_plist, new_plist)
for d in diffs:
    print(d)
