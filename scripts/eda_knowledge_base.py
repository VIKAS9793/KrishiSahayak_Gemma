# eda_knowledge_base_v2.py
"""
Exploratory Data Analysis (EDA) for Agricultural Knowledge Base

This script performs a comprehensive, production-grade EDA on the agricultural 
knowledge base dataset, adhering to high standards for code quality, robustness,
and maintainability.

Key Features:
- Object-oriented design for better structure and state management.
- Configuration managed via a dedicated class.
- Robust logging for clear, level-based output.
- Comprehensive data quality assessment.
- Detailed statistical and text-based analysis.
- High-quality visualizations saved to a structured output directory.
- Automated generation of a detailed Markdown report.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import logging
from pathlib import Path
from typing import Dict, List, Optional

# --- Step 1: Setup Professional Logging ---
# A production script should use logging instead of print() for better control.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Step 2: Centralized Configuration ---
# Encapsulates all paths and settings in one place for easy management.
class Config:
    """Configuration class for the EDA script."""
    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            # Assumes the script is in a 'scripts' or similar directory
            self.project_root = Path(__file__).resolve().parent.parent
        else:
            self.project_root = base_dir

        self.data_dir = self.project_root / "data" / "raw"
        self.input_csv = self.data_dir / "knowledge_base.csv"
        
        self.reports_dir = self.project_root / "reports"
        self.output_dir = self.reports_dir / "eda_results"
        self.report_path = self.reports_dir / "knowledge_base_eda_report.md"

        # Create directories if they don't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Visualization settings
        sns.set(style="whitegrid", font_scale=1.2)
        plt.rcParams['figure.figsize'] = (14, 8)
        plt.rcParams['figure.dpi'] = 300

# --- Step 3: Object-Oriented Analyzer ---
# Encapsulates data and methods for a cleaner, more maintainable structure.
class EDAAnalyzer:
    """A class to perform EDA on the knowledge base."""

    def __init__(self, config: Config):
        self.config = config
        self.df: Optional[pd.DataFrame] = None
        self.missing_df: Optional[pd.DataFrame] = None

    def load_data(self) -> bool:
        """Load the dataset from the processed data directory."""
        input_file = os.path.join('data', 'processed', 'knowledge_base.csv')
        logging.info(f"Loading data from: {os.path.abspath(input_file)}")
        
        if not os.path.exists(input_file):
            logging.error(f"Input file not found at {os.path.abspath(input_file)}")
            # Try alternative paths if the file is not found
            alternative_paths = [
                os.path.join('data', 'knowledge_base.csv'),
                os.path.join('knowledge_base.csv')
            ]
            
            for path in alternative_paths:
                if os.path.exists(path):
                    input_file = path
                    logging.info(f"Found data at alternative path: {os.path.abspath(input_file)}")
                    break
            else:
                logging.error("Could not find knowledge_base.csv in any expected location")
                return False
        
        try:
            self.df = pd.read_csv(input_file)
            # Basic preprocessing
            for col in self.df.select_dtypes(include=['object']).columns:
                self.df[col] = self.df[col].str.strip()
            self.df.replace({'': np.nan}, inplace=True)
            
            # Add text length features for analysis
            for col in ['symptoms', 'remedy']:
                if col in self.df.columns:
                    self.df[f'{col}_length'] = self.df[col].str.len().fillna(0).astype(int)
            
            # Extract plant from disease_name
            if 'disease_name' in self.df.columns:
                self.df['plant'] = self.df['disease_name'].apply(lambda x: x.split('___')[0] if '___' in x else 'Unknown')
            
            logging.info("Data loaded and preprocessed successfully.")
            return True
        except Exception as e:
            logging.error(f"Failed to load or process data: {e}")
            return False

    def assess_data_quality(self):
        """Perform and log a comprehensive data quality assessment."""
        if self.df is None:
            logging.warning("DataFrame not loaded. Skipping data quality assessment.")
            return

        logging.info("--- Starting Data Quality Assessment ---")
        logging.info(f"Dataset Shape: {self.df.shape[0]} records, {self.df.shape[1]} features.")
        
        # Missing values
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        self.missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
        missing_report = self.missing_df[self.missing_df['Missing Count'] > 0]
        if not missing_report.empty:
            logging.warning("Missing values found:\n" + missing_report.to_string())
        else:
            logging.info("No missing values found.")

        # Duplicate rows
        duplicates = self.df.duplicated().sum()
        logging.info(f"Found {duplicates} duplicate rows ({(duplicates/len(self.df))*100:.2f}%).")
        logging.info("--- Data Quality Assessment Complete ---")

    def analyze_categorical(self, column: str, top_n: int = 15):
        """Analyze and visualize a single categorical column."""
        if self.df is None or column not in self.df.columns:
            logging.warning(f"Column '{column}' not found. Skipping analysis.")
            return
            
        logging.info(f"Analyzing categorical column: '{column}'")
        value_counts = self.df[column].value_counts(dropna=False)
        
        plt.figure()
        plot_data = value_counts.head(top_n)
        plot_data.plot(kind='bar', color=sns.color_palette("viridis", len(plot_data)))
        plt.title(f'Top {top_n} Distribution of {column.replace("_", " ").title()}', fontsize=16, weight='bold')
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        save_path = self.config.output_dir / f'{column}_distribution.png'
        plt.savefig(save_path)
        plt.close()
        logging.info(f"Saved visualization to {save_path}")

    def analyze_text(self, column: str):
        """Analyze and visualize a single text column."""
        if self.df is None or column not in self.df.columns or self.df[column].isna().all():
            logging.warning(f"Text column '{column}' not found or is empty. Skipping analysis.")
            return

        logging.info(f"Analyzing text column: '{column}'")
        lengths = self.df[f'{column}_length']
        
        # Plot length distribution
        plt.figure()
        sns.histplot(lengths, bins=50, kde=True, color='skyblue')
        plt.title(f'Distribution of {column.title()} Length (in characters)', fontsize=16, weight='bold')
        plt.xlabel('Number of Characters')
        plt.ylabel('Frequency')
        plt.tight_layout()
        save_path = self.config.output_dir / f'{column}_length_distribution.png'
        plt.savefig(save_path)
        plt.close()
        logging.info(f"Saved visualization to {save_path}")

        # Generate word cloud
        text = ' '.join(self.df[column].dropna().astype(str).values)
        if text.strip():
            wordcloud = WordCloud(width=1200, height=600, background_color='white', colormap='magma').generate(text)
            plt.figure(figsize=(15, 10))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Word Cloud for {column.title()}', fontsize=20, weight='bold')
            plt.tight_layout()
            save_path = self.config.output_dir / f'{column}_wordcloud.png'
            plt.savefig(save_path)
            plt.close()
            logging.info(f"Saved visualization to {save_path}")

    def generate_report(self):
        """Generate a comprehensive EDA report in Markdown format."""
        if self.df is None:
            logging.error("Cannot generate report without loaded data.")
            return

        logging.info(f"Generating EDA report at {self.config.report_path}")
        report_lines = ["# 🚜 KrishiSahayak Knowledge Base: EDA Report\n"]
        
        # Overview
        report_lines.append("## 1. Dataset Overview")
        report_lines.append(f"- **Total Records:** {self.df.shape[0]}")
        report_lines.append(f"- **Total Features:** {self.df.shape[1]}")
        report_lines.append("\n### Data Snippet")
        report_lines.append(self.df.head().to_markdown(index=False))

        # Data Quality
        report_lines.append("\n## 2. Data Quality Assessment")
        if self.missing_df is not None and not self.missing_df[self.missing_df['Missing Count'] > 0].empty:
            report_lines.append("### Missing Values")
            report_lines.append(self.missing_df[self.missing_df['Missing Count'] > 0].to_markdown())
        else:
            report_lines.append("✅ No missing values found.")
        
        duplicates = self.df.duplicated().sum()
        report_lines.append(f"\n### Duplicate Records\n- **Total Duplicates:** {duplicates}")

        # Analysis Sections and Visualizations
        report_lines.append("\n## 3. Analysis and Visualizations")
        for file in sorted(self.config.output_dir.glob('*.png')):
            title = file.stem.replace('_', ' ').title()
            relative_path = os.path.join("eda_results", file.name)
            report_lines.append(f"\n### {title}")
            report_lines.append(f"![{title}]({relative_path})")

        with open(self.config.report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        logging.info("EDA report generation complete.")

    def run(self):
        """Execute the full EDA pipeline."""
        if not self.load_data():
            return
        
        self.assess_data_quality()
        self.analyze_categorical('plant')
        self.analyze_text('symptoms')
        self.analyze_text('remedy')
        self.generate_report()

# --- Step 4: Main Execution Block ---
# Clean, professional entry point.
if __name__ == "__main__":
    logging.info("--- Starting EDA Pipeline ---")
    config = Config()
    analyzer = EDAAnalyzer(config)
    analyzer.run()
    logging.info("--- EDA Pipeline Finished ---")
