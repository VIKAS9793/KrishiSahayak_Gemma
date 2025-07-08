# Data Journey & Knowledge Base Curation Report

**Project:** KrishiSahayak+Gemma  
**Date:** July 3, 2025  
**Status:** Completed

## 1. Introduction & Objective

The reliability of any AI-driven advisory system is fundamentally dependent on the quality of its underlying knowledge. For the KrishiSahayak+Gemma project, the primary objective was to build a trustworthy, offline-first agricultural assistant for six key Indian states (Maharashtra, Uttar Pradesh, Punjab, Himachal Pradesh, Jammu & Kashmir, and Ladakh). This necessitated the creation of a high-fidelity, verifiable knowledge base to power the system's Retrieval-Augmented Generation (RAG) fallback mechanism, with content specifically curated for these regions.

This document details the iterative engineering process undertaken to prepare this data. It outlines the methods attempted, the technical challenges encountered, and the justification for the final, expert-curated methodology. The project's findings demonstrate that for high-stakes applications like agricultural diagnostics, a purely automated data collection approach is insufficient. A Human-in-the-Loop (HITL) strategy is non-negotiable to ensure the accuracy, trust, and real-world applicability required.

## 2. Initial Data Scoping

The project's initial scope was defined by a comprehensive collection of image data from six key Indian states, sourced from two well-regarded public datasets and augmented with region-specific agricultural information:

- **PlantVillage Dataset:** A large, open-source repository of images of healthy and diseased plant leaves.
- **PlantDoc Dataset:** Another significant collection of plant disease images, with specific relevance to the Indian agricultural context.

By merging and de-duplicating these datasets, a definitive list of 46 distinct plant-disease classes was established, with a focus on crops and conditions relevant to our six target states. The folder names from this dataset (e.g., `Tomato___Late_blight`) provided the foundational checklist of diseases the system needed to address. The images themselves were reserved to serve as the unbiased test set for the final evaluation phase, with additional validation from agricultural experts in each pilot state.

## 3. Data Curation Methodology: An Iterative Engineering Process

The core task was to create a structured knowledge base (`knowledge_base_v0_generic_46-class.csv`) containing accurate symptoms and remedy information for each of the 46 disease classes. An iterative process involving three distinct methods was undertaken.

### Method 1: Automated Web Scraping (Attempt and Failure)

The initial hypothesis was that the knowledge base could be constructed automatically by scraping information from authoritative websites.

**Tools:** Python, requests, BeautifulSoup4, googlesearch-python.

**Process:** A script was developed to iterate through the disease list, perform targeted Google searches prioritizing authoritative domains (e.g., icar.gov.in), and scrape text content from the top-ranking pages.

**Challenges & Reasons for Rejection:**
- **Structural Inconsistency:** Public and academic websites have highly variable HTML structures, making it impossible for a single scraper to reliably extract data.
- **Content Format Barriers:** A significant portion of high-quality information is embedded in .pdf documents, which are not parsable by a standard HTML scraping library.
- **Low-Quality Output:** The resulting dataset was incomplete, filled with errors, garbled text, and "Scraping failed" messages, rendering it unusable.

**Conclusion:** It was determined that simple web scraping was too brittle and unreliable to meet the project's quality standards.

### Method 2: Generative AI with Gemma 3n (Attempt and Failure)

The second approach involved leveraging the project's core AI model, Gemma 3n, to generate the knowledge base content.

**Tools:** Python, transformers, torch, Gemma 3n.

**Process:** A script was created to prompt Gemma 3n with a specific instruction for each disease, asking it to act as an agricultural scientist and provide structured Symptoms and Remedy information.

**Challenges & Reasons for Rejection:**
- **Formatting Inconsistency:** While the generated text was articulate, the model did not always adhere strictly to the requested format, causing the simple parsing logic to fail and resulting in "Not found" entries.
- **Lack of Source Verifiability:** The model, by its nature, does not cite its sources. While the generated information may have been factually correct, its origin could not be verified. This directly violated the project's core principle of building a transparent and trustworthy system.

**Conclusion:** A purely generative approach, while faster, lacked the structural consistency and source verifiability necessary for a high-stakes, real-world application.

### Method 3: Expert-Led Curation with AI-Powered Research (The Chosen Approach)

The failures of the automated methods led to the final, successful strategy: a professional, hybrid approach that combines the power of advanced AI for research with the precision of human expertise for verification.

**Tools:** Google Gemini 2.5 Pro (Deep Research Functionality), Human Expertise, Spreadsheet Software.

**Process:**
1. **AI-Powered Research:** The Project Owner utilized the advanced research capabilities of a state-of-the-art model (Gemini 2.5 Pro) to synthesize information from multiple authoritative sources, including academic papers and PDFs, for each of the 46 diseases.
2. **Human-in-the-Loop (HITL) Verification:** The AI-synthesized information was not accepted blindly. The Project Owner performed the critical role of a human expert, meticulously reviewing the generated text for factual accuracy, clarity, and relevance to the Indian agricultural context.
3. **Manual Curation:** This verified and refined information was then manually structured and compiled into the final `knowledge_base_v0_generic_46-class.csv` file, ensuring perfect formatting and data integrity.

## 4. Justification for the Final Methodology

The expert-led curation approach was chosen because it was the only method that successfully overcame the limitations of the others and met the project's stringent quality requirements.

- **It Ensures Trust:** By manually verifying every piece of information and citing authoritative sources, the resulting knowledge base is not a "black box." Its reliability is transparent and can be audited.
- **It Captures Nuance:** The human-led process allowed for the inclusion of strategic depth, such as the principles of Integrated Disease Management (IDM), which prioritizes cultural and biological controls—a level of sophistication that automation failed to achieve.
- **It Is Robust:** The final `knowledge_base_v0_generic_46-class.csv` is clean, complete, and correctly formatted, providing a solid foundation for the project's RAG system.

## 5. Conclusion

The journey to create the project's knowledge base underscores a critical lesson in applied AI: for high-stakes, real-world applications, data quality and trustworthiness are paramount. The initial attempts at full automation failed to meet the required standards of accuracy and verifiability. The final, successful methodology was a hybrid, Human-in-the-Loop approach that leveraged powerful AI for efficient research and human expertise for the critical tasks of verification and curation. This ensures that the foundation of KrishiSahayak+Gemma is not just data, but trusted, actionable knowledge.