#!/bin/bash
ZIPFILE=deploy.zip
if [ -f "$ZIPFILE" ]; then
  rm "$ZIPFILE"
fi
DEPENDENCY_FOLDER=dependencies
if [ ! -d "$DEPENDENCY_FOLDER" ]; then
  mkdir "$DEPENDENCY_FOLDER"
fi
rm -rf "${DEPENDENCY_FOLDER:?}/*"
pip install -r requirements.txt --target "./$DEPENDENCY_FOLDER"
cd "$DEPENDENCY_FOLDER"
zip -r "../$ZIPFILE" .
cd ..
zip -g "$ZIPFILE" src/lambda.py