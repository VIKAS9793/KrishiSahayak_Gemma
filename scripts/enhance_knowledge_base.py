#!/usr/bin/env python3
"""
enhance_knowledge_base.py

Script to enhance missing data and validate existing information in the knowledge base.
"""

import pandas as pd
from pathlib import Path
import json
from datetime import datetime

# File paths
PROJECT_ROOT = Path(__file__).parent.parent
KNOWLEDGE_BASE = PROJECT_ROOT / "data" / "processed" / "final_knowledge_base.csv"
ENHANCED_KB = PROJECT_ROOT / "data" / "processed" / "enhanced_knowledge_base.csv"
VALIDATION_REPORT = PROJECT_ROOT / "reports" / "data_validation_report.md"
ENHANCEMENTS_FILE = PROJECT_ROOT / "data" / "enhancements" / "disease_enhancements.json"

# Create necessary directories
ENHANCED_KB.parent.mkdir(parents=True, exist_ok=True)
VALIDATION_REPORT.parent.mkdir(parents=True, exist_ok=True)
ENHANCEMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load enhancement data (if exists)
enhancements = {}
if ENHANCEMENTS_FILE.exists():
    with open(ENHANCEMENTS_FILE, 'r', encoding='utf-8') as f:
        enhancements = json.load(f)

def load_knowledge_base():
    """Load the knowledge base and return a DataFrame."""
    return pd.read_csv(KNOWLEDGE_BASE)

def validate_data(df):
    """Validate the knowledge base data and generate a report."""
    report = []
    report.append("# Data Validation Report")
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Basic stats
    total = len(df)
    complete = df[df['has_details']].shape[0]
    incomplete = total - complete
    
    report.append("## Summary")
    report.append(f"- Total diseases: {total}")
    report.append(f"- Complete entries: {complete} ({(complete/total)*100:.1f}%)")
    report.append(f"- Incomplete entries: {incomplete} ({(incomplete/total)*100:.1f}%)")
    
    # Check for missing values
    report.append("\n## Data Quality Checks")
    
    # 1. Check for missing symptoms or remedies in complete entries
    complete_df = df[df['has_details']]
    missing_symptoms = complete_df[complete_df['symptoms'].str.lower().isin(['not specified', 'none', ''])]
    missing_remedies = complete_df[complete_df['remedy'].str.lower().isin(['not specified', 'none', ''])]
    
    report.append("### Missing Data in Complete Entries")
    if not missing_symptoms.empty:
        report.append("⚠️ The following complete entries are missing symptoms:")
        for _, row in missing_symptoms.iterrows():
            report.append(f"   - {row['plant']} - {row['disease']}")
    else:
        report.append("✅ All complete entries have symptom information.")
    
    if not missing_remedies.empty:
        report.append("\n⚠️ The following complete entries are missing remedies:")
        for _, row in missing_remedies.iterrows():
            report.append(f"   - {row['plant']} - {row['disease']}")
    else:
        report.append("\n✅ All complete entries have remedy information.")
    
    # 2. List incomplete entries
    incomplete_df = df[~df['has_details']]
    report.append("\n## Incomplete Entries")
    if not incomplete_df.empty:
        report.append("The following entries are missing detailed information:")
        for _, row in incomplete_df.iterrows():
            report.append(f"- {row['plant']} - {row['disease']}")
    else:
        report.append("✅ All entries have complete information!")
    
    # 3. Data quality suggestions
    report.append("\n## Data Quality Suggestions")
    report.append("1. Review and enhance the incomplete entries listed above.")
    report.append("2. Add more detailed descriptions for symptoms and remedies where possible.")
    report.append("3. Include sources for all information to ensure traceability.")
    
    # Save report
    with open(VALIDATION_REPORT, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print(f"✅ Validation report saved to: {VALIDATION_REPORT}")
    return report

def enhance_data(df):
    """Enhance the knowledge base with additional data."""
    print("🔍 Enhancing knowledge base data...")
    
    # Create a copy to avoid modifying the original
    enhanced_df = df.copy()
    
    # Apply any saved enhancements
    if enhancements:
        print(f"Applying {len(enhancements)} saved enhancements...")
        for disease_name, enhancement in enhancements.items():
            # Convert to standard format if needed
            std_name = disease_name.replace(' ', '_')
            mask = enhanced_df['disease_name'] == std_name
            
            if not mask.any():
                # Try alternative formatting
                alt_name = disease_name.replace('_', ' ').replace('  ', ' ').strip()
                alt_std_name = alt_name.replace(' ', '_')
                mask = enhanced_df['disease_name'] == alt_std_name
            
            if mask.any():
                print(f"Enhancing: {std_name}")
                for key, value in enhancement.items():
                    if key in enhanced_df.columns:
                        enhanced_df.loc[mask, key] = value
                enhanced_df.loc[mask, 'has_details'] = True
                enhanced_df.loc[mask, 'source'] = 'Enhanced with additional data'
    
    # Add any new enhancements here programmatically
    # Example:
    # enhanced_df.loc[enhanced_df['disease_name'] == 'Apple___Apple_Scab', 'symptoms'] = 'Updated symptoms...'
    # enhanced_df.loc[enhanced_df['disease_name'] == 'Apple___Apple_Scab', 'remedy'] = 'Updated remedy...'
    
    # Save enhanced knowledge base
    enhanced_df.to_csv(ENHANCED_KB, index=False)
    print(f"✅ Enhanced knowledge base saved to: {ENHANCED_KB}")
    
    return enhanced_df

def main():
    # Load the knowledge base
    print("📊 Loading knowledge base...")
    df = load_knowledge_base()
    
    # Validate the data
    print("\n🔍 Validating data...")
    validate_data(df)
    
    # Enhance the data
    enhanced_df = enhance_data(df)
    
    # Show summary
    total = len(enhanced_df)
    complete = enhanced_df['has_details'].sum()
    
    print("\n📊 Enhanced Knowledge Base Summary:")
    print(f"- Total diseases: {total}")
    print(f"- Complete entries: {complete} ({(complete/total)*100:.1f}%)")
    print(f"- Incomplete entries: {total - complete} ({((total - complete)/total)*100:.1f}%)")
    
    print("\n✅ Process completed!")
    print(f"- Validation report: {VALIDATION_REPORT}")
    print(f"- Enhanced knowledge base: {ENHANCED_KB}")

if __name__ == "__main__":
    main()
