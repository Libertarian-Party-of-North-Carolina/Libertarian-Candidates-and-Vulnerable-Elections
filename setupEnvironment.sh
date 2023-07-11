#!/bin/bash

echo "Creating folders."
mkdir ./outputs
mkdir ./registration_data
mkdir ./candidate_data
echo "Created folders."

# Create virtual environment

#echo "Creating virtual environment."
#
#sudo apt install python3-virtualenv
#python3 -m venv env
#
#echo "Created virtual environment."


echo "Downloading Candidate Files."

wget -q -P ./candidate_data/ "https://s3.amazonaws.com/dl.ncsbe.gov/Elections/2023/Candidate%20Filing/Candidate_Listing_2023.csv"

echo "Downloaded Candidate Files."


echo "Downloading Voter Registration Files."

wget -q -P ./registration_data/ "https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvoter_Statewide.zip"

echo "Downloaded Voter Registration Files."

echo "Unzipping Voter Registration Files."

unzip ./registration_data/ncvoter_Statewide.zip -d ./registration_data

echo "Unzipped Voter Registration Files."

echo "Removing Voter Registration zip File."

rm -rf ./registration_data/ncvoter_Statewide.zip

echo "Removed Voter Registration zip File."
