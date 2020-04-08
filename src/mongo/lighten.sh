#!/bin/bash

# CORD19 dataset
VERSION=6

# MongoDB database
DB=cord19v${VERSION}

mongo localhost/$DB lighten_entityfishing.js

mongo localhost/$DB lighten_spotlight.js
