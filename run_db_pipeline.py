"""
Database Pipeline Runner
Executes the MySQL database approach for data processing
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from db_approach.main import main

if __name__ == "__main__":
    main()
