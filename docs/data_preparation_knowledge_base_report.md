# Data Journey & Knowledge Base Curation Report

**Project:** KrishiSahayak+Gemma  
**Date:** July 8, 2025  
**Status:** Finalized

## 1. Introduction & Objective

The reliability of any AI-driven advisory system is fundamentally dependent on the quality of its underlying knowledge. For the KrishiSahayak+Gemma project, the primary objective was to build a trustworthy, offline-first agricultural assistant. This necessitated the creation of a high-fidelity, verifiable knowledge base to power the system's Retrieval-Augmented Generation (RAG) fallback mechanism.

This document details the iterative engineering process undertaken to prepare this data. It outlines the methods attempted, the technical challenges encountered, and the justification for the final, expert-curated methodology. The project's findings demonstrate that for high-stakes applications like agricultural diagnostics, a purely automated data collection approach is insufficient. A Human-in-the-Loop (HITL) strategy is non-negotiable to ensure the accuracy, trust, and real-world applicability required.

## 2. Initial Data Scoping

The project's scope was defined by a comprehensive collection of image data sourced from two well-regarded public datasets:

- **PlantVillage Dataset:** A large, open-source repository of images of healthy and diseased plant leaves.
- **PlantDoc Dataset:** Another significant collection of plant disease images, with specific relevance to the Indian agricultural context.

By merging and de-duplicating these datasets, a definitive list of 46 distinct plant-disease classes was established. This list formed the basis for our generic `knowledge_base_v0_generic_46-class.csv`, which is used for the initial MVP development and web demo.

## 3. Data Curation Methodology: An Iterative Engineering Process

The core task was to establish a reliable process for creating a structured knowledge base containing accurate symptoms and remedy information. An iterative process involving three distinct methods was undertaken.

### Method 1: Automated Web Scraping (Attempt and Failure)

The initial hypothesis was that the knowledge base could be constructed automatically by scraping information from authoritative websites.

**Process:** A script was developed to iterate through the disease list, perform targeted Google searches prioritizing authoritative domains (e.g., icar.gov.in), and scrape text content.

**Challenges & Reasons for Rejection:**
- **Structural Inconsistency:** Public and academic websites have highly variable HTML structures, making it impossible for a single scraper to reliably extract data.
- **Content Format Barriers:** A significant portion of high-quality information is embedded in .pdf documents, which are not parsable by a standard HTML scraping library.

**Conclusion:** Simple web scraping was too brittle and unreliable to meet the project's quality standards.

### Method 2: Generative AI with Gemma 3n (Attempt and Failure)

The second approach involved leveraging the project's core AI model, Gemma 3n, to generate the knowledge base content.

**Process:** A script was created to prompt Gemma 3n with a specific instruction for each disease, asking it to act as an agricultural scientist and provide structured Symptoms and Remedy information.

**Challenges & Reasons for Rejection:**
- **Formatting Inconsistency:** The model did not always adhere strictly to the requested format, causing parsing logic to fail.
- **Lack of Source Verifiability:** The model, by its nature, does not cite its sources. While the generated information may have been factually correct, its origin could not be verified. This directly violated the project's core principle of building a transparent and trustworthy system.

**Conclusion:** A purely generative approach, while faster, lacked the structural consistency and source verifiability necessary for a high-stakes, real-world application.

### Method 3: Fully Manual, Expert-Led Curation (The Chosen Approach)

The failures of the automated methods led to the final, successful strategy. This is the official process for creating all future production-ready Regional Data Packs.

**Tools:** Human Expertise, Spreadsheet Software, and direct access to authoritative sources.

**Process:**
1. **Direct Research:** The Project Owner and collaborating agricultural experts (scientists, researchers) will directly consult primary, trusted sources (e.g., ICAR publications, state agricultural university portals, peer-reviewed journals).
2. **Manual Curation and Synthesis:** The experts will synthesize the information from these sources and manually write the Symptoms and Remedy descriptions. This ensures the information is not only accurate but also includes the necessary nuance and context for farmers.
3. **Source Citation:** Every piece of information will be accompanied by a citation of the source from which it was derived.
4. **Structuring:** This verified and cited information is then manually structured into the final .csv file, ensuring perfect formatting and data integrity.

## 4. Justification for the Final Methodology

The fully manual, expert-led curation approach was chosen because it is the only method that guarantees the level of trust required for this sensitive domain.

- **It Ensures Maximum Trust:** By completely removing generative AI from the data creation process, we eliminate all risk of factual inaccuracies or "hallucinations." The resulting knowledge base is not a "black box"; its reliability is transparent and can be audited directly against its cited sources.
- **It Captures Human Expertise:** The manual process allows for the inclusion of strategic depth, such as the principles of Integrated Disease Management (IDM), which prioritizes cultural and biological controls—a level of sophistication that automation failed to achieve.
- **It Is Robust:** The resulting CSV files are clean, complete, and correctly formatted, providing a solid foundation for the project's RAG system.

## 5. Accessing Pre-processed Knowledge Base Files

To simplify deployment and ensure consistency, pre-processed knowledge base files are made available through GitHub Releases. These files include the fully curated and processed data ready for use with the KrishiSahayak+Gemma system.

### Available Files

1. **knowledge_base_v0_generic_46-class.csv**
   - CSV file containing the curated knowledge base
   - Columns: Disease, Symptoms, Remedy, Source

2. **knowledge_base_v0_generic_46-class.faiss**
   - FAISS index for fast semantic search
   - Generated from the embeddings of the knowledge base content

3. **knowledge_base_v0_generic_46-class.sqlite**
   - SQLite database for efficient querying
   - Contains the full knowledge base with metadata

4. **knowledge_base_v0_generic_46-class_text.pkl**
   - Serialized text data for quick loading
   - Used by the RAG system for response generation

### Download Instructions

1. Visit the [GitHub Releases](https://github.com/VIKAS9793/KrishiSahayak_Gemma/releases) page
2. Download the `KrishiSahayak_KB_v0.10.0.zip` file from the latest release
3. Extract the contents to the `data/processed/` directory
4. The application will automatically detect and use these files

### File Contents

The ZIP file contains the following files:
- `knowledge_base_v0_generic_46-class.csv`
- `knowledge_base_v0_generic_46-class.faiss`
- `knowledge_base_v0_generic_46-class.sqlite`
- `knowledge_base_v0_generic_46-class_text.pkl`

### Regenerating Files (Advanced)

### Regenerating the Knowledge Base

If you need to regenerate the processed files from the source CSV:

1. Ensure you have the knowledge base CSV file in the correct location:
   ```
   data/processed/knowledge_base_v0_generic_46-class.csv
   ```

2. Run the build index script:
   ```bash
   python asset_preparation/build_index.py
   ```

This will generate the following files in the `data/processed/` directory:
- `knowledge_base_v0_generic_46-class.faiss` - FAISS index for semantic search
- `knowledge_base_v0_generic_46-class.sqlite` - SQLite database for efficient querying
- `knowledge_base_v0_generic_46-class_text.pkl` - Serialized text data for the RAG system

## 6. Conclusion

The journey to create the project's knowledge base underscores a critical lesson in applied AI: for high-stakes, real-world applications, data quality and trustworthiness are paramount. The final, adopted methodology is a fully manual, expert-driven process that ensures the foundation of KrishiSahayak+Gemma is not just data, but trusted, verifiable, and actionable knowledge.