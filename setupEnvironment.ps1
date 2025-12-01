Write-Host "Creating folders."
New-Item -ItemType Directory -Path "./outputs"
New-Item -ItemType Directory -Path "./registration_data"
New-Item -ItemType Directory -Path "./candidate_data"
Write-Host "Created folders."

# Create virtual environment

#Write-Host "Creating virtual environment."
#
#sudo apt install python3-virtualenv
#python3 -m venv env
#
#Write-Host "Created virtual environment."


Write-Host "Downloading Candidate Files."

Invoke-WebRequest -Uri "https://s3.amazonaws.com/dl.ncsbe.gov/Elections/2026/Candidate%20Filing/Candidate_Listing_2026.csv" -OutFile "./candidate_data/Candidate_Listing_2026.csv"

Write-Host "Downloaded Candidate Files."


Write-Host "Downloading Voter Registration Files."

Invoke-WebRequest -Uri "https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvoter_Statewide.zip" -OutFile "./registration_data/ncvoter_Statewide.zip"

Write-Host "Downloaded Voter Registration Files."

Write-Host "Unzipping Voter Registration Files."

Expand-Archive -Path "./registration_data/ncvoter_Statewide.zip" -DestinationPath "./registration_data"

Write-Host "Unzipped Voter Registration Files."

Write-Host "Removing Voter Registration zip File."

Remove-Item -Path "./registration_data/ncvoter_Statewide.zip"

Write-Host "Removed Voter Registration zip File."
