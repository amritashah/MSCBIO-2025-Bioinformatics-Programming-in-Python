#!/bin/bash
awk -F',' '{print $1}' $1 | sort | uniq -c | sort -n
