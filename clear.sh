#!/bin/sh
rm -rf V_ENV/
rm -rf build/
rm -rf dist/
pushd src/
rm -rf *.egg-info/
pushd apns_worker/
rm -f */*.pyc
rm *.pyc
popd
popd

