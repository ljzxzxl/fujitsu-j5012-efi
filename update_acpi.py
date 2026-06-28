import plistlib

plist_path = r"D:\www\EFI\OC\config.plist"

with open(plist_path, 'rb') as f:
    plist = plistlib.load(f)

acpi_add = plist['ACPI']['Add']

# Remove SSDT-RTCAWAC.aml
acpi_add = [item for item in acpi_add if item['Path'] != 'SSDT-RTCAWAC.aml']

# Check if SSDT-AWAC.aml already exists
if not any(item['Path'] == 'SSDT-AWAC.aml' for item in acpi_add):
    acpi_add.append({
        'Comment': 'AWAC',
        'Enabled': True,
        'Path': 'SSDT-AWAC.aml'
    })

# Check if SSDT-HPET.aml already exists
if not any(item['Path'] == 'SSDT-HPET.aml' for item in acpi_add):
    acpi_add.append({
        'Comment': 'HPET',
        'Enabled': True,
        'Path': 'SSDT-HPET.aml'
    })

plist['ACPI']['Add'] = acpi_add

with open(plist_path, 'wb') as f:
    plistlib.dump(plist, f)

print("ACPI updated.")
