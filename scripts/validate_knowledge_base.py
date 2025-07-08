#!/usr/bin/env python3
"""
Knowledge Base Validation Script

This script performs comprehensive validation of the agricultural knowledge base,
including data quality checks, coverage analysis, and statistical insights.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class KnowledgeBaseValidator:
    """Class to validate the agricultural knowledge base."""
    
    def __init__(self, data_dir: str = "data/processed"):
        """Initialize the validator with data directory."""
        self.project_root = Path(__file__).resolve().parent.parent
        self.data_dir = self.project_root / data_dir
        self.reports_dir = self.project_root / "reports"
        self.results_dir = self.reports_dir / "validation_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Data storage
        self.df = None
        self.validation_results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {},
            "data_quality": {},
            "coverage": {},
            "issues": []
        }
    
    def load_data(self) -> None:
        """Load and preprocess the knowledge base data."""
        try:
            kb_path = self.data_dir / "knowledge_base.csv"
            self.df = pd.read_csv(kb_path)
            logger.info(f"Loaded knowledge base with {len(self.df)} entries.")
            
            # Basic preprocessing
            self.df = self.df.replace({np.nan: None})
            
            # Add text length metrics
            self.df['symptoms_length'] = self.df['symptoms'].apply(
                lambda x: len(str(x).split()) if x else 0
            )
            self.df['remedy_length'] = self.df['remedy'].apply(
                lambda x: len(str(x).split()) if x else 0
            )
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def check_completeness(self) -> Dict:
        """Check for missing values in required fields."""
        required_columns = ['plant', 'disease', 'symptoms', 'remedy', 'source']
        completeness = {}
        
        for col in required_columns:
            if col in self.df.columns:
                null_count = self.df[col].isnull().sum()
                completeness[col] = {
                    'missing': int(null_count),
                    'completeness': 1 - (null_count / len(self.df)),
                    'status': '✅' if null_count == 0 else '⚠️'
                }
        
        self.validation_results['data_quality']['completeness'] = completeness
        return completeness
    
    def analyze_coverage(self) -> Dict:
        """Analyze coverage of diseases and crops."""
        coverage = {
            'total_diseases': len(self.df),
            'crops': {},
            'disease_status': {}
        }
        
        # Crop coverage
        crop_counts = self.df['plant'].value_counts().to_dict()
        coverage['total_crops'] = len(crop_counts)
        coverage['crops'] = crop_counts
        
        # Disease status (complete/incomplete)
        complete_threshold = 10  # Minimum words for symptoms and remedies
        self.df['is_complete'] = (
            (self.df['symptoms_length'] >= complete_threshold) &
            (self.df['remedy_length'] >= complete_threshold)
        )
        
        status = self.df['is_complete'].value_counts().to_dict()
        coverage['disease_status'] = {
            'complete': status.get(True, 0),
            'incomplete': status.get(False, 0)
        }
        
        self.validation_results['coverage'] = coverage
        return coverage
    
    def check_data_quality(self) -> Dict:
        """Perform various data quality checks."""
        quality_checks = {
            'duplicates': {
                'count': int(self.df.duplicated().sum()),
                'status': '✅' if not self.df.duplicated().any() else '⚠️'
            },
            'text_lengths': {
                'min_symptoms': int(self.df['symptoms_length'].min()),
                'avg_symptoms': float(self.df['symptoms_length'].mean().round(2)),
                'max_symptoms': int(self.df['symptoms_length'].max()),
                'min_remedy': int(self.df['remedy_length'].min()),
                'avg_remedy': float(self.df['remedy_length'].mean().round(2)),
                'max_remedy': int(self.df['remedy_length'].max())
            }
        }
        
        self.validation_results['data_quality']['quality_checks'] = quality_checks
        return quality_checks
    
    def generate_visualizations(self) -> None:
        """Generate visualizations for the validation report."""
        # Set style
        sns.set_theme(style="whitegrid")
        
        # 1. Disease status pie chart
        plt.figure(figsize=(8, 6))
        status_counts = self.df['is_complete'].value_counts()
        plt.pie(
            status_counts,
            labels=['Complete' if x else 'Incomplete' for x in status_counts.index],
            autopct='%1.1f%%',
            startangle=90,
            colors=['#4CAF50', '#FFC107']
        )
        plt.title('Disease Entry Completeness')
        plt.savefig(self.results_dir / 'completeness_pie.png', bbox_inches='tight')
        plt.close()
        
        # 2. Symptoms and Remedy length distribution
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        sns.histplot(self.df['symptoms_length'], bins=20, color='#2196F3')
        plt.title('Symptoms Length Distribution')
        plt.xlabel('Word Count')
        
        plt.subplot(1, 2, 2)
        sns.histplot(self.df['remedy_length'], bins=20, color='#9C27B0')
        plt.title('Remedy Length Distribution')
        plt.xlabel('Word Count')
        
        plt.tight_layout()
        plt.savefig(self.results_dir / 'length_distributions.png')
        plt.close()
    
    def generate_report(self) -> str:
        """Generate a comprehensive validation report in Markdown format."""
        report = "# 🛠️ Knowledge Base Validation Report\n\n"
        
        # Header
        report += f"**Generated on:** {self.validation_results['timestamp']}  \n"
        report += f"**Total Entries:** {len(self.df)}  \n"
        
        # Summary
        report += "## 📋 Executive Summary\n\n"
        complete = self.validation_results['coverage']['disease_status']['complete']
        total = len(self.df)
        report += f"- ✅ **Complete Entries:** {complete} ({(complete/total)*100:.1f}%)\n"
        report += f"- ⚠️ **Incomplete Entries:** {total - complete} ({(1 - complete/total)*100:.1f}%)\n"
        report += f"- 🌱 **Crops Covered:** {self.validation_results['coverage']['total_crops']}\n"
        # Data Quality
        report += "## 🔍 Data Quality Assessment\n\n"
        report += "### Completeness Check\n"
        for field, stats in self.validation_results['data_quality']['completeness'].items():
            report += (
                f"- {stats['status']} **{field.capitalize()}**: "
                f"{stats['completeness']*100:.1f}% complete "
                f"({stats['missing']} missing)\n"
            )
        
        # Coverage
        report += "\n### Coverage Analysis\n\n"
        report += f"#### Crops Coverage ({self.validation_results['coverage']['total_crops']} total)\n"
        for crop, count in sorted(
            self.validation_results['coverage']['crops'].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            report += f"- {crop}: {count} diseases\n"
        
        # Visualizations
        report += "\n## 📊 Visualizations\n\n"
        report += "### Entry Completeness\n"
        report += "![Completeness Pie Chart](validation_results/completeness_pie.png)\n\n"
        
        report += "### Text Length Distributions\n"
        report += "![Length Distributions](validation_results/length_distributions.png)\n\n"
        
        # Recommendations
        report += "## 🚀 Recommendations\n\n"
        report += "1. **Complete Missing Data**\n"
        report += "   - Focus on entries with incomplete symptoms or remedies\n"
        report += "   - Add source attribution for all entries\n\n"
        
        report += "2. **Enhance Data Quality**\n"
        report += "   - Standardize text formatting\n"
        report += "   - Add more detailed descriptions where possible\n\n"
        
        report += "3. **Expand Coverage**\n"
        report += "   - Add more crops and diseases\n"
        report += "   - Include regional variations and local names\n"
        # Save the report
        report_path = self.reports_dir / 'knowledge_base_validation_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Validation report generated at: {report_path}")
        return report
    
    def run(self) -> None:
        """Run the complete validation pipeline."""
        try:
            logger.info("Starting knowledge base validation...")
            self.load_data()
            self.check_completeness()
            self.analyze_coverage()
            self.check_data_quality()
            self.generate_visualizations()
            self.generate_report()
            logger.info("Validation completed successfully!")
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            raise

if __name__ == "__main__":
    validator = KnowledgeBaseValidator()
    validator.run()
