#!/bin/bash

# Set the input and output directories
input_dir="./"
output_dir="temp"

# Make sure the output directory exists
mkdir -p "$output_dir"

# Loop over all WAV files in the input directory
for file in "$input_dir"/*.wav; do
  filename=$(basename "$file")  # Extract file name without the path
  sox "$file" "$output_dir/$filename"
done
