import sys
sys.path.insert(0, ".")
from app import generar_visor_3d_pelvis

def test_modulo_c_viewer():
    print("Testing Módulo C (Atlas Mode) 3D Viewer HTML output...")
    
    presets = ['pi', 'as', 'up', 'down', 'outflare', 'inflare', 'torsion_ant', 'torsion_post']
    sides = ['Derecho', 'Izquierdo']
    
    for p in presets:
        for s in sides:
            html = generar_visor_3d_pelvis(
                preset_inicial=p,
                lado_inicial=s,
                es_modo_atlas=True,
                mostrar_ficha_didactica=False,
                altura_canvas=850
            )
            
            # 1. Embedded selectors MUST NOT be present
            assert "id=\"atlas-category-select\"" not in html, f"Failed: atlas-category-select found for preset {p}"
            assert "id=\"atlas-dysfunction-select\"" not in html, f"Failed: atlas-dysfunction-select found for preset {p}"
            assert "id=\"side-btn-d\"" not in html, f"Failed: side-btn-d found for preset {p}"
            assert "id=\"side-btn-i\"" not in html, f"Failed: side-btn-i found for preset {p}"
            
            # 2. Preset shortcut buttons subtoolbar MUST NOT be present
            assert "class=\"preset-subtoolbar\"" not in html, f"Failed: preset-subtoolbar found for preset {p}"
            assert "btn-preset-pi" not in html, f"Failed: btn-preset-pi found for preset {p}"
            assert "btn-preset-as" not in html, f"Failed: btn-preset-as found for preset {p}"
            assert "btn-preset-up" not in html, f"Failed: btn-preset-up found for preset {p}"
            assert "btn-preset-down" not in html, f"Failed: btn-preset-down found for preset {p}"
            assert "btn-preset-outflare" not in html, f"Failed: btn-preset-outflare found for preset {p}"
            assert "btn-preset-inflare" not in html, f"Failed: btn-preset-inflare found for preset {p}"
            assert "btn-preset-torsion_ant" not in html, f"Failed: btn-preset-torsion_ant found for preset {p}"
            assert "btn-preset-torsion_post" not in html, f"Failed: btn-preset-torsion_post found for preset {p}"
            
            # 3. Patient case button MUST NOT be present in Modulo C
            assert "id=\"btn-dysfunction\"" not in html, f"Failed: btn-dysfunction found in Modulo C for preset {p}"
            
            # 4. View and model controls MUST be present
            assert "id=\"btn-neutral\"" in html, f"Failed: btn-neutral missing for preset {p}"
            assert "id=\"btn-gait\"" in html, f"Failed: btn-gait missing for preset {p}"
            assert "id=\"btn-toggle-landmarks\"" in html, f"Failed: btn-toggle-landmarks missing for preset {p}"
            assert "id=\"btn-toggle-lines\"" in html, f"Failed: btn-toggle-lines missing for preset {p}"
            assert "id=\"glbFileInput\"" in html, f"Failed: glbFileInput missing for preset {p}"
            
            # 5. Injection of preset, side, and toggleNeutral
            assert f'let currentPatientSide = "{s}";' in html, f"Failed: currentPatientSide incorrect for side {s}"
            assert f'let currentActivePreset = "{p}";' in html, f"Failed: currentActivePreset incorrect for preset {p}"
            assert f'const baseActivePreset = "{p}";' in html, f"Failed: baseActivePreset incorrect for preset {p}"
            assert "function toggleNeutral()" in html, "Failed: toggleNeutral function missing"
            
    print("[SUCCESS] Modulo C Atlas Viewer passes all redundancy removal and control retention tests!")

def test_modulo_a_viewer():
    print("Testing Módulo A (Clinical Case Mode) 3D Viewer HTML output...")
    html = generar_visor_3d_pelvis(
        es_modo_atlas=False,
        altura_canvas=850
    )
    # Modulo A MUST have btn-dysfunction (Paciente) and btn-neutral (Neutro)
    assert "id=\"btn-dysfunction\"" in html, "Failed: btn-dysfunction missing in Modulo A"
    assert "id=\"btn-neutral\"" in html, "Failed: btn-neutral missing in Modulo A"
    assert "id=\"btn-gait\"" in html, "Failed: btn-gait missing in Modulo A"
    assert "id=\"btn-toggle-landmarks\"" in html, "Failed: btn-toggle-landmarks missing in Modulo A"
    assert "id=\"btn-toggle-lines\"" in html, "Failed: btn-toggle-lines missing in Modulo A"
    assert "id=\"glbFileInput\"" in html, "Failed: glbFileInput missing in Modulo A"
    
    # Modulo A MUST NOT have atlas selectors or preset subtoolbar
    assert "id=\"atlas-category-select\"" not in html
    assert "class=\"preset-subtoolbar\"" not in html
    print("[SUCCESS] Modulo A viewer passes all tests!")

if __name__ == "__main__":
    test_modulo_c_viewer()
    test_modulo_a_viewer()
    print("ALL TESTS PASSED SUCCESSFULLY!")
