# psipred_modal_script

## Description
This script is designed to get secondary structure (SS) predictions with s4pred on modal.

## How to Run
To run this script, use the following command:
modal run psipred_modal_script.py --input-file-path=<INPUT_TXT> --output-file-path=<OUTPUT_TXT>

Replace `<INPUT_TXT>` and `<OUTPUT_TXT>` with your input and output file paths.

## Input Format
The input should look like protein_1 \t AVETSQINEIEEELTVLKEVFRNEAGLQE \n

## Output Format
The output will be in the FAS format as output by S4pred. 
It looks something like this: >protein_1 \n AVETSQINEIEEELTVLKEVFRN... \n HHHHHEEEEEEELLEEEEHHHH... \n 

## Execution parameters
- **Maximum Workers:** The script supports up to 10 workers at a time.
- **Batch Sequence Size:** The maximum sequence size per batch is set to 20.

## Additional Information
Please allow some time for the script to set up and execute
