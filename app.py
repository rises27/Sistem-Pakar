import tkinter as tk
from tkinter import messagebox
from inference_engine.forward_cf import load_rules, forward_chaining, combine_cf

rules = load_rules()

gejala_list = {
    "G01": "Usia lebih dari 40 tahun",
    "G02": "Kelebihan berat badan",
    "G03": "Riwayat patah tulang",
    "G04": "Riwayat keluarga osteoporosis",
    "G05": "Menopause",
    "G06": "Sakit punggung berkelanjutan",
    "G07": "Sering merokok",
    "G08": "Nyeri sendi",
    "G09": "Kekurangan hormon testosteron",
    "G10": "Sering konsumsi alkohol",
    "G11": "Keretakan tulang punggung",
    "G12": "Konsumsi obat steroid",
    "G13": "Penyakit hipertiroidisme"
}

root = tk.Tk()
root.title("Sistem Pakar Osteoporosis")
root.geometry("500x600")

tk.Label(root, text="Pilih Gejala yang Dirasakan:", font=("Arial", 12, "bold")).pack(pady=10)

var_dict = {}
for code, desc in gejala_list.items():
    var_dict[code] = tk.IntVar()
    tk.Checkbutton(root, text=desc, variable=var_dict[code]).pack(anchor="w")

def diagnose():
    selected = [code for code, val in var_dict.items() if val.get() == 1]
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih minimal satu gejala.")
        return

    conclusions = forward_chaining(selected, rules)
    if conclusions:
        penyakit = conclusions[0][0]
        cf_total = combine_cf([c[1] for c in conclusions])
        messagebox.showinfo("Hasil Diagnosa", f"Penyakit: {penyakit}\nTingkat Keyakinan: {cf_total*100:.1f}%")
    else:
        messagebox.showinfo("Hasil Diagnosa", "Tidak ditemukan hasil yang sesuai.")

tk.Button(root, text="Diagnosa", command=diagnose, bg="lightblue", width=20).pack(pady=20)

root.mainloop()
