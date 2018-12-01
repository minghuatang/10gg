import os

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'template/').replace('\\', '/')
STATIC_DIR = os.path.join(BASE_DIR, 'static/').replace('\\', '/')
CONFIG_DIR = os.path.join(BASE_DIR, 'config/').replace('\\', '/')
DATA_DIR = os.path.join(BASE_DIR, 'data/').replace('\\', '/')

site_settings = {
    "debug": False,
    "cookie_secret": "d13a4dbd47f042ccb47169a2fdd5e789",
    "xsrf_cookies": False,
    "login_url": "/login",
    "autoescape": None,
    "port": 8000,
    "base_path": BASE_DIR,
    "template_path": TEMPLATE_DIR,
    "static_path": STATIC_DIR,
    "salt_length": 12,
    "cluster_config": os.path.join(CONFIG_DIR, 'inventory.ini'),
    "data_path": DATA_DIR,
    "remote_username": "pingcap"
}
