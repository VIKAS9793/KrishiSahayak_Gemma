# asset_preparation/create_database.py
"""
Creates a production-ready, portable SQLite database from the knowledge base CSV.

Purpose:
- To convert the CSV data into a structured, efficient, and offline-first format.
- This SQLite file will be bundled directly into the Android application's assets.
- Using a database allows for fast, indexed queries on the device without
  loading the entire dataset into memory.

Run standalone during the asset build process:
`python asset_preparation/create_database.py`
"""

import pandas as pd
import sqlite3
import logging
import os
from pathlib import Path

# --- Configuration ---
# Setup professional logging to monitor the script's execution.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define project paths relative to this script's location.
# This ensures the script can be run from anywhere.
try:
    # Assuming this script is in asset_preparation/
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    INPUT_CSV_PATH = PROJECT_ROOT / "data" / "knowledge_base.csv"
    
    # Define the output directory for all prepared assets.
    OUTPUT_DIR = PROJECT_ROOT / "android_app" / "src" / "main" / "assets"
    OUTPUT_DB_PATH = OUTPUT_DIR / "knowledge_base.sqlite"

    # Create the output directory if it doesn't exist.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
except Exception as e:
    logger.error(f"Error setting up file paths: {e}")
    # Exit if paths can't be resolved, as nothing else will work.
    exit(1)


def create_db_from_csv(csv_path: Path, db_path: Path):
    """
    Reads data from a CSV file and writes it to a clean SQLite database.

    Args:
        csv_path (Path): The path to the input knowledge_base.csv file.
        db_path (Path): The path where the output knowledge_base.sqlite will be saved.
    """
    if not csv_path.exists():
        logger.error(f"Input file not found at: {csv_path}")
        return

    logger.info(f"Reading data from {csv_path}...")
    try:
        df = pd.read_csv(csv_path)

        # --- Data Cleaning & Validation ---
        # Ensure column names are clean (no spaces, lowercase) for DB compatibility.
        df.columns = [col.strip().lower() for col in df.columns]
        
        # We expect specific columns from your CSV.
        expected_cols = {'disease_name', 'symptoms', 'remedy'}
        if not expected_cols.issubset(df.columns):
            logger.error(f"CSV is missing required columns. Expected at least: {expected_cols}")
            return
            
    except Exception as e:
        logger.error(f"Failed to read or process CSV: {e}")
        return

    logger.info("Connecting to SQLite database and writing data...")
    try:
        # The 'with' statement ensures the connection is closed automatically.
        with sqlite3.connect(db_path) as conn:
            # Write the DataFrame to a table named 'knowledge'.
            # 'if_exists='replace'' ensures we start fresh each time we build assets.
            df.to_sql('knowledge', conn, if_exists='replace', index=False)
        
        logger.info(f"✅ Successfully created database with {len(df)} records.")
        logger.info(f"SQLite database saved to: {db_path}")

    except sqlite3.Error as e:
        logger.error(f"An error occurred with the SQLite database: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during database creation: {e}")


if __name__ == "__main__":
    logger.info("--- Starting Knowledge Base to SQLite Conversion ---")
    create_db_from_csv(INPUT_CSV_PATH, OUTPUT_DB_PATH)
    logger.info("--- ✅ Database creation process finished. ---")