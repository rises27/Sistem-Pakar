import json
from pathlib import Path

def load_rules(filename="C:\\Users\\F4QIH\\OneDrive\\Documents\\Perkuliahan\\Tugas Kuliah\\Semester 5\\Sistem Pakar\\Sistem pakar berbasis rule-based, forward chaining, dan CF\\rules.json"):
    """Load rules.json (default: parent folder rules.json)."""
    if filename is None:
        filename = Path(__file__).resolve().parents[1] / "rules.json"
    with open(filename, "r") as f:
        return json.load(f)

def parallel_cf_for_rule(fact_cfs):
    """
    Parallel CF for AND: min(CF(x), CF(y), ...)
    (Paper uses min for AND.)
    """
    if not fact_cfs:
        return 0.0
    return min(fact_cfs)

def sequential_cf(parallel_cf, rule_cf):
    """
    Sequential CF as described in the paper:
    CF_sequence = parallel_cf * rule_cf
    """
    return round(parallel_cf * rule_cf, 4)

def forward_infer(selected_facts, fact_cf_map, rules):
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
            fact_cfs = [fact_cf_map.get(cond, 1.0) for cond in rule["if"]]
            pcf = parallel_cf_for_rule(fact_cfs)
            seq = sequential_cf(pcf, rule.get("cf", 1.0))
            matches.append({
                "rule_id": rule.get("id"),
                "conclusion": rule.get("then"),
                "rule_cf": rule.get("cf", 1.0),
                "matched_facts": rule["if"],
                "fact_cfs": fact_cfs,
                "parallel_cf": pcf,
                "sequential_cf": seq
            })

    # Combine results that have the same conclusion (CF combination rule)
    # CF_combined = CF1 + CF2 * (1 - CF1)
    combined = {}
    for m in matches:
        key = m["conclusion"]
        if key not in combined:
            combined[key] = {"combined_cf": m["sequential_cf"], "sources": [m]}
        else:
            prev = combined[key]["combined_cf"]
            new = round(prev + m["sequential_cf"] * (1 - prev), 4)
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
    selected = ["A1","B2","B8","B11","B17"]  # example from paper
    fact_cf = {
        "A1":0.95,"B2":0.85,"B8":0.75,"B11":0.70,"B17":0.95
    }
    out = forward_infer(selected, fact_cf, rules)
    import pprint
    pprint.pprint(out)

