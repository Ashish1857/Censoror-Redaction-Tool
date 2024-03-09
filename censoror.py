# censoror.py
import argparse
import glob
import os
from assignment1.redact_functions import redact_text

def load_files(input_pattern, default_directory='./'):
    if input_pattern:  # If a pattern is provided, use it to load files
        return glob.glob(input_pattern)
    else:  # If no pattern is provided, load all .txt files from the default directory
        return glob.glob(os.path.join(default_directory, '*.txt'))


def save_redacted_file(text, original_file_path, output_directory):
    output_file_name = os.path.basename(original_file_path) + ".censored"
    output_file_path = os.path.join(output_directory, output_file_name)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Write the modified text to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(text)

def main():
    parser = argparse.ArgumentParser(description="Censor sensitive information from text files.")
    parser.add_argument('--input', type=str, help="Glob pattern for input text files.")
    parser.add_argument('--names', action='store_true', help="Flag to censor names.")
    parser.add_argument('--dates', action='store_true', help="Flag to censor dates.")
    parser.add_argument('--phones', action='store_true', help="Flag to censor phone numbers.")
    parser.add_argument('--address', action='store_true', help="Flag to censor addresses.")
    parser.add_argument('--output', type=str, help="Directory to save censored files.", default='files')
    parser.add_argument("--stats", choices=["stdout", "stderr"], default="stderr", help="Output statistics to stdout or stderr.")
    args = parser.parse_args()

    input_pattern = args.input if args.input else '*.txt'
    file_paths = load_files(args.input or './*.txt')  # Use provided pattern or default to docs

    for file_path in file_paths:
        with open(file_path, 'r') as f:
            text = f.read()

        flags = {
            'names': args.names,
            'dates': args.dates,
            'phones': args.phones,
            'address': args.address
        }
        redacted_text = redact_text(text, flags)

        save_redacted_file(redacted_text, file_path, args.output)

if __name__ == "__main__":
    main()