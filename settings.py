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
    "port": 19092,
    "base_path": BASE_DIR,
    "template_path": TEMPLATE_DIR,
    "static_path": STATIC_DIR,
    "salt_length": 12,
    "cluster_config": os.path.join(CONFIG_DIR, 'inventory.ini'),
    "data_dir": DATA_DIR,
    "remote_username": "pingcap",
    "pd_host": "172.16.30.38",
    "pd_port": "13379",
    "tidb_host": "172.16.30.38",
    "tidb_port": "10083",
    "prometheus_host": "192.168.199.118",
    "prometheus_port": "9090",
}
