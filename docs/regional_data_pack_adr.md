# Architectural Decision Record: Regional Data Pack Strategy

> **About ADRs**: An Architectural Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences. This helps the team understand why a particular approach was chosen.

**ID:** ADR-001  
**Date:** July 7, 2025  
**Status:** Adopted  
**Author:** KrishiSahayak AI Engineering Team

## 1. Executive Summary

This document details the strategic decision to pivot from a single, monolithic knowledge base to a modular "Regional Data Pack" architecture. This decision was taken to make the KrishiSahayak application significantly more efficient, relevant, and user-friendly for our target audience of farmers across all 36 states and union territories of India, each with its unique agricultural practices and challenges.

This new architecture solves critical challenges related to storage, performance, and user relevance, while offering unprecedented flexibility for future updates and scalability. It is a cornerstone of our commitment to a user-centric design that respects the resource constraints of our end-users.

## 2. The Initial Approach and Its Limitations

Our initial plan was to build a single, comprehensive knowledge base containing information on all major crops and diseases across India. While comprehensive, this approach presented several critical limitations when considering our end-users' environment:

- **Irrelevant Data Overload**: A farmer in Punjab, primarily concerned with wheat and cotton, would have their device's resources consumed by data on coconut and rubber plant diseases from Kerala. This is inefficient and creates a poor user experience.

- **Excessive Storage Footprint**: A single, nationwide knowledge base (SQLite + FAISS index) would be very large, potentially exceeding 500MB or more. This is a significant storage burden on low-cost smartphones with limited available space.

- **Slower Performance**: The Retrieval-Augmented Generation (RAG) system's search speed is directly related to the size of the FAISS index. A larger, nationwide index would result in slower semantic searches, making the app less responsive when the AI needs to fall back on the knowledge base.

- **Inflexible Updates**: To update or add information for a single crop, we would need to redistribute the entire, massive database file through our offline network. This would be inefficient and cumbersome for both our partner NGOs and the end-users.

## 3. The "Regional Data Pack" Architecture

The new architecture addresses all the limitations above by treating regional knowledge as a modular, plug-and-play component. The system is designed to cover all 36 states and union territories of India, with each region having its own specialized data pack containing locally relevant agricultural knowledge.

### Concept

A "Data Pack" is a self-contained bundle of assets tailored to a specific geographical region (e.g., a state like Maharashtra or Punjab). Each pack contains:

1. A `knowledge_base_[region].sqlite` file: A lightweight SQLite database containing only the curated data on crops and diseases relevant to that region.

2. A `knowledge_base_[region].faiss` file: A compact FAISS vector index built exclusively from the text in the regional SQLite database.

### Deployment Model

This model integrates perfectly with our offline distribution strategy. A local NGO agent in a specific state will provide the farmer with two items:

1. The small, universal `KrishiSahayak.apk` file.
2. The small, relevant `[region]_data_pack.zip` containing the specific SQLite and FAISS files for their area.

The application is being designed to detect and load the data pack present on the user's device, ensuring all searches and lookups are performed against the local, relevant dataset.

## 4. Advantages and Problems Solved

This architectural decision provides four key advantages:

| #  | Advantage | Problem Solved |
|----|-----------|----------------|
| 1  | Hyper-Relevance | Solves: Irrelevant Information  
The application becomes a specialized tool for the farmer's specific region. It provides targeted, relevant information, which builds trust and makes the tool significantly more useful in their daily work. |
| 2  | Reduced Footprint | Solves: Storage Constraints  
Instead of one massive >500MB database, a user only needs the ~20-50MB pack for their region. This is a 90%+ reduction in the storage burden, a critical factor on low-cost devices. |
| 3  | Enhanced Performance | Solves: Slow Search and App Latency  
Searching a smaller, regional FAISS index is much faster than searching a nationwide one. This means when the RAG fallback is needed, the user gets a faster, more responsive experience. |
| 4  | Flexibility & Scalability | Solves: Inefficient Updates and Future Growth  
We can now update or add crop data for a single region by distributing only that small data pack. This makes updates seamless. Furthermore, it allows us to easily scale by creating new packs for new regions or even specialized packs (e.g., "organic farming," "horticulture") in the future. |

## 5. Conclusion

The decision to adopt the Regional Data Pack architecture was a critical strategic pivot. It aligns the project more closely with our core principles of user-centricity, efficiency, and offline-first design. While it requires a more sophisticated data preparation pipeline on our end, the benefits in terms of user experience, performance, and long-term maintainability are immense. This makes the KrishiSahayak application a more practical, powerful, and trusted tool for the farmers we aim to serve.

- Large file size (>500MB)
- Slow search performance
- Irrelevant data for most users
- Inefficient updates

## Solution
Implement regional data packs:

1. **Structure**
   - Each region has its own SQLite DB and FAISS index
   - Files named: `knowledge_base_[region].{sqlite,faiss}`
   - Packaged as `[region]_data_pack.zip`

2. **Deployment**
   - Core app distributed as small APK
   - Regional packs distributed separately
   - App auto-detects and loads regional pack

## Benefits

### 1. Relevance
- Farmers see only region-specific information
- More focused user experience
- Builds trust through local relevance

### 2. Performance
- Smaller FAISS indexes = faster searches
- Reduced memory usage
- Faster app startup

### 3. Efficiency
- Typical pack size: 20-50MB (90% smaller)
- Lower storage requirements
- Better for low-end devices

### 4. Maintainability
- Update individual regions
- Easier testing
- Gradual rollout of changes

## Implementation
1. Create data pipeline for regional packs
2. Update app to support pack loading
3. Develop distribution system for NGOs
4. Document pack creation process

## Status
Adopted and in progress.
