import streamlit.cli as stcli
import sys
import os

if __name__ == "__main__":
    # Add the project root directory to the Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Run the Streamlit app
    sys.argv = ["streamlit", "run", "src/web/app.py"]
    sys.exit(stcli.main()) 