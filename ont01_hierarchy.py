import json
import pandas as pd
import os

os.makedirs("outputs", exist_ok=True)

# ── Ayurveda Concept Hierarchy (CORRECTED) ──────────────────────────────────
hierarchy = {
  "Ayurveda": {
    "Fundamental Concepts": {
      "Tridosha": ["Vata", "Pitta", "Kapha"],
      "Panchamahabhuta": ["Akasha", "Vayu", "Agni", "Jala", "Prithvi"],
      "Trigunas": ["Sattva", "Rajas", "Tamas"],
      "Sapta Dhatu": ["Rasa", "Rakta", "Mamsa", "Meda", "Asthi", "Majja", "Shukra"],
      "Trimala": ["Mutra", "Purisha", "Sweda"]
    },
    "Prakriti (Constitution)": {
      "Dwandwa Prakriti": ["Vata-Pitta", "Pitta-Kapha", "Vata-Kapha"],
      "Tridoshaja Prakriti": ["Sama Prakriti"]
    },
    "Herbs & Medicinal Plants": {
      "Adaptogenic Herbs": ["Ashwagandha", "Shatavari"],
      "Digestive Herbs": ["Triphala", "Trikatu", "Ginger", "Cumin"],
      "Anti-inflammatory Herbs": ["Turmeric", "Neem", "Guduchi"],
      "Nervine Herbs": ["Brahmi", "Shankhapushpi", "Jatamansi"],
      "Cardiac Herbs": ["Arjuna", "Pushkarmool"]
    },
    "Formulations": {
      "Churna (Powder)": ["Triphala Churna", "Trikatu Churna", "Ashwagandha Churna"],
      "Kwatha (Decoction)": ["Dashmoola Kwatha", "Triphala Kwatha"],
      "Taila (Oil)": ["Sesame Oil", "Brahmi Taila", "Ksheerabala Taila"],
      "Ghrita (Ghee)": ["Shatavari Ghrita", "Brahmi Ghrita"],
      "Vati (Tablet)": ["Arogyavardhini Vati", "Chandraprabha Vati"],
      "Asava/Arishta (Fermented)": ["Dashamularishta", "Saraswatarishta"]
    },
    "Diseases (Vyadhi)": {
      "Digestive Disorders": ["Ajirna", "Atisara", "Grahani", "Arsha"],
      "Respiratory Disorders": ["Kasa", "Swasa", "Pratishyaya"],
      "Metabolic Disorders": ["Prameha", "Madhumeha", "Sthoulya"],
      "Neurological Disorders": ["Apasmara", "Unmada", "Vata Vyadhi"],
      "Skin Disorders": ["Kushtha", "Vicharchika", "Shwitra"]
    },
    "Treatment Modalities": {
      "Panchakarma": ["Vamana", "Virechana", "Basti", "Nasya", "Raktamokshana"],
      "Shamana Chikitsa": ["Langhana", "Deepana", "Pachana"],
      "Rasayana (Rejuvenation)": ["Chyawanprash", "Brahma Rasayana"],
      "Ahara (Diet Therapy)": ["Pathya Ahara", "Apathya Ahara"],
      "Yoga & Pranayama": ["Surya Namaskar", "Pranayama", "Dhyana"]
    },
    "Diagnostic Methods": {
      "Ashtavidha Pariksha": [
        "Nadi (Pulse)", "Mutra (Urine)", "Mala (Stool)",
        "Jihva (Tongue)", "Shabda (Voice)", "Sparsha (Touch)",
        "Drik (Eyes)", "Akriti (Appearance)"
      ],
      "Dashavidha Pariksha": ["Prakriti", "Vikriti", "Sara", "Samhanana",
                               "Pramana", "Satmya", "Satva", "Ahara Shakti",
                               "Vyayama Shakti", "Vaya"]
    }
  }
}

# ── Save JSON ────────────────────────────────────────────────────────────────
with open("outputs/ont01_hierarchy.json", "w", encoding="utf-8") as f:
    json.dump(hierarchy, f, indent=2, ensure_ascii=False)
print("ont01_hierarchy.json saved")

# ── Flatten to CSV ───────────────────────────────────────────────────────────
rows = []
for root, categories in hierarchy.items():
    for category, subcategories in categories.items():
        for subcategory, concepts in subcategories.items():
            for concept in concepts:
                rows.append({
                    "root": root,
                    "category": category,
                    "subcategory": subcategory,
                    "concept": concept,
                    "level": 4
                })

df = pd.DataFrame(rows)
# Remove any accidental duplicate concepts
df = df.drop_duplicates(subset=["concept"], keep="first")
df.to_csv("outputs/ont01_hierarchy.csv", index=False, encoding="utf-8")
print("ont01_hierarchy.csv saved")
print(f"   Total rows: {len(df)}")