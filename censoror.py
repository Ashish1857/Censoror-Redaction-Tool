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
    filename = os.path.basename(original_file_path)
    output_path = os.path.join(output_directory, f"{filename}.censored")
    with open(output_path, 'w') as f:
        f.write(text)

def main():
    parser = argparse.ArgumentParser(description="Censor sensitive information from text files.")
    parser.add_argument('--input', type=str, help="Glob pattern for input text files.")
    parser.add_argument('--names', action='store_true', help="Flag to censor names.")
    parser.add_argument('--dates', action='store_true', help="Flag to censor dates.")
    parser.add_argument('--phones', action='store_true', help="Flag to censor phone numbers.")
    parser.add_argument('--address', action='store_true', help="Flag to censor addresses.")
    parser.add_argument('--output', type=str, help="Directory to save censored files.", default='files')
    args = parser.parse_args()

    # If we're testing (no specific input given), use the 'docs' directory
    input_pattern = args.input if args.input else '*.txt'
    file_paths = load_files(args.input or 'docs/*.txt')  # Use provided pattern or default to docs

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