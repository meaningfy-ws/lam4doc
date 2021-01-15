#!/bin/bash

if ! [ $(id -u) = 0 ]; then
   echo "This script must be run as root."
   exit 1
fi

VERSION_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
VERSION=$(curl -f --silent $VERSION_URL)
if [ -z "$VERSION" ]; then
  echo "Failed to read current version from $VERSION_URL. Aborting."
  exit 1
else
  echo "Current version is $VERSION"
fi

set -e
set -o pipefail

ZIPFILEPATH="/tmp/chromedriver-$VERSION.zip"
echo "Downloading to $ZIPFILEPATH"
curl -f "https://chromedriver.storage.googleapis.com/$VERSION/chromedriver_linux64.zip" > "$ZIPFILEPATH"

BINFILEPATH="/opt/chromedriver"
echo "Extracting to $BINFILEPATH"
unzip -p "$ZIPFILEPATH" chromedriver > "$BINFILEPATH"

echo Setting execute flag
chmod +x "$BINFILEPATH"

echo Updating symlink
ln -nfs "$BINFILEPATH" /usr/local/bin/chromedriver

echo Removing ZIP file
rm "$ZIPFILEPATH"


curl -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm /etc/apt/sources.list.d/google-chrome.list

echo Done.
google-chrome --version
chromedriver -v