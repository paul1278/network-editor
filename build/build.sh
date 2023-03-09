#!/bin/bash
cd `dirname $0`
VERSION=$1
if [ "$VERSION" = "" ]; then
  echo "Supply a version please!"
  exit 1
fi
echo "Building version v$VERSION"
rm -r localbuild 2>/dev/null
mkdir localbuild
mkdir -p localbuild/opt/pinterceptor
mkdir -p localbuild/usr/local/bin/
sed -i "s|Version: .*|Version: $VERSION|g" DEBIAN/control
cp -r DEBIAN localbuild
rsync --filter=':- ../.gitignore' -r ../src localbuild/opt/pinterceptor
ln -s /opt/pinterceptor/src/start.py localbuild/usr/local/bin/pinterceptor
cp localbuild/opt/pinterceptor/src/config.dist.yaml localbuild/opt/pinterceptor/src/config.yaml
dpkg-deb --build --root-owner-group ./localbuild pinterceptor-v$VERSION.deb
rm -r localbuild
