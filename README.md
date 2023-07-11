# Libertarian-Candidates-and-Vulnerable-Elections
Identifies Libertarian Candidates and Vulnerable Elections. 

This repo contains two things. First, a script that will set up the environment to match the one that I developed in. It isn't necessarily done 'right,' but it does work. This should work with either Windows or Linux with standard tools and Python3. Minor code changes will be needed for 2023.

After running all 3 steps below, your file structure will look like this.
```
├── candidate_data
│   └── Candidate_Listing_2023.csv
├── outputs
│   ├── all_libertarian_party_candidates_Candidate_Listing_2023.csv
│   └── vulnerable_races_Candidate_Listing_2023.csv
├── process.py
├── README.md
├── registration_data
│   └── ncvoter_Statewide.txt
├── setupEnvironment.ps1
└── setupEnvironment.sh
```

Step 1: Clone the repo.
```
git clone https://github.com/Libertarian-Party-of-North-Carolina/Libertarian-Candidates-and-Vulnerable-Elections.git
```
Step 2.1: Run the script Linux
```
chmod +x setupEnvironment.sh
./setupEnvironment.sh
```
Step 2.2: Run the script Windows
```
.\setupEnvironment.ps1
```
Step 3: Process the files.
```
python3 process.py
```
Step 4: The output of the script will be in the ouputs folder.
```
outputs/all_libertarian_party_candidates_Candidate_Listing_2023.csv
outputs/vulnerable_races_Candidate_Listing_2023.csv
```

