# psipred_modal_script

## Description
This script is designed to execute the psipred prediction model.

## How to Run
To run this script, use the following command:
modal run psipred_modal_script.py --input-file-path=<INPUT_TXT> --output-file-path=<OUTPUT_TXT>

Replace `<INPUT_TXT>` and `<OUTPUT_TXT>` with your input and output file paths, respectively.

## Output Format
The output will be in the FAS format as defined by S4pred.

## Execution parameters
- **Maximum Workers:** The script supports up to 10 workers at a time.
- **Batch Sequence Size:** The maximum sequence size per batch is 20.

## Additional Information
Please allow some time for the script to set up and execute
