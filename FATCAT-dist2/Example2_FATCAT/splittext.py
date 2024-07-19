import re

def parse_data(file_path):
    results = []
    with open(file_path, 'r') as file:
        current_result = {}
        for line in file:
            # extract pdb name
            if "Align" in line:
                match = re.search(r"Align (\S+)\.pdb \d+ with (\S+)\.pdb \d+", line)
                if match:
                    current_result['name1'] = match.group(1)
                    current_result['name2'] = match.group(2)
            
            # extract score name
            elif "Twists" in line:
                match = re.search(r"Score (\d+\.\d+)", line)
                if match:
                    current_result['score'] = match.group(1)

            # extract p-value name
            elif "P-value" in line:
                match = re.search(r"P-value (\S+)", line)
                if match:
                    current_result['p-value'] = match.group(1)
                    results.append(current_result)
                    current_result = {} 

    return results

file_path = 'allpair3.aln'  # hardcode now
parsed_results = parse_data(file_path)
for result in parsed_results:
    print(result)




