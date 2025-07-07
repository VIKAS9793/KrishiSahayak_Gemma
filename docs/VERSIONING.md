# Data Versioning Strategy

This document outlines the versioning strategy for the KrishiSahayak-Gemma project's data assets.

## Version Format

### Global Knowledge Base
```
knowledge_base_v{MAJOR}.{MINOR}_[TYPE]_[DETAILS].{EXT}
```

### Regional Knowledge Bases
```
knowledge_base_{REGION}_v{MAJOR}.{MINOR}.{EXT}
```

Where:
- `{REGION}`: Lowercase, underscore-separated region name (e.g., maharashtra, punjab)
  - Covers all 36 states and union territories of India
  - Naming follows ISO 3166-2:IN where applicable
- `{MAJOR}`: Major version number (breaking changes)
- `{MINOR}`: Minor version number (backward-compatible changes)
- `{EXT}`: File extension (csv, sqlite, faiss, etc.)

- `MAJOR`: Incremented for significant changes or additions to the knowledge base
- `MINOR`: Incremented for minor updates or corrections
- `TYPE`: Describes the type of dataset (e.g., `generic`, `regional`)
- `DETAILS`: Additional details about the dataset (e.g., `46-class`)
- `EXT`: File extension (csv, faiss, pkl, sqlite)

## Current Version

**v0.1 - Generic 46-class Dataset**
- `knowledge_base_v0_generic_46-class.csv`
- `knowledge_base_v0_generic_46-class.faiss`
- `knowledge_base_v0_generic_46-class_text.pkl`
- `knowledge_base_v0_generic_46-class.sqlite`

## Regional Coverage

The regional knowledge base covers all 36 states and union territories of India, ensuring comprehensive agricultural support across the entire country. This includes:

- 28 states (e.g., Maharashtra, Punjab, Kerala)
- 8 union territories (e.g., Delhi, Jammu & Kashmir, Ladakh)
- Each region has its own specialized data pack with locally relevant agricultural knowledge

## Directory Structure

```
data/
├── _archive/               # Versioned global datasets
│   └── knowledge_base_v0_generic_46-class.*
├── regional_kbs/           # Regional knowledge bases
│   ├── 1_raw_text/        # Raw text data
│   ├── 2_curated_csv/     # Processed CSV files
│   ├── 3_sqlite_packs/    # SQLite databases
│   └── 4_faiss_packs/     # FAISS indices
├── processed/              # Temporary processed data
└── raw/                    # Raw data sources
```

## Creating a New Version

### Global Knowledge Base
1. **Major Version (v1, v2, etc.)**
   - Significant changes to data structure
   - Addition of new disease classes
   - Major updates to existing information

2. **Minor Version (v0.1, v0.2, etc.)**
   - Minor corrections
   - Formatting improvements
   - Small additions to existing entries

### Regional Knowledge Bases
1. **Versioning per Region**
   - Each region maintains its own version number
   - Version format: `v{MAJOR}.{MINOR}` (e.g., v1.0, v1.1, v2.0)
   - Update version when making changes specific to a region

2. **Synchronization**
   - When updating the global knowledge base, consider if regional versions need updates
   - Document any dependencies between global and regional versions

## Updating Dependencies

When creating a new version, ensure all related files are updated:

1. Web demo configuration
2. Android app assets
3. Documentation references
4. Test cases

## Backward Compatibility

- The web demo and mobile app should specify which version they require
- Include migration scripts if data structure changes
- Maintain documentation of changes between versions

## Best Practices

1. Always create a new version when making changes to the knowledge base
2. Update documentation to reflect the current version in use
3. Test all dependent systems with the new version before deployment
4. Keep previous versions in the archive for reference and rollback
