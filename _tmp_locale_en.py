# Insert health keys into en.yaml after business_card: section
with open("locales/en.yaml", "r") as f:
    lines = f.readlines()

# Find line with top-level "business_card:" (L915)
insert_idx = None
for i, line in enumerate(lines):
    if line.strip() == "business_card:" and not line.startswith(' ') and not line.startswith('\t'):
        # Find next top-level key (not indented)
        for j in range(i+1, len(lines)):
            if lines[j] and not lines[j].startswith(' ') and not lines[j].startswith('\t'):
                insert_idx = j
                break
        break

if insert_idx is None:
    insert_idx = len(lines)

health_keys = """  health:
    section_title: Company Health
    source_estimated: 📊 System Estimate
    confidence_note: Confidence indicator reflects data completeness, not AI prediction certainty
    risk_analysis_title: ⚠️ Risk Analysis — What Could Go Wrong?

"""

lines.insert(insert_idx, health_keys)

with open("locales/en.yaml", "w") as f:
    f.writelines(lines)

print(f"Inserted health keys at line {insert_idx}")

# Now add unit.point to en.yaml
with open("locales/en.yaml", "r") as f:
    content = f.read()

if "point:" not in content.split("unit:")[1].split("\n")[0] if "unit:" in content else True:
    # Check if point already exists under unit:
    with open("locales/en.yaml", "r") as f:
        lines = f.readlines()
    
    added_point = False
    for i, line in enumerate(lines):
        if line.strip() == "unit:":
            # Insert point as first child
            lines.insert(i+1, "  point: pts\n")
            added_point = True
            break
    
    if added_point:
        with open("locales/en.yaml", "w") as f:
            f.writelines(lines)
        print("Added unit.point to en.yaml")
    else:
        print("WARNING: unit: section not found in en.yaml")
else:
    print("unit.point already exists in en.yaml")
