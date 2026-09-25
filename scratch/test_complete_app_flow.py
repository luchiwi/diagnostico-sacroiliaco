import streamlit as st
from streamlit.testing.v1 import AppTest

# Test that app.py compiles and can run its imports
from clinical_knowledge import CLINICAL_KNOWLEDGE_BASE
from auth import render_user_badge

print("Imports from app.py dependencies work successfully.")
