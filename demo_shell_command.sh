#!/bin/bash
for file in $(cat filelist); do
    curl --data-binary @"$file" localhost:10080/NEW@file
done
