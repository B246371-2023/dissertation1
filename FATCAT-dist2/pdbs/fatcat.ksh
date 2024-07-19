#!/usr/bin/ksh

set -e

PROGNAME="$(basename "$0")"

# First parameter ($1) is PDB file to generate inputs from
function makeinput {
    # Check if passed file with PDBs exists
    if [[ ! -e "${1}" ]]; then
        echo "File '${1}' for generating inputs was not found."
        return 1
    fi

    # Remove all input files prior to generating the new ones
    rm -f input_*.lst
    c=1
    n=1

    for pdb1 in $(< "${1}"); do
        for pdb2 in $(< "${1}"); do
            print "${pdb1}" "${pdb2}" >> "input_${c}.lst"
            if (( n == 512 )); then
                n=0
                ((c++))
            fi 
        ((n++))
        done
    done
}


function gofatcat {
    i=1
    # Get all files that match "input_*.lst" pattern. When there are no files that match, nothing happends
    files=(~(N)input_*.lst)
    for f in "${files[@]}"; do
        echo "Staring FATCAT for file: '${f}'"
        #~/biojava-protein-comparison-tool-4.0.0/runFATCAT.sh -autoFetch -pdbFilePath PDBs/ -flexible -alignPairs "${f}" -outFile "output_${i}.txt" &
        # Redirect output messages from bacground process to log file
        /home/s2530615/dissertation/biojava-protein-comparison-tool-7.1.1/runFATCAT.sh -autoFetch -pdbFilePath /home/s2530615/dissertation/pdbs -flexible -alignPairs "${f}" -outFile "output_${i}.txt" &> "compare_${i}.log" &
        ((i++))
    done

# Original supports only upto 8 input files
#     for ((c=1; c < 9; c++)); do
#         ~/biojava-protein-comparison-tool-4.0.0/runFATCAT.sh -autoFetch -pdbFilePath PDBs/ -flexible -alignPairs "input_${c}.lst" -outFile "output_${c}.txt" &
#     done
}


function reformat {
    #read in data from files
    for ((c=1; c < 9; c++)); do
        data+=($(tail -n +4 output_${c}.txt | awk '{print $1" "$2" "$3}'))
    done

    #print first line as csv
    columnheadings=" ,"
    for ((c=1; c < 193; c+=3)); do
        columnheadings+="${data[$c]},"
    done

    print "$columnheadings"

    #output the scores
    i=2
    for ((n=1; n < 193; n+=3)); do
        line="${data[$n]},"
        for ((c=$i; c < ((i+192)); c+=3)); do
            line+="${data[$c]},"
        done
        print "$line"
        ((i+=192))
    done
}

# help prints help.
function help {
  echo 1>&2 "Usage: ${PROGNAME} [--makeinputs, --compare, --help]"
  echo 1>&2 ""
  echo 1>&2 "Flags:"
  echo 1>&2 "  --makeinputs [file]   Run in make inputs mode with an optional input file. If input file is not passed the default file 'pdblist.txt' is used"
  echo 1>&2 "  --compare             Run in compare mode"
  echo 1>&2 "  --help                Display this help and exit script"
}

# Control flags to decide what mode to run
MAKE_INPUTS=0
COMPARE=0

# Default input file with list of PDBs for generating inputs
INPUT_FILE="pdblist.txt"

# If no argument is passed, display help
if [[ $# -eq 0 ]]; then
    help
    exit 1
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        "--makeinputs")
            MAKE_INPUTS=1
            shift # past argument

            # Check if optional file was passed
            if [[ -n "${1}" ]]; then
                INPUT_FILE="${1}"
                shift # past value
            fi
            ;;
        
        "--compare")
            COMPARE=1
            shift # past argument
            ;;
        
        "" | "help" | "-h" | "--help" )
            help
            exit 1
            ;;
        
        *)
            echo "Unknown option '$1'"
            help
            exit 1
            ;;
    esac
done

if [[ "${COMPARE}" -eq 1 && "${MAKE_INPUTS}" -eq 1 ]]; then
    echo "'--makeinputs' and '--compare' cannot be used together! This script should run only in a single mode at the time."
    echo "See --help for more information."
    exit 1
fi

# Make inputs mode
if [[ "${MAKE_INPUTS}" -eq 1 ]]; then
    echo "Creating inputs from PDB file: ${INPUT_FILE}"
    makeinput "${INPUT_FILE}"
fi

# Compare mode
if [[ "${COMPARE}" -eq 1 ]]; then
    echo "Comparison started..."
    gofatcat
fi
