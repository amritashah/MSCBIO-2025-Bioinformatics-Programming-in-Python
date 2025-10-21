#!/bin/bash
awk -F',' '{print $2,$1}' $1 |sort
