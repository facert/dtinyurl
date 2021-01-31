import re
import os
import hashlib
#import ipfsapi
import ipfshttpclient
import short_url


ipfs_api = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001/http")


GATEWAY_DOMAIN = "http://gateway.bdaily.club"

TINY_DOMAIN = "http://127.0.0.1:8000"

IPFS_DIR = "ipfs_dir"

FILENAME_PATH_DIR_FORMAT = "ipfs_dir/{p_dir}/{pp_dir}"
FILENAME_PATH_FORMAT = "ipfs_dir/{p_dir}/{pp_dir}/{filename}"
URL_PATH_FORMAT = "{domain}/ipfs/{hash}"


def gen_tiny_url(raw_url):
    tiny_code = gen_tiny_code(raw_url)
    u_hash = add_tiny_to_ipfs(tiny_code, raw_url)
    return {
        "tiny_url": "{domain}/{tiny_code}".format(domain=TINY_DOMAIN, tiny_code=tiny_code),
        "hash_urls": [URL_PATH_FORMAT.format(domain=GATEWAY_DOMAIN, hash=u_hash),
                     URL_PATH_FORMAT.format(domain="https://gateway.ipfs.io", hash=u_hash),
                     URL_PATH_FORMAT.format(domain="https://cloudflare-ipfs.com", hash=u_hash)]
    }


def gen_tiny_code(raw_url):
    u_id = int(hashlib.sha256(raw_url.encode('utf-8')).hexdigest(), 16) % 10 ** 8
    tiny_code = short_url.encode_url(u_id)
    return tiny_code


def add_tiny_to_ipfs(tiny_code, raw_url):
    filedir = FILENAME_PATH_DIR_FORMAT.format(p_dir=tiny_code[0], pp_dir=tiny_code[:2])
    filepath = FILENAME_PATH_FORMAT.format(p_dir=tiny_code[0], pp_dir=tiny_code[:2], filename=tiny_code)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    with open(filepath, "w") as f:
        f.write('<script>window.location.href=decodeURIComponent("{raw_url}")</script>'.format(raw_url=raw_url))
    return ipfs_api.add(filepath)["Hash"]


def get_tiny_url_by_code(tiny_code):
    filepath = FILENAME_PATH_FORMAT.format(p_dir=tiny_code[0], pp_dir=tiny_code[:2], filename=tiny_code)
    u_hash = ipfs_api.add(filepath)["Hash"]
    return URL_PATH_FORMAT.format(domain=GATEWAY_DOMAIN, hash=u_hash)






