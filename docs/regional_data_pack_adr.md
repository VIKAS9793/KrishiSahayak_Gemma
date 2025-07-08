# Architectural Decision Record: Regional Data Pack Strategy

| **ID** | ADR-001 |
|--------|---------|
| **Date** | July 8, 2025 |
| **Status** | Adopted |
| **Author** | KrishiSahayak AI Engineering Team |

## 1. Context

The project requires a knowledge base to power its Retrieval-Augmented Generation (RAG) system. The initial plan was to use a single, comprehensive knowledge base covering all of India. However, this monolithic approach was found to have significant drawbacks for our target users, including:

- **Irrelevant Data**: A farmer in one state would have their device's resources burdened with data irrelevant to their region.
- **Excessive Storage Footprint**: A single, nationwide database would be too large for low-resource devices.
- **Slower Performance**: A larger FAISS index would lead to slower semantic search times.
- **Inflexible Updates**: Updating information for a single region would require redistributing the entire database.

A more modular and user-centric approach was required.

## 2. Decision

We will adopt a phased, modular "Regional Data Pack" architecture.

1. **MVP Development Phase**: To accelerate the technical development of the Android application, the initial MVP will be built and tested using the existing generic 46-class dataset. This de-risks the engineering effort by separating it from the data curation timeline.

2. **Production Data Phase**: Following the successful validation of the MVP's technical framework, we will begin creating expert-curated Regional Data Packs. The initial rollout will focus on a pilot of 6 key states. This data will be curated manually by agricultural experts, with no AI involvement in data generation, to ensure maximum accuracy and trust.

## 3. The "Regional Data Pack" Architecture

A "Data Pack" is a self-contained bundle of assets tailored to a specific geographical region.

- **Contents**: Each pack will contain two files:
  - A `knowledge_base_[region].sqlite` file with curated data on local crops and diseases.
  - A `knowledge_base_[region].faiss` file, a compact vector index built from the regional data.

- **Deployment**: The small, universal `.apk` will be distributed alongside the small, relevant regional data pack via offline P2P methods. The application will be designed to detect and load the available data pack.

## 4. Consequences

### Positive:

1. **Relevance**: Users receive information tailored specifically to their region, building trust and utility.
2. **Performance**: Smaller, regional FAISS indexes result in faster search times and a more responsive app.
3. **Efficiency**: The storage footprint on the user's device is drastically reduced (e.g., from >500MB to ~20-50MB per pack).
4. **Maintainability**: Data for a single region can be updated independently without affecting others, simplifying the update process for our offline distribution network.
5. **De-risked Development**: The phased approach allows the engineering team to build and validate the core application immediately, without being blocked by the long-term data curation effort.

### Negative:

1. **Increased Curation Effort**: This approach requires a more sophisticated data pipeline and a significant manual curation effort for each new region we support. This is a recognized and accepted trade-off for the superior user experience.

---
*Last updated: July 8, 2025*
