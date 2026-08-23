#!/bin/bash
set -e
cd site/quartz
npm install --legacy-peer-deps
npx quartz build -d ../content
