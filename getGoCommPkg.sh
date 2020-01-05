#!/usr/bin/env bash

#set -eox
cd $GOPATH/src
mkdir -p golang.org/x
cd golang.org/x

[ -d sys ] || git clone https://github.com/golang/sys.git
[ -d net ] || git clone https://github.com/golang/net.git
[ -d tools ] || git clone https://github.com/golang/tools.git

cd $GOPATH/src
[ ! -d google.golang.org ] && mkdir -p google.golang.org
cd  $GOPATH/src/google.golang.org
[ -d genproto ] || git clone https://github.com/googleapis/go-genproto genproto
