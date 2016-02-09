#!/bin/bash

# usage: ./make_guis.sh "new_commit_name"
# removes all pre-existing dist/ stuff
# makes new frozen binaries
# commits them to PmagPy-Standalone
# pushes the new commit to Github

new="$1"
echo $new
my_commit="update: $new"
echo $my_commit

echo "starting make_guis script"
cp setup_scripts/setup_pmag_gui.py .
cp setup_scripts/setup_magic_gui.py .
echo "copied in setup scripts"
rm -rf build dist
echo "removed build & dist"

python setup_pmag_gui.py py2app
echo "ran setup script for Pmag GUI"
rm -rf ../PmagPy-Standalone/pmag_gui.app
echo "deleted old Pmag GUI"
mv dist/pmag_gui.app ../PmagPy-Standalone
echo "moved pmag_gui.app to PmagPy-Standalone"

rm -rf build dist
echo "removed build & dist"

python setup_magic_gui.py py2app
echo "ran setup script for MagIC GUI"
rm -rf ../PmagPy-Standalone/magic_gui.app
echo "deleted old Pmag GUI"
mv dist/magic_gui.app ../PmagPy-Standalone
echo "moved magic_gui.app to PmagPy-Standalone"
cd ../PmagPy-Standalone

echo 'adding git stuff'
git add .
echo 'adding .'
git commit -m "$my_commit"
echo 'committed'
git push

echo "clean up"
rm setup_pmag_gui.py
rm setup_magic_gui.py

echo "Done!  Changes pushed to PmagPy-Standalone-OSX"
