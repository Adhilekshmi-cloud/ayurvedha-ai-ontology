import json
import pandas as pd
import os

os.makedirs("outputs", exist_ok=True)

vocabulary = [
  {"term_id": "AYU-001", "preferred_term": "Vata", "term_type": "Dosha", "definition": "One of the three biological energies governing movement, nervous system, and elimination", "standard_source": "Charaka Samhita", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-002", "preferred_term": "Pitta", "term_type": "Dosha", "definition": "One of the three biological energies governing digestion, metabolism, and transformation", "standard_source": "Charaka Samhita", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-003", "preferred_term": "Kapha", "term_type": "Dosha", "definition": "One of the three biological energies governing structure, lubrication, and immunity", "standard_source": "Charaka Samhita", "icd_mapping": "N/A", "status": "Active"},

  {"term_id": "AYU-010", "preferred_term": "Rasa Dhatu", "term_type": "Dhatu", "definition": "First tissue layer; plasma and lymphatic fluid", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-011", "preferred_term": "Rakta Dhatu", "term_type": "Dhatu", "definition": "Second tissue layer; blood and its components", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-012", "preferred_term": "Mamsa Dhatu", "term_type": "Dhatu", "definition": "Third tissue layer; muscle tissue", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-013", "preferred_term": "Meda Dhatu", "term_type": "Dhatu", "definition": "Fourth tissue layer; adipose/fat tissue", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-014", "preferred_term": "Asthi Dhatu", "term_type": "Dhatu", "definition": "Fifth tissue layer; bone tissue", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-015", "preferred_term": "Majja Dhatu", "term_type": "Dhatu", "definition": "Sixth tissue layer; bone marrow and nerve tissue", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-016", "preferred_term": "Shukra Dhatu", "term_type": "Dhatu", "definition": "Seventh tissue layer; reproductive tissue", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},

  {"term_id": "AYU-020", "preferred_term": "Ashwagandha", "term_type": "Herb", "definition": "Withania somnifera; adaptogenic herb used for strength and vitality", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-021", "preferred_term": "Shatavari", "term_type": "Herb", "definition": "Asparagus racemosus; rejuvenating herb for female reproductive health", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-022", "preferred_term": "Brahmi", "term_type": "Herb", "definition": "Bacopa monnieri; nervine tonic for memory and cognition", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-023", "preferred_term": "Haridra", "term_type": "Herb", "definition": "Curcuma longa; anti-inflammatory and antimicrobial herb", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-024", "preferred_term": "Nimba", "term_type": "Herb", "definition": "Azadirachta indica; blood purifier and skin disease remedy", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-025", "preferred_term": "Guduchi", "term_type": "Herb", "definition": "Tinospora cordifolia; immunomodulator and adaptogen", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-026", "preferred_term": "Amalaki", "term_type": "Herb", "definition": "Emblica officinalis; richest natural source of Vitamin C, Rasayana herb", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-027", "preferred_term": "Haritaki", "term_type": "Herb", "definition": "Terminalia chebula; digestive, laxative, and Rasayana herb", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-028", "preferred_term": "Bibhitaki", "term_type": "Herb", "definition": "Terminalia bellerica; respiratory and digestive herb", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-029", "preferred_term": "Arjuna", "term_type": "Herb", "definition": "Terminalia arjuna; cardiac tonic herb", "standard_source": "Ayurvedic Pharmacopoeia of India Vol.1", "icd_mapping": "N/A", "status": "Active"},

  {"term_id": "AYU-040", "preferred_term": "Triphala Churna", "term_type": "Formulation", "definition": "Powder of three fruits (Amalaki, Haritaki, Bibhitaki); digestive and detox formula", "standard_source": "Ayurvedic Formulary of India", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-041", "preferred_term": "Trikatu Churna", "term_type": "Formulation", "definition": "Powder of three pungents (Shunthi, Maricha, Pippali); digestive stimulant", "standard_source": "Ayurvedic Formulary of India", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-042", "preferred_term": "Chyawanprash", "term_type": "Formulation", "definition": "Classical Rasayana jam with Amalaki base; immunity booster", "standard_source": "Charaka Samhita / Ayurvedic Formulary of India", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-043", "preferred_term": "Dashamularishta", "term_type": "Formulation", "definition": "Fermented preparation of ten roots; tonic for postpartum and respiratory health", "standard_source": "Ayurvedic Formulary of India", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-044", "preferred_term": "Arogyavardhini Vati", "term_type": "Formulation", "definition": "Classical tablet for liver disorders and skin diseases", "standard_source": "Ayurvedic Formulary of India", "icd_mapping": "N/A", "status": "Active"},

  {"term_id": "AYU-050", "preferred_term": "Prameha", "term_type": "Disease", "definition": "Group of urinary disorders including diabetes mellitus", "standard_source": "Charaka Samhita", "icd_mapping": "E11 (Type 2 DM)", "status": "Active"},
  {"term_id": "AYU-051", "preferred_term": "Sthoulya", "term_type": "Disease", "definition": "Obesity; excess accumulation of Meda Dhatu", "standard_source": "Charaka Samhita", "icd_mapping": "E66 (Obesity)", "status": "Active"},
  {"term_id": "AYU-052", "preferred_term": "Kasa", "term_type": "Disease", "definition": "Cough; classified into five types based on dosha involvement", "standard_source": "Charaka Samhita", "icd_mapping": "R05 (Cough)", "status": "Active"},
  {"term_id": "AYU-053", "preferred_term": "Swasa", "term_type": "Disease", "definition": "Dyspnoea/Asthma; breathing difficulty due to Vata-Kapha imbalance", "standard_source": "Charaka Samhita", "icd_mapping": "J45 (Asthma)", "status": "Active"},
  {"term_id": "AYU-054", "preferred_term": "Arsha", "term_type": "Disease", "definition": "Haemorrhoids/Piles; anorectal disease classified in Sushruta", "standard_source": "Sushruta Samhita", "icd_mapping": "K64 (Haemorrhoids)", "status": "Active"},
  {"term_id": "AYU-055", "preferred_term": "Kushtha", "term_type": "Disease", "definition": "Skin diseases including leprosy; 18 types described in classics", "standard_source": "Charaka Samhita", "icd_mapping": "L98 (Skin disorders NEC)", "status": "Active"},
  {"term_id": "AYU-056", "preferred_term": "Ajirna", "term_type": "Disease", "definition": "Indigestion; impaired digestive fire (Agni)", "standard_source": "Ashtanga Hridayam", "icd_mapping": "K30 (Functional dyspepsia)", "status": "Active"},

  {"term_id": "AYU-060", "preferred_term": "Vamana", "term_type": "Panchakarma", "definition": "Therapeutic emesis; primary treatment for Kapha disorders", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-061", "preferred_term": "Virechana", "term_type": "Panchakarma", "definition": "Therapeutic purgation; primary treatment for Pitta disorders", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-062", "preferred_term": "Basti", "term_type": "Panchakarma", "definition": "Medicated enema; primary treatment for Vata disorders", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-063", "preferred_term": "Nasya", "term_type": "Panchakarma", "definition": "Nasal drug administration; treatment for head and neck disorders", "standard_source": "Ashtanga Hridayam", "icd_mapping": "N/A", "status": "Active"},
  {"term_id": "AYU-064", "preferred_term": "Raktamokshana", "term_type": "Panchakarma", "definition": "Bloodletting therapy; treatment for blood-borne disorders", "standard_source": "Sushruta Samhita", "icd_mapping": "N/A", "status": "Active"},
]

# ── Save JSON ────────────────────────────────────────────────────────────────
with open("outputs/ont03_vocabulary.json", "w", encoding="utf-8") as f:
    json.dump(vocabulary, f, indent=2, ensure_ascii=False)
print("ont03_vocabulary.json saved")

# ── Save CSV ─────────────────────────────────────────────────────────────────
df = pd.DataFrame(vocabulary)
df = df.drop_duplicates(subset=["term_id"], keep="first")
df.to_csv("outputs/ont03_vocabulary.csv", index=False, encoding="utf-8")
print("ont03_vocabulary.csv saved")
print(f"   Total terms: {len(df)}")