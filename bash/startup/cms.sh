#!/bin/sh

echo starting up CMS...

cd "../../CMS Web App"

python3 -m http.server 21001

echo DONE! CMS running on port 21001