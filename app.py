"""Backwards-compatible alias: `streamlit run app.py` still works.

The canonical Streamlit Community Cloud entry point is streamlit_app.py.
Calling main() (not just importing the module) ensures Streamlit reruns
execute the UI on every interaction.
"""
from streamlit_app import main

main()
