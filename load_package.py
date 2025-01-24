import sys
import importlib

def load_topsis_package():
    try:
        # Package name must match the installed package
        package_name = 'Topsis-Vansh-102203021'
        print(f"Attempting to import: {package_name}")
        
        # Dynamically import the package
        topsis_module = importlib.import_module(package_name)
        print(f"Successfully imported {package_name}")
        
        # Check if the required function exists in the package
        if hasattr(topsis_module, 'topsis'):
            return topsis_module.topsis
        else:
            raise ImportError(f"'calculate_topsis' not found in {package_name}")
    except ImportError as e:
        raise ImportError(f"Error importing the TOPSIS package: {e}")

# Load the package and assign the function
calculate_topsis = load_topsis_package()
