from flask import Flask, render_template, request, jsonify
from pathlib import Path
from inference_engine.forward_cf import load_rules, forward_infer

app = Flask(__name__, template_folder="templates", static_folder="static")
BASE = Path(__file__).resolve().parents[1]

# Gejala dikategorikan
GEJALA = {
    "Kerusakan pada Daun": {
        "A1": "Ujung atau tepi daun berwarna cokelat keabu-abuan",
        "A2": "Daun memiliki bercak cokelat berbentuk belah ketupat",
        "A3": "Daun memiliki bercak cokelat sempit dan memanjang",
        "A4": "Terdapat bercak putih pada daun berupa garis atau gulungan",
        "A5": "Daun berwarna kuning hingga oranye kekuningan, terlihat wereng hijau pada daun",
        "B1": "Daun menguning lalu mengering",
        "B2": "Ujung atau tepi daun berwarna cokelat keabu-abuan dan kemudian menyebar ke seluruh daun",
        "B3": "Ujung dan tepi daun mengering serta layu"
    },
    "Kerusakan pada Batang": {
        "A6": "Batang mengering dan bagian pangkal batang tampak cokelat akibat wereng cokelat",
        "A7": "Pucuk batang padi mengering dan mudah dicabut",
        "A8": "Di dalam batang tanaman terdapat larva atau ulat",
        "A9": "Batang tanaman berwarna kuning atau cokelat kemerahan dan terdapat bercak hitam",
        "A10": "Batang padi roboh, terlihat adanya serangan tikus",
        "B4": "Malai padi busuk atau patah pada fase generatif",
        "B5": "Batang dan tulang daun membusuk sehingga tanaman rebah",
        "B6": "Tangkai malai padi patah dan rusak"
    },
    "Kerusakan pada Gabah": {
        "A11": "Terdapat bercak hitam pada gabah",
        "A12": "Gabah rontok, terlihat burung di area sawah",
        "B7": "Jumlah malai sedikit dan gabah banyak yang kosong",
        "B8": "Gabah tidak terisi penuh atau hampa",
        "B9": "Malai padi berdiri tegak namun gabah tidak terisi penuh atau hampa",
        "B10": "Warna gabah berubah dan rasanya menjadi tidak enak"
    },
    "Kerusakan akibat Faktor Luar": {
        "B11": "Tanaman layu dan mati pada awal pertumbuhan",
        "B12": "Daun tanaman berwarna kuning oranye",
        "B13": "Pertumbuhan tanaman kerdil",
        "B14": "Pertumbuhan tanaman terhambat",
        "B16": "Tanaman muda mati dan mengering",
        "B17": "Penggunaan pupuk nitrogen (N) secara berlebihan",
        "B20": "Terdapat jejak kaki dan lubang tikus di sekitar sawah"
    }
}

PENYAKIT = {
    "P01": "Hawar Daun Bakteri",
    "P02": "Penyakit BLAS",
    "P03": "Bercak Daun Cokelat Sempit",
    "P04": "Wereng Hijau & Tungro",
    "P05": "Wereng Cokelat",
    "P06": "Penggerek Batang Padi",
    "P07": "Serangga Padi Hitam",
    "P08": "Tikus Sawah",
    "P09": "Serangga Padi Berbau"
}


RULES_PATH = BASE / ".." / "C:\\Users\\F4QIH\\OneDrive\\Documents\\Perkuliahan\\Tugas Kuliah\\Semester 5\\Sistem Pakar\\Sistem pakar berbasis rule-based, forward chaining, dan CF\\rules.json"
RULES_PATH = RULES_PATH.resolve()

@app.route("/")
def index():
    return render_template("index.html", gejala=GEJALA)

@app.route("/diagnose", methods=["POST"])
def diagnose():
    data = request.json
    selected = data.get("gejala", [])
    fact_cfs = data.get("fact_cfs", {})
    rules = load_rules(RULES_PATH)
    results = forward_infer(selected, fact_cfs, rules)
    for r in results:
        r["label"] = PENYAKIT.get(r["conclusion"], r["conclusion"])
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
