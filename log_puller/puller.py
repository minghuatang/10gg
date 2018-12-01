#!/usr/bin/python3
import os
from settings import site_settings
from configparser import ConfigParser, ExtendedInterpolation

def pull():
    config_filename = site_settings['cluster_config']
    cluster_config = {}
    cluster_config = load_config(config_filename)
    username = site_settings['remote_username']
    data_dir = site_settings['data_dir']
    deploy_dir = cluster_config["all:vars"]["deploy_dir"]
    for k in cluster_config["tidb_servers"].keys():
        os.system("scp {}@{}:{}/log/tidb.log {}/{}-tidb.log"
                  .format(username, k, deploy_dir, data_dir, k))
    for k in cluster_config["pd_servers"].keys():
        os.system("scp {}@{}:{}/log/pd.log {}/{}-pd.log"
                  .format(username, k, deploy_dir, data_dir, k))
    for i in cluster_config["tikv_servers"].items():
        v = i[1].split()
        os.system("scp {}@{}:{}/log/tikv.log {}/{}-tikv.log"
                  .format(username, v[0], v[1][11:], data_dir, i[0].split()[0]))

def load_config(filename):
    f = open(filename, "r")
    parser = ConfigParser(
        interpolation=ExtendedInterpolation(),
        allow_no_value=True
    )
    parser.read_string(f.read())
    return parser

if __name__ == "__main__":
    pull()
