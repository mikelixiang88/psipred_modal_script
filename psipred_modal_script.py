import sys
import modal
from modal import Image

dockerfile_image = Image.from_dockerfile("Dockerfile")
stub = modal.Stub(image=dockerfile_image)

@stub.function()
def predict_structure(sequence):
    import subprocess
    import tempfile
    import os

    combined_sequence = ''.join(sequence)
    # Use a temporary file to safely write/read sequence data
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.fas') as temp_file:
        temp_file.write(combined_sequence)
        temp_file.flush()
        temp_file_path = temp_file.name
    # Run the model using subprocess and capture the output
    try:
        result = subprocess.run(["python", "run_model.py", temp_file_path, "--outfmt", "fas"],
                                capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print("Error running the model:", e.stderr)  # Print errors if the model fails
        return f"\nERROR\n"

    finally:
        # Cleanup the temporary FASTA file
        os.remove(temp_file_path)

    return result.stdout

def read_input_file(input_file_path):
    results = []
    with open(input_file_path, 'r') as file:
        identifier = None
        sequence_parts = []
        for line in file:
            line = line.strip()
            if '\t' in line:
                if identifier is not None:
                    results.append(f">{identifier}\n{''.join(sequence_parts)}\n")
                parts = line.split('\t', 1)
                identifier = parts[0]  
                sequence_parts = [parts[1]] if len(parts) > 1 else []  
            else:
                sequence_parts.append(line)

        if identifier is not None:
            results.append(f">{identifier}\n{''.join(sequence_parts)}\n")

    return results



def write_output_file(output_file_path, results):
    with open(output_file_path, 'a') as file:
        for result in results:
            file.write(result)

@stub.local_entrypoint()
def main(input_file_path, output_file_path):
    sequence_data = read_input_file(input_file_path)
    
    max_sequence_size = 20
    max_workers = 10
    num_batches = (len(sequence_data) + max_sequence_size - 1) // max_sequence_size

    num_workers = min(num_batches, 10)

    if num_workers == 0:
        print("No data to process.")
        return
    
    sequence_size = (len(sequence_data) + num_workers - 1) // num_workers
    sequence_size = min(sequence_size, max_sequence_size) 

    # Generate sequence chunks
    sequence_chunks = [sequence_data[i:i + sequence_size] for i in range(0, len(sequence_data), sequence_size)]


    # Use map to apply predict_structure to each chunk in parallel
    for i in range(0, len(sequence_chunks), max_workers):
        current_batch = sequence_chunks[i:i + max_workers]
        results = predict_structure.map(current_batch)  # Using map for parallel processing
        write_output_file(output_file_path, results)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python psipred_modal_script.py <INPUT_TXT> <OUTPUT_TXT>")
        sys.exit(1)
    input_txt, output_txt = sys.argv[1], sys.argv[2]
    main(input_txt, output_txt)
