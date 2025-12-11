#!/usr/bin/env python
"""
Script to reset the Chroma database and reingest all data.
Run this once to clear old data and rebuild with new metadata.
"""

import os
import shutil
from ingest import build_vectorstore

PERSIST_DIR = "chroma_db"

def reset_database():
    """Delete the old Chroma database."""
    if os.path.exists(PERSIST_DIR):
        print(f"🗑️  Deleting old database at '{PERSIST_DIR}'...")
        shutil.rmtree(PERSIST_DIR)
        print("✅ Old database deleted")
    else:
        print(f"ℹ️  No existing database found at '{PERSIST_DIR}'")

def main():
    print("🔄 RESET & REINGEST WORKFLOW")
    print("=" * 50)
    
    # Step 1: Reset
    reset_database()
    
    # Step 2: Reingest
    print("\n📥 Starting fresh ingestion...")
    build_vectorstore()
    
    print("\n" + "=" * 50)
    print("✅ COMPLETE! Database is ready to use.")
    print(f"📁 New data stored in '{PERSIST_DIR}'")

if __name__ == "__main__":
    main()
