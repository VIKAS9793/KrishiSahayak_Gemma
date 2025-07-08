# Data Versioning Strategy

This document outlines the versioning strategy for the KrishiSahayak-Gemma project's data assets.

## 1. Version Format

A semantic versioning scheme is used to track changes to our knowledge base assets.

### Generic Knowledge Base (For MVP)
```
knowledge_base_v{MAJOR}.{MINOR}_[TYPE]_[DETAILS].{EXT}
```
*Example:* `knowledge_base_v0_generic_46-class.csv`

### Regional Knowledge Bases (Future Scope)
```
knowledge_base_{REGION}_v{MAJOR}.{MINOR}.{EXT}
```
*Example:* `knowledge_base_maharashtra_v1.0.csv`

## 2. Current Data Assets (For MVP Development)

The initial development of the Android MVP will use the following versioned, generic dataset. This allows the engineering team to build and test the application's core technology without being blocked by the long-term data curation process.

- **Version:** v0.1
- **Type:** Generic 46-Class Dataset
- **Files:**
  - `knowledge_base_v0_generic_46-class.csv`
  - `knowledge_base_v0_generic_46-class.faiss`
  - `knowledge_base_v0_generic_46-class_text.pkl`
  - `knowledge_base_v0_generic_46-class.sqlite`

These assets are archived in the `data/_archive/` directory for reference.

## 3. Regional Data Strategy & Versioning

The long-term vision for the production application is to use expert-curated, regional data packs for maximum relevance and accuracy.

### Phased Rollout

The creation of these data packs will follow a phased approach:

1. **Pilot Phase:** The initial data curation effort will focus on the 6 key states outlined in the `REGIONAL_COVERAGE.md` document.
2. **Future Expansion:** Based on the success of the pilot, coverage will be expanded to additional states and union territories.

### Versioning

- Each regional data pack will be versioned independently (e.g., `maharashtra_v1.0`, `punjab_v1.1`).
- This allows for updates to a specific region's data without affecting others.

## 4. Directory Structure

All data assets are organized in a structured manner to ensure clarity and maintainability.

```
data/
├── processed/               # Current version of the knowledge base
│   ├── knowledge_base_v0_generic_46-class.csv
│   ├── knowledge_base_v0_generic_46-class.faiss
│   ├── knowledge_base_v0_generic_46-class_text.pkl
│   └── knowledge_base_v0_generic_46-class.sqlite
├── raw/                    # Raw data sources
│   ├── disease_data.txt
│   ├── diseases_list.txt
│   ├── plantvillage/      # PlantVillage dataset
│   └── plantdoc/          # PlantDoc dataset
└── _archive/              # (Planned) For archiving old versions
```

## 5. Best Practices

- **Immutable Versions:** Once a version is created, it should not be modified. Any changes require a new version number.
- **Documentation:** All relevant documentation (`README.md`, `TECHNICAL_REPORT.md`) must be updated to reflect the current data version in use.
- **Testing:** Any new data version must be thoroughly tested with all dependent systems before being deployed.
- **Archiving:** Previous versions should always be kept in the archive for reference and potential rollbacks.

---
*Last updated: July 8, 2025*
