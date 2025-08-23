import os

import crossplane

NGINX_SITES_DIR = "/opt/homebrew/etc/nginx"


def process_conf(path):
    return crossplane.parse(path)


class NginxSite:
    def __init__(self):
        self._common_name = None
        self._sans = []


class Nginx:
    def __init__(self):
        self._sites = []

    def extract_sites(self):
        files = os.listdir(NGINX_SITES_DIR)
        data = [
            {file: process_conf(f"{NGINX_SITES_DIR}/{file}")}
            for file in files
            if os.path.isfile(f"{NGINX_SITES_DIR}/{file}") and file.endswith(".conf")
        ]
        return data
