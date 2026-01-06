"""Fix the duplicate lines error in auth_app.py"""

file_path = r'd:\codewave\auth_app.py'

print("Reading file...")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Fixing duplicate lines...")
fixed_lines = []
skip_until = -1

for i, line in enumerate(lines):
    # Skip lines 579-584 (the duplicate parameters)
    if i >= 579 and i <= 584:
        continue
    fixed_lines.append(line)

print("Writing fixed file...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("\n[OK] Fixed! Lines 580-584 removed.")
print("\nNow restart your server:")
print("  python auth_app.py")
