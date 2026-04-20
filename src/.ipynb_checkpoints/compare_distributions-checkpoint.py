import os 
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.compare_mfccs import compute_directory_transformed_skld


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_distributions.py <directory1> <directory_2")
        sys.exit(1)

    directory1 = sys.argv[1]
    directory2 = sys.argv[2]

    avg_tskld = compute_directory_transformed_skld(directory1, directory2)

    print(f"Average T-SKLD between the two directories: {avg_tskld}")

