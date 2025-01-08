import os
import fitz

# Check if the static/ directory exists
static_dir = 'static/'
if not os.path.exists(static_dir):
    print(f"Error: {static_dir} does not exist")
    # Create the directory if it doesn't exist
    os.makedirs(static_dir)

# Try importing the fitz library again
try:
    import fitz
except ImportError as e:
    print(f"Error: {e}")