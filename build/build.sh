#!/bin/bash
cd `dirname $0`
rm -r localbuild 2>/dev/null
mkdir localbuild
mkdir -p localbuild/opt/pinterceptor
cp -r DEBIAN localbuild
rsync --filter=':- ../.gitignore' -r ../src localbuild/opt/pinterceptor
dpkg-deb --build --root-owner-group ./localbuild nice.deb
rm -r localbuild
