from dash_app_2.app.config import load_config

try:
    CONFIG = load_config()
except:
    print("NO DASH APP CONFIG FOUND")