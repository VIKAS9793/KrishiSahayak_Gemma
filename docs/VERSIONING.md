# Data Versioning Strategy

This document outlines the versioning strategy for the KrishiSahayak-Gemma project's data assets.

## Version Format

```
knowledge_base_v{MAJOR}.{MINOR}_[TYPE]_[DETAILS].{EXT}
```

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

## Directory Structure

```
data/
├── _archive/               # Versioned datasets
│   └── knowledge_base_v0_generic_46-class.*
├── processed/              # Processed data (temporary)
└── raw/                    # Raw data sources
```

## Creating a New Version

1. **Major Version (v1, v2, etc.)**
   - Significant changes to data structure
   - Addition of new disease classes
   - Major updates to existing information

2. **Minor Version (v0.1, v0.2, etc.)**
   - Minor corrections
   - Formatting improvements
   - Small additions to existing entries

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
