# tests/test_censoror.py
import subprocess
import os
import re

def test_censoror():
    # Get the absolute path of the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    censoror_script_path = os.path.join(project_root, 'censoror.py')
    input_pattern = os.path.join(project_root, './', '*.txt')
    output_directory = os.path.join(project_root, 'files')
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    command = [
        'python', censoror_script_path,
        '--input', input_pattern,
        '--names', 
        '--dates', 
        '--phones', 
        '--address',
        '--output', output_directory
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, f"Error: {result.stderr}"

    # Check if files are created in the output directory
    censored_files = os.listdir(output_directory)
    assert len(censored_files) > 0, "No files were censored and written to the output directory."
    
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

   # Check if emails are redacted if that is part of your requirements
    for file_name in censored_files:
        file_path = os.path.join(output_directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            emails = email_pattern.findall(content)
            assert not emails, f"Emails not redacted in {file_name}"

# This line allows the script to be run from the command line
if __name__ == "__main__":
    test_censoror()
