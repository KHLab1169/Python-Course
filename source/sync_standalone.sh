#!/bin/sh
# Build the page to publish and the standalone app's index.html from the course page.
# speed_pub.py moves the course content into a JSON block (faster to parse than script source);
# vendorize.py points the app at its local fonts and highlight.js.
cd "$(dirname "$0")"
mkdir -p publish
python3 speed_pub.py course.html publish/python-course.html >/dev/null
python3 vendorize.py publish/python-course.html python-course/index.html
