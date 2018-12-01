#!/usr/bin/python3
import os
from configparser import ConfigParser, ExtendedInterpolation

CLUSTER_CONFIG = dict()
LOG = dict()


def pull(config_filename, username):
    CLUSTER_CONFIG = load_config(config_filename)
    deploy_dir = CLUSTER_CONFIG["all:vars"]["deploy_dir"]
    for s in CLUSTER_CONFIG["tidb_servers"].keys():
        os.system("scp {}@{}:{}/log/tidb.log {}-tidb.log"
                  .format(username, s, deploy_dir, s))
    for s in CLUSTER_CONFIG["pd_servers"].keys():
        os.system("scp {}@{}:{}/log/pd.log {}-pd.log"
                  .format(username, s, deploy_dir, s))
    for s in CLUSTER_CONFIG["tikv_servers"].items():
        v = s[1].split()
        os.system("scp {}@{}:{}/log/tikv.log {}-tikv.log"
                  .format(username, v[0], v[1][11:], s[0].split()[0]))


def load_config(filename):
    f = open(filename, "r")
    parser = ConfigParser(
        interpolation=ExtendedInterpolation(),
        allow_no_value=True
    )
    parser.read_string(f.read())
    return parser


if __name__ == "__main__":
    pull("inventory.ini", "pingcap")
