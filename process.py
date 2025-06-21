import csv

def compare_candidates_to_members_and_analyze_races():

    outputs_folder = "outputs/"
    registration_data_folder = "registration_data/"
    candidate_filing_csv_folder = "candidate_data/"

    # Candidate filing CSV
    candidate_filing_csv_list = ["Candidate_Listing_2025.csv"]
    # candidate_filing_csv_list = ["Candidate_listing_2010.csv", "Candidate_listing_2011.csv", "Candidate_listing_2012.csv", "Candidate_listing_2013.csv", "Candidate_Listing_2014_rev1.csv", "Candidate_listing_2015.csv", "Candidate_Listing_2016.csv", "Candidate_Listing_2017.csv", "Candidate_Listing_2018.csv", "Candidate_Listing_2019.csv", "Candidate_Listing_2020.csv", "Candidate_Listing_2021.csv", "Candidate_Listing_2022.csv","Candidate_Listing_2023.csv", "Candidate_Listing_2024.csv", "Candidate_Listing_2025.csv"]

    # Libertarian Party Members CSV
    # registration_csv = "ncLibertarians3.csv"
    registration_csv = "ncvoter_Statewide.txt"

    # Dictionary of CSV headers and their index
    candidate_header_indexes = {}
    # Dictionary of CSV headers and their index
    libertarians_header_indexes = {}

    # Dictionary of all libertarians
    all_libertarians_dict = {}

    # Dictionary of all candidates
    all_candidates_dict = {}
    # Dictionary of all libertarian candidates
    all_libertarian_candidates_dict = {}

    # Dictionary of all races.
    all_races_dict = {}

    # Dictionary of Vulnerable Races
    vulnerable_races = {}

    # File headers
    candidate_headers_list = []

    # Open the registration file. Either the pre processed subset of libertarians or the entire state DB.
    def open_registration_csv_file(registration_csv, all_libertarians_dict, libertarians_header_indexes):
        all_libertarians_dict.clear()
        libertarians_header_indexes.clear()
        libertarian_member_headers_list = []

        print ('Opening Registration CSV files...')

        # Open the registration file.
        with open(registration_data_folder + registration_csv, errors='replace', encoding='utf-8-sig') as registration_csv_file:
            registration_csv_reader = csv.reader(registration_csv_file, delimiter='\t')
            libertarian_member_headers_list = next(registration_csv_reader)
            registration_csv_file.seek(0)

            for libertarian_header in libertarian_member_headers_list:
                libertarians_header_indexes.setdefault((libertarian_header),[]).append(libertarian_member_headers_list.index(libertarian_header))


            for registered in registration_csv_reader:
                if  registered[libertarians_header_indexes['party_cd'][0]] == "LIB": # and registered[libertarians_header_indexes['voter_status_desc'][0]] == "ACTIVE":
                    all_libertarians_dict[(registered[libertarians_header_indexes['first_name'][0]] + \
                        registered[libertarians_header_indexes['last_name'][0]] + \
                        registered[libertarians_header_indexes['name_suffix_lbl'][0]] + \
                        registered[libertarians_header_indexes['zip_code'][0]]).replace(" ", "").upper()] = registered
                    continue
            registration_csv_file.close()
        print ('Closing Registration CSV files...')

    def open_candidate_csv_file(all_candidates_dict, all_races_dict, candidate_headers_list, candidate_filing_csv_folder, candidate_filing_csv):

        candidate_headers_list.clear()
        candidate_header_indexes.clear()
        all_candidates_dict.clear()
        all_races_dict.clear()

        print ('Opening Candidate CSV files...')

        with open(candidate_filing_csv_folder + candidate_filing_csv, errors='replace', encoding='utf-8-sig') as candidate_filing_csv_file:
            candidate_csv_reader = csv.reader(candidate_filing_csv_file, delimiter=',')
            candidate_headers_list = next(candidate_csv_reader)
            # candidate_filing_csv_file.seek(0)

            # Headers for CSVs
            for candidate_header in candidate_headers_list:
                candidate_header_indexes.setdefault((candidate_header),[]).append(candidate_headers_list.index(candidate_header))

            for candidate in candidate_csv_reader:
                all_candidates_dict[(candidate[candidate_header_indexes['first_name'][0]] + \
                    candidate[candidate_header_indexes['last_name'][0]] + \
                    candidate[candidate_header_indexes['name_suffix_lbl'][0]] + \
                    candidate[candidate_header_indexes['zip_code'][0]]).replace(" ", "").upper()] = candidate
                all_races_dict.setdefault((candidate[candidate_header_indexes['election_dt'][0]]+candidate[candidate_header_indexes['contest_name'][0]]+candidate[candidate_header_indexes['county_name'][0]]),[]).append(candidate)
            candidate_filing_csv_file.close()
        print ('Closing Candidate CSV files...')
        return (candidate_headers_list)

    def idenfity_libertarian_candidates_dict_compare(all_candidates_dict, all_libertarians_dict, candidate_header_indexes, candidate_headers_list, all_libertarian_candidates_dict):
        print ('Identifying Libertarian Candidates...')
        all_libertarian_candidates_dict.clear()

        all_keys = set(list(all_candidates_dict.keys()) + list(all_libertarians_dict.keys()))

        for key in all_keys:
            try:
                if (key in all_libertarians_dict and key in all_candidates_dict) or all_candidates_dict[key][candidate_header_indexes['party_candidate'][0]] == 'LIB':
                    all_libertarian_candidates_dict[key] = all_candidates_dict[key]
            except (KeyError):
                pass

        print ('Done identifying Libertarian Candidates...')

    def identify_vulnerable_races(all_races_dict, candidate_header_indexes, vulnerable_races):
        vulnerable_races.clear()

        print ('Identifying Vulnerable Races...')
        for race in all_races_dict.keys():
            if int(all_races_dict[race][0][candidate_header_indexes['vote_for'][0]]) > len(all_races_dict[race]) or len(all_races_dict[race]) <= int(all_races_dict[race][0][candidate_header_indexes['vote_for'][0]]):
                vulnerable_races[race] = (all_races_dict[race][0][candidate_header_indexes['election_dt'][0]], \
                    all_races_dict[race][0][candidate_header_indexes['county_name'][0]], \
                    all_races_dict[race][0][candidate_header_indexes['contest_name'][0]], \
                    all_races_dict[race][0][candidate_header_indexes['is_unexpired'][0]], \
                    all_races_dict[race][0][candidate_header_indexes['vote_for'][0]], \
                    str(len(all_races_dict[race])))

        print ('Done Identifying Vulnerable Races...')

    def write_vulnerable_races(vulnerable_races, outputs_folder, candidate_filing_csv):
        print ('Writing Vulnerable Races...')


        vulnerable_races_list_headers = ['election_dt', 'county_name', 'contest_name', 'is_unexpired', 'vote_for', 'candidates_filed']

        with open(outputs_folder + 'vulnerable_races_'+candidate_filing_csv, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(vulnerable_races_list_headers)
            writer.writerows(vulnerable_races.values())

        print ('Done writing Vulnerable Races...')

    def write_all_libertarian_candidates_csv(candidate_headers_list, all_libertarian_candidates_dict, candidate_filing_csv):
        print ('Writing Libertarian Candidates...')

        with open(outputs_folder + 'all_libertarian_party_candidates_'+candidate_filing_csv, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(candidate_headers_list)
            writer.writerows(all_libertarian_candidates_dict.values())

        print ('Done writing Libertarian Candidates...')

    def driver(**kwargs):

        candidate_headers_list = []

        open_registration_csv_file(registration_csv, all_libertarians_dict, libertarians_header_indexes)
        for file in candidate_filing_csv_list:
            print ('Processing File: ' + file)
            candidate_filing_csv = file
            candidate_headers_list = open_candidate_csv_file(all_candidates_dict, all_races_dict, candidate_headers_list, candidate_filing_csv_folder, candidate_filing_csv)
            identify_vulnerable_races(all_races_dict, candidate_header_indexes, vulnerable_races)
            idenfity_libertarian_candidates_dict_compare(all_candidates_dict, all_libertarians_dict, candidate_header_indexes, candidate_headers_list, all_libertarian_candidates_dict)
            write_vulnerable_races(vulnerable_races, outputs_folder, candidate_filing_csv)
            write_all_libertarian_candidates_csv(candidate_headers_list, all_libertarian_candidates_dict, candidate_filing_csv)

    driver(**locals())

compare_candidates_to_members_and_analyze_races()
