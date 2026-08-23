#!/bin/bash
set -e
cd site
npm install --legacy-peer-deps
npx quartz build -d ../content
