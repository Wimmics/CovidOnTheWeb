#!/bin/bash

DB=cord19v4

mongo localhost/$DB entityfishing_light.js
