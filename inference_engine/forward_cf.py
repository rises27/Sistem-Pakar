import json
from pathlib import Path

def load_rules(filename="C:\\Users\\risda\\OneDrive\\Documents\\Tugas Kuliah\\Sistem Pakar\\rules.json"):
    """Load rules.json (default: parent folder rules.json)."""
    if filename is None:
        filename = Path(__file__).resolve().parents[1] / "rules.json"
    with open(filename, "r") as f:
        return json.load(f)

def CFtotal (user_CF, expert_CF):
    return round(user_CF * expert_CF, 2)
def forward_infer(selected_facts, user_cf_map, rules):
    """
    selected_facts: list of fact codes selected by user, e.g. ["A1","B2",...]
    fact_cf_map: map fact_code -> CF (0..1). If a fact is selected but not in map, default = 1.0
    rules: list of rule dicts from rules.json
    Returns: list of conclusions sorted by combined CF descending
      each item: { conclusion, combined_cf, sources:[ {rule_id, matched_facts, fact_cfs, parallel_cf, sequential_cf, rule_cf} ... ] }
    """
    matches = []
    for rule in rules:
        # check if all antecedents are present
        if all(cond in selected_facts for cond in rule["if"]):
            # collect per-fact CFs (default 1.0 if not provided)
            user_cfs = [user_cf_map.get(cond, 1.0) for cond in rule["if"]]

            matches.append({
                "rule_id": rule.get("id"),
                "conclusion": rule.get("then"),
                "rule_cf": rule.get("cf", 1.0),
                "matched_facts": rule["if"],
                "user_cfs": user_cfs,
                "total_cf": CFtotal(user_cfs[0], rule.get("cf", 1.0))
            })

    # Combine results that have the same conclusion (CF combination rule)
    # CF_combined = CF1 + CF2 * (1 - CF1)
    combined = {}
    for m in matches:
        key = m["conclusion"]
        if key not in combined:
            combined[key] = {"combined_cf": m["total_cf"], "sources": [m]}
        else:
            prev = combined[key]["combined_cf"]
            new = round(prev + m["total_cf"] * (1 - prev), 4)
            combined[key]["combined_cf"] = new
            combined[key]["sources"].append(m)

    final = []
    for k, v in combined.items():
        final.append({
            "conclusion": k,
            "combined_cf": v["combined_cf"],
            "sources": v["sources"]
        })
    final.sort(key=lambda x: x["combined_cf"], reverse=True)
    return final

if __name__ == "__main__":
    # quick example using the paper's example:
    rules = load_rules()
    selected = ["G01","G17","G25","G35"]  # example from paper
    fact_cf = {
        "G01":1,"G17":1,"G25":1,"G35":1
    }
    out = forward_infer(selected, fact_cf, rules)
    import pprint
    pprint.pprint(out)
