from flask import Flask, render_template, request, jsonify
from pathlib import Path
import sys

# Menambahkan root direktori ke Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from inference_engine.forward_cf import load_rules, forward_infer

app = Flask(__name__, template_folder="templates", static_folder="static")
BASE = Path(__file__).resolve().parents[1]

# Gejala dikategorikan
gejala_dict = {
    "G01": "Nafsu makan menurun",
    "G02": "Sesak napas / megap-megap",
    "G03": "Napas mendengkur basah",
    "G04": "Bersin",
    "G05": "Batuk",
    "G06": "Bulu kusam dan keriput",
    "G07": "Diare",
    "G08": "Produksi telur menurun",
    "G09": "Membeku",
    "G10": "Terlihat lesu",
    "G11": "Diare kehijauan",
    "G12": "Diare keputihan",
    "G13": "Wajah pucat",
    "G14": "Terlihat kebiruan",
    "G15": "Bercak membengkak",
    "G16": "Jengger pucat",
    "G17": "Kaki dan sayap lumpuh",
    "G18": "Keluar cairan dari mata dan hidung",
    "G19": "Kepala bengkak",
    "G20": "Kepala berputar",
    "G21": "Pembengkakan sinus dan mata",
    "G22": "Perut membesar",
    "G23": "Sayap menggantung",
    "G24": "Terdapat kotoran putih di sekitar anus",
    "G25": "Kematian mendadak",
    "G26": "Kulit telur kasar",
    "G27": "Putih telur encer",
    "G28": "Feses kuning kehijauan",
    "G29": "Pembengkakan area wajah dan sekitar mata",
    "G30": "Feses berdarah",
    "G31": "Berkelompok di sudut kandang",
    "G32": "Mematuk area kloaka",
    "G33": "Telur lebih kecil",
    "G34": "Lumpuh pada tembolok",
    "G35": "Bernapas lewat mulut sambil menjulurkan leher",
    "G36": "Batuk berdarah",
    "G37": "Tidur dengan paruh menyentuh lantai",
    "G38": "Duduk dengan posisi membungkuk",
    "G39": "Terlihat mengantuk dengan bulu berdiri",
    "G40": "Tubuh kurus",
    "G41": "Ada lendir bercampur darah di rongga mulut",
    "G42": "Kaki pincang"
}

penyakit_dict = {
    "P01": "Tinja berwarna kapur (Pullorum)",
    "P02": "Kolera ayam (Fowl Cholera)",
    "P03": "Flu burung (Avian Influenza)",
    "P04": "Totelo / ND (Newcastle Disease)",
    "P05": "Ayam tifus (Fowl Typhoid)",
    "P06": "Diare (Coccidiosis)",
    "P07": "Gumboro (Gumboro Disease)",
    "P08": "Ayam salesma (Infectious Coryza)",
    "P09": "Batuk ayam kronis (Infectious Bronchitis)",
    "P10": "Busung ayam (Lymphoid Leukosis)",
    "P11": "Batuk berdarah (Infectious Laryngotracheitis)",
    "P12": "Mareks (Marek's Disease)",
    "P13": "Penurunan produksi telur (Egg Drop Syndrome 76 / EDS 76)"
}


RULES_PATH = BASE / ".." / "C:\\Users\\risda\\OneDrive\\Documents\\Tugas Kuliah\\Sistem Pakar\\rules.json"
RULES_PATH = RULES_PATH.resolve()

@app.route("/")
def index():
    return render_template("index.html", gejala=gejala_dict)

@app.route("/diagnose", methods=["POST"])
def diagnose():
    data = request.json
    selected = data.get("gejala", [])
    fact_cfs = data.get("user_cfs", {})
    rules = load_rules(RULES_PATH)
    results = forward_infer(selected, fact_cfs, rules)
    for r in results:
        r["label"] = penyakit_dict.get(r["conclusion"], r["conclusion"])
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
