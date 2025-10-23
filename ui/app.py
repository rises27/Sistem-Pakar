from flask import Flask, render_template, request, jsonify
from pathlib import Path
from inference_engine.forward_cf import load_rules, forward_infer

app = Flask(__name__, template_folder="templates", static_folder="static")
BASE = Path(__file__).resolve().parents[1]

# Gejala mapping (kode -> deskripsi) dari tabel di jurnal
GEJALA = {
"A1":"Leaves or edges of the leaves are brownish-gray",
"A2":"Leaves have brown spots shaped like a rhombus",
"A3":"Leaves have narrow, elongated brown spots",
"A5":"White patches on the leaves in the form of lines or tubes / leaf rolls",
"A6":"The stem dries and at the base of the stem looks brown",
"A7":"Shoots of rice stem dry and easily removed",
"A8":"Inside the plant stem, there are larvae/caterpillars",
"A9":"Rice stalks collapse, rats sighted",
"A10":"Black spots in rice grains",
"B1":"Yellow leaves then dry",
"B2":"The shoots or edges of the leaves are brownish-gray and then spread",
"B4":"Rice panicles are rotten or broken in the generative phase",
"B5":"The stems and midribs of the leaves are rotten so the plants fall",
"B7":"Few panicles and hollow rice grains",
"B8":"Rice grains are not fully filled or empty",
"B9":"The stem of the plant is yellow or brownish-red and there is a black bed",
"B10":"The remaining rice seeds fall / birds in the fields / taste or color changes",
"B11":"There is a plant wilting and dying at the beginning of the growth",
"B12":"Yellow-orange plant leaves",
"B13":"Dwarf plant growth",
"B14":"Plant growth is inhibited",
"B15":"Young plants die and dry out",
"B16":"Young plants die and dry out (alternate symptom)",
"B17":"Excess use of N fertilizer",
"B18":"Other pest symptom",
"B19":"Footprints found around the rice fields",
"B20":"Rat holes around the rice fields",
"B21":"Other damage factors"
}

PENYAKIT = {
"P01":"Bacterial leaf blight",
"P02":"BLAS disease",
"P03":"Narrow brown leaf spot",
"P04":"Green leafhopper & Tungro",
"P05":"Brown planthopper",
"P06":"Rice stem borer",
"P07":"Black rice bug",
"P08":"Rice field rat",
"P09":"Stinky rice bug"
}

RULES_PATH = BASE / ".." / "C:\\Users\\F4QIH\\OneDrive\\Documents\\Perkuliahan\\Tugas Kuliah\\Semester 5\\Sistem Pakar\\Sistem pakar berbasis rule-based, forward chaining, dan CF\\rules.json"
RULES_PATH = RULES_PATH.resolve()

def load_rules_wrapper():
    return load_rules(RULES_PATH)

@app.route("/")
def index():
    return render_template("index.html", gejala=GEJALA)

@app.route("/diagnose", methods=["POST"])
def diagnose():
    data = request.json
    selected = data.get("gejala", [])
    fact_cfs = data.get("fact_cfs", {})  # optional: client may send per-fact CFs
    rules = load_rules_wrapper()
    results = forward_infer(selected, fact_cfs, rules)
    # attach readable label
    for r in results:
        r["label"] = PENYAKIT.get(r["conclusion"], r["conclusion"])
    return jsonify({"results":results})

if __name__ == "__main__":
    app.run(debug=True)

