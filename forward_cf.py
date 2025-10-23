import json

def load_rules(filename="rules.json"):
    import os
    base_path = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(base_path, filename)
    with open(full_path, "r") as f:
        return json.load(f)

def forward_chaining(facts, rules):
    conclusions = []
    for rule in rules:
        if all(cond in facts for cond in rule["if"]):
            conclusions.append((rule["then"], rule["cf"]))
    return conclusions

def combine_cf(cf_values):
    """Kombinasi certainty factor: CF1 + CF2 * (1 - CF1)"""
    if not cf_values:
        return 0
    cf_total = cf_values[0]
    for cf in cf_values[1:]:
        cf_total = cf_total + cf * (1 - cf_total)
    return round(cf_total, 3)

if __name__ == "__main__":
    # contoh input gejala dari user
    user_facts = ["G01", "G02", "G03", "G07", "G08", "G10", "G12", "G13"]

    rules = load_rules()
    conclusions = forward_chaining(user_facts, rules)

    if conclusions:
        penyakit = conclusions[0][0]
        cf_total = combine_cf([c[1] for c in conclusions])
        print(f"Hasil diagnosis: {penyakit}")
        print(f"Tingkat keyakinan (CF): {cf_total * 100}%")
    else:
        print("Tidak ditemukan penyakit yang cocok dengan gejala.")
