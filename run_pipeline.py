
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))

# Import and run main
from inmemory_approach.main import main

if __name__ == "__main__":
    main()
