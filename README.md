# cis6930sp24-assignment1

# Censoror - Sensitive Information Redaction Tool

## Introduction

Censoror is a Python-based command-line tool designed to redact sensitive information from text files, such as names, dates, phone numbers, and addresses.

## Installation

Clone the repository and navigate to the project directory. Install dependencies via pipenv or pip, as defined in `Pipfile`.

```bash
pipenv install
```

## How to run

![Video](docs/Video.gif)

## Features

- Redaction of personal names, dates, phone numbers, and addresses.
- Scalable to handle multiple files.

## Usage

Use the following command to run Censoror:

```bash
python censoror.py --input '*.txt' --names --dates --phones --address --output 'files/' --stats stderr
```

## Flags:

- input: Glob pattern for input files.
- names: Flag to redact names.
- dates: Flag to redact dates.
- phones: Flag to redact phone numbers.
- address: Flag to redact addresses.
- output: Directory for saving redacted files.

## Configuration

Set up service.json with your Google Cloud credentials for using the Google Cloud Natural Language API.

## Dependencies

- Python 3.11
- Spacy
- Snorkel
- Google Cloud Language API

Ensure you have Spacy's language model downloaded:

`python -m spacy download en_core_web_lg`

## Code Snippets and Explanation

### Loading Files

The `load_files` function uses the `glob` library to find all files matching a certain pattern. By default, it looks for `.txt` files.

```python
def load_files(input_pattern, default_directory='./'):
    if input_pattern:
        return glob.glob(input_pattern)
    else:
        return glob.glob(os.path.join(default_directory, '*.txt'))
```

### Main Function

The main function sets up the command-line argument parsing and iterates over each file to redact sensitive information based on the flags provided by the user.

```python
    def main():
    ...
    for file_path in file_paths:
    with open(file_path, 'r') as f:
    text = f.read()

            flags = {
                'names': args.names,
                'dates': args.dates,
                'phones': args.phones,
                'address': args.address
            }

            redact_text(text, flags, file_path, args.output)
```

### Redaction with Blocks

The replace_with_blocks function replaces the sensitive text with a full block character, \u2588, for each character in the sensitive string.

```python
def replace_with_blocks(text, entities, file_path, args):
    ent = filter_out_4_digit_numbers(entities)
    for replace_str in ent:
        full_block = "\u2588" \* len(replace_str)
        text = text.replace(replace_str, full_block)
```

### Google Cloud Natural Language API Usage

The gcp_usage function leverages Google Cloud's Natural Language API to analyze entities in the text and identify sensitive information such as dates, addresses, and phone numbers.

```python
def gcp_usage(text_content, file_path, args):
    client = language_v1.LanguageServiceClient.from_service_account_json('service.json')
    ...
```

### Redacting Folder Names

The redact_folder_names function searches for X-Folder: patterns and uses Named Entity Recognition (NER) to identify and redact personal names within the folder path.

```python
def redact_folder_names(text):
    folder_pattern = re.compile(r'X-Folder: [\\]*\\([^\n\\]+)\\')
    ...
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Ashish Anand - Initial work - [ashish.anand@ufl.edu](mailto:ashish.anand@ufl.edu)

## Assumptions, Bugs, and Limitations

## Assumptions

- **Text Encoding:** It is assumed that all text files are encoded in UTF-8. Files with different encodings may not be processed correctly.

- **Language Support:** The tool assumes that the text to be redacted is in English, as it uses an English-language model for Named Entity Recognition (NER).

- **Data Format:** The current version expects data in a format similar to email headers and content. Other formats may require additional logic for proper redaction.

## Known Bugs

- **Overzealous Redaction:** Due to the nature of NER, non-sensitive data that is mistakenly identified as a named entity (like company names or common nouns) may be redacted.

- **Inconsistent Entity Recognition:** Sometimes, the NER may not consistently identify all instances of an entity, leading to incomplete redaction.

- **Email Redaction Inconsistencies:** The tool may not redact all parts of an email address if the username does not get recognized as a person's name by the NER model.

## Limitations

- **Entity Type Coverage:** Currently, only dates, addresses, phone numbers, and names are targeted for redaction. Other types of sensitive information (such as social security numbers or credit card numbers) are not explicitly handled.

- **Complex Name Patterns:** Names that do not follow standard naming conventions may not be identified and redacted.

- **Performance:** The redaction process may be slow for large files, as it involves substantial computational work for entity detection.

- **Context Awareness:** The tool does not consider context; for example, it cannot distinguish between a date in a sentence and a date that is part of a non-sensitive data structure.

Please report any additional bugs or issues on the repository's issues page.

## Acknowledgements

I'd like to thank professor and the community for their invaluable insights and suggestions which have greatly improved the quality of this project. Special thanks go to the spaCy team for the amazing NLP library and Google Cloud for their powerful Language API which were instrumental in the development of this tool. Lastly, my gratitude goes to the <b>Snorkel<b> team for their novel approach to weak supervision, which has inspired aspects of this project.

## Details

For detailed documentation on the implementation, refer to the in-line comments within the censoror.py and redact_functions.py files.
