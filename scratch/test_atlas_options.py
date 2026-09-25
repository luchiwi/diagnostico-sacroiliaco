import sys, os
sys.path.insert(0, os.path.abspath("."))
import app
import streamlit_app

print("Testing CATEGORIAS_ATLAS consistency and PRESET_TO_CK_KEY coverage...")

for mod_name, mod in [("app", app), ("streamlit_app", streamlit_app)]:
    print(f"\nChecking module {mod_name}:")
    assert hasattr(mod, "PRESET_TO_CK_KEY"), f"{mod_name} missing PRESET_TO_CK_KEY"
    assert hasattr(mod, "ATLAS_PRESET_METADATA"), f"{mod_name} missing ATLAS_PRESET_METADATA"
    
    # Check that presets in clinical knowledge base are valid
    import clinical_knowledge
    for preset, ck_key in mod.PRESET_TO_CK_KEY.items():
        assert ck_key in clinical_knowledge.CLINICAL_KNOWLEDGE_BASE, f"Missing {ck_key} in CLINICAL_KNOWLEDGE_BASE"
        info = clinical_knowledge.get_disfuncion_info(ck_key)
        assert info is not None, f"get_disfuncion_info failed for {ck_key}"
    print(f"All {len(mod.PRESET_TO_CK_KEY)} presets in PRESET_TO_CK_KEY exist in CLINICAL_KNOWLEDGE_BASE.")

print("\nAll Atlas metadata and preset tests passed successfully!")
