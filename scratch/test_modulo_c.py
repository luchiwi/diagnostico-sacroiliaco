from streamlit.testing.v1 import AppTest

def test_app_py_modulo_c():
    at = AppTest.from_file("../app.py", default_timeout=30)
    at.query_params["tab"] = "c"
    at.run()
    assert not at.exception, f"Exception in app.py with tab=c: {at.exception}"
    print("app.py tab=c loaded successfully without errors!")

def test_streamlit_app_py_modulo_c():
    at = AppTest.from_file("../streamlit_app.py", default_timeout=30)
    at.query_params["tab"] = "c"
    at.run()
    assert not at.exception, f"Exception in streamlit_app.py with tab=c: {at.exception}"
    print("streamlit_app.py tab=c loaded successfully without errors!")

if __name__ == "__main__":
    test_app_py_modulo_c()
    test_streamlit_app_py_modulo_c()
    print("ALL TESTS PASSED WITH 0 EXCEPTIONS!")
