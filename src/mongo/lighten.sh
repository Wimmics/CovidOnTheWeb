#!/bin/bash

# CORD19 dataset
VERSION=6

# MongoDB database
DB=cord19v${VERSION}

mongo localhost/$DB entityfishing_light.js

mongo localhost/$DB spotlight_light.js
