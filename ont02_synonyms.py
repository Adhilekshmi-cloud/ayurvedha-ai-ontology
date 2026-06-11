import json
import pandas as pd
import os

os.makedirs("outputs", exist_ok=True)

synonyms = [
  # Doshas
  {"sanskrit": "Vata", "english": "Wind / Air-Space Energy", "category": "Dosha", "alternate_sanskrit": "Anila, Pavana", "source": "Charaka Samhita"},
  {"sanskrit": "Pitta", "english": "Fire / Bile Energy", "category": "Dosha", "alternate_sanskrit": "Agni, Teja", "source": "Charaka Samhita"},
  {"sanskrit": "Kapha", "english": "Water / Earth Energy", "category": "Dosha", "alternate_sanskrit": "Shleshma, Ledha", "source": "Charaka Samhita"},

  # Dhatus
  {"sanskrit": "Rasa", "english": "Plasma / Lymph", "category": "Dhatu", "alternate_sanskrit": "Ahara Rasa", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Rakta", "english": "Blood", "category": "Dhatu", "alternate_sanskrit": "Asra, Lohita", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Mamsa", "english": "Muscle Tissue", "category": "Dhatu", "alternate_sanskrit": "Palala", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Meda", "english": "Adipose / Fat Tissue", "category": "Dhatu", "alternate_sanskrit": "Vasaa", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Asthi", "english": "Bone Tissue", "category": "Dhatu", "alternate_sanskrit": "Haddi", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Majja", "english": "Bone Marrow / Nerve Tissue", "category": "Dhatu", "alternate_sanskrit": "", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Shukra", "english": "Reproductive Tissue / Semen", "category": "Dhatu", "alternate_sanskrit": "Retas", "source": "Ashtanga Hridayam"},

  # Herbs
  {"sanskrit": "Ashwagandha", "english": "Indian Ginseng / Winter Cherry", "category": "Herb", "alternate_sanskrit": "Vajigandha, Balya", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Shatavari", "english": "Asparagus", "category": "Herb", "alternate_sanskrit": "Shatamuli, Bahusuta", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Brahmi", "english": "Water Hyssop / Bacopa", "category": "Herb", "alternate_sanskrit": "Saraswati, Mandukparni", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Haridra", "english": "Turmeric", "category": "Herb", "alternate_sanskrit": "Kanchani, Nisha", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Nimba", "english": "Neem", "category": "Herb", "alternate_sanskrit": "Pichumarda, Arishta", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Guduchi", "english": "Giloy / Tinospora", "category": "Herb", "alternate_sanskrit": "Amrita, Chakrangi", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Amalaki", "english": "Indian Gooseberry / Amla", "category": "Herb", "alternate_sanskrit": "Dhatri, Amrita", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Bibhitaki", "english": "Belleric Myrobalan", "category": "Herb", "alternate_sanskrit": "Vibhitaka, Karshaphala", "source": "Ayurvedic Formulary of India"},
  {"sanskrit": "Haritaki", "english": "Chebulic Myrobalan", "category": "Herb", "alternate_sanskrit": "Abhaya, Pathya", "source": "Ayurvedic Formulary of India"},
  {"sanskrit": "Shunthi", "english": "Dry Ginger", "category": "Herb", "alternate_sanskrit": "Vishvabheshaja, Nagara", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Maricha", "english": "Black Pepper", "category": "Herb", "alternate_sanskrit": "Krishnadi, Vellaja", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Pippali", "english": "Long Pepper", "category": "Herb", "alternate_sanskrit": "Magadhi, Ushana", "source": "Ayurvedic Pharmacopoeia of India"},
  {"sanskrit": "Arjuna", "english": "Arjuna Tree / Terminalia arjuna", "category": "Herb", "alternate_sanskrit": "Kakubha, Nadisarja", "source": "Ayurvedic Pharmacopoeia of India"},

  # Diseases
  {"sanskrit": "Prameha", "english": "Urinary Disorders / Diabetes", "category": "Disease", "alternate_sanskrit": "Madhumeha (specific)", "source": "Charaka Samhita"},
  {"sanskrit": "Ajirna", "english": "Indigestion", "category": "Disease", "alternate_sanskrit": "Amasaya Roga", "source": "Charaka Samhita"},
  {"sanskrit": "Kasa", "english": "Cough", "category": "Disease", "alternate_sanskrit": "", "source": "Charaka Samhita"},
  {"sanskrit": "Swasa", "english": "Asthma / Dyspnoea", "category": "Disease", "alternate_sanskrit": "Shwasa", "source": "Charaka Samhita"},
  {"sanskrit": "Kushtha", "english": "Skin Diseases / Leprosy", "category": "Disease", "alternate_sanskrit": "", "source": "Charaka Samhita"},
  {"sanskrit": "Arsha", "english": "Haemorrhoids / Piles", "category": "Disease", "alternate_sanskrit": "", "source": "Sushruta Samhita"},
  {"sanskrit": "Sthoulya", "english": "Obesity", "category": "Disease", "alternate_sanskrit": "Atisthaulya", "source": "Charaka Samhita"},

  # Treatments
  {"sanskrit": "Vamana", "english": "Therapeutic Emesis / Vomiting Therapy", "category": "Panchakarma", "alternate_sanskrit": "", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Virechana", "english": "Therapeutic Purgation", "category": "Panchakarma", "alternate_sanskrit": "", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Basti", "english": "Medicated Enema", "category": "Panchakarma", "alternate_sanskrit": "Vasti", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Nasya", "english": "Nasal Administration", "category": "Panchakarma", "alternate_sanskrit": "Nasyakarma", "source": "Ashtanga Hridayam"},
  {"sanskrit": "Raktamokshana", "english": "Bloodletting Therapy", "category": "Panchakarma", "alternate_sanskrit": "", "source": "Sushruta Samhita"},

  # Formulations
  {"sanskrit": "Triphala", "english": "Three Fruits Combination", "category": "Formulation", "alternate_sanskrit": "", "source": "Ayurvedic Formulary of India"},
  {"sanskrit": "Trikatu", "english": "Three Pungents Combination", "category": "Formulation", "alternate_sanskrit": "", "source": "Ayurvedic Formulary of India"},
  {"sanskrit": "Chyawanprash", "english": "Herbal Jam / Rasayana Preparation", "category": "Formulation", "alternate_sanskrit": "Chyavanaprasham", "source": "Charaka Samhita"},
]

# ── Save JSON ────────────────────────────────────────────────────────────────
with open("outputs/ont02_synonyms.json", "w", encoding="utf-8") as f:
    json.dump(synonyms, f, indent=2, ensure_ascii=False)
print("✅ ont02_synonyms.json saved")

# ── Save CSV ─────────────────────────────────────────────────────────────────
df = pd.DataFrame(synonyms)
df.to_csv("outputs/ont02_synonyms.csv", index=False, encoding="utf-8")
print("✅ ont02_synonyms.csv saved")
print(f"   Total terms: {len(df)}")