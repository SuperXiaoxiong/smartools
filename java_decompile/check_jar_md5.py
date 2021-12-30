#! /usr/bin/env python3
#
# Resolve a list of local JAR files against Maven Central.
# The script calculates the SHA-1 checksum of each JAR and
# matches them using Maven Central's REST web service. For
# files known to the service, it prints an POM dependency
# snippet, unknown files are printed to stderr.
#
# Usage:
#   $ python3 jar-lookup.py JARFILE... > deps.xml 2> not-found.txt
#
import requests
import sys
import hashlib

URL_FMT = 'http://search.maven.org/solrsearch/select?q=1:"{}"&rows=20&wt=json'
DEP_FMT = """\
    <dependency>
      <groupId>{}</groupId>
      <artifactId>{}</artifactId>
      <version>{}</version>
    </dependency>"""


def mkhash(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return hashlib.sha1(data).hexdigest()

def lookup(checksum):
    url = URL_FMT.format(checksum)
    result = requests.get(url)
    docs = result.json()['response']['docs']
    return docs[0] if len(docs) > 0 else None

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        checksum = mkhash(filename)
        artifact = lookup(checksum)
        if artifact:
            print(DEP_FMT.format(artifact['g'], artifact['a'], artifact['v']))
        else:
            print(filename, file=sys.stderr)