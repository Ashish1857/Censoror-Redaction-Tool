# Importing necessary libraries
import os
import re
import spacy
from google.cloud import language_v1, language

#spacy.cli.download("en_core_web_lg")

# Loading the spaCy model for named entity recognition (NER)
nlp = spacy.load('en_core_web_lg')

# This function filters out strings that are exactly four digits long.
# These are often not sensitive entities but could be years or other numerical data.
def filter_out_4_digit_numbers(strings):
    return [s for s in strings if not re.match(r'^\d{4}$', s)]

# This function replaces identified entities with a block character.
# The block character is a visual indicator of redaction in the output text.
def replace_with_blocks(text, entities, file_path, args):
    # Removing any four-digit numbers as they are typically not entities of interest.
    ent = filter_out_4_digit_numbers(entities)
    for replace_str in ent:
        # Creating a string of block characters of equal length to the entity.
        full_block = "\u2588" * len(replace_str)
        text = text.replace(replace_str, full_block)  # Performing the replacement in the text.

    # Calling the function to save the redacted output to a file.
    save_redacted_file(text, file_path, args)

# This function utilizes Google Cloud's Language API to identify and redact entities from the text.
def gcp_usage(text_content, file_path, args):
    # Setting up the client with the provided JSON credentials.
    client = language_v1.LanguageServiceClient.from_service_account_json('service.json')

    # Creating a document for analysis by the Language API.
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Calling the API to analyze entities within the document.
    response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)

    # Extracting the text of the entities identified by the API call.
    entities = response.entities
    entity_texts = [entity.name for entity in entities if language_v1.Entity.Type(entity.type_).name in ['DATE', 'ADDRESS', 'PHONE_NUMBER']]

    # Redacting the entities by replacing them with block characters.
    replace_with_blocks(text_content, entity_texts, file_path, args)

# This function combines spaCy NER and Google Cloud's Language API to identify entities.
def analyze_entities(text_content, nlp):
    # Using spaCy to identify names within the text.
    doc = nlp(text_content)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    # Setting up the client and performing the analysis.
    client = language.LanguageServiceClient.from_service_account_json('services.json')
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)

    # Extracting entity names and combining them with spaCy-detected names.
    entities = response.entities
    entity_texts = [entity.name for entity in entities if language_v1.Entity.Type(entity.type_).name in ['DATE', 'ADDRESS', 'PHONE_NUMBER']]
    entity_texts += names

    return entity_texts

# Function to redact names found in folder paths, often present in email headers.
def redact_folder_names(text):
    # Matching the pattern of folder paths in the text.
    folder_pattern = re.compile(r'X-Folder: [\\]*\\([^\n\\]+)\\')
    matches = folder_pattern.findall(text)
    for match in matches:
        parts = re.split('_|, ', match)
        for part in parts:
            doc = nlp(part)
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    text = text.replace(match, "\u2588" * len(match))
                    break
    return text

# Main function to redact names identified by spaCy.
def redact_names(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            text = text.replace(ent.text, "\u2588" * len(ent.text))
    text = redact_folder_names(text)
    return text

# Function to redact names within email addresses, which can contain personally identifiable information.
def redact_names_in_emails(text):
    email_pattern = re.compile(r'\b[\w.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
    emails = email_pattern.findall(text)
    for email in emails:
        username = email.split('@')[0]
        for name_part in username.split('.'):
            doc = nlp(name_part)
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    redacted_email = email.replace(username, "\u2588" * len(username))
                    text = text.replace(email, redacted_email)
                    break
    return text

# Function to save the redacted text to a new file with '.censored' appended to the original file name.
def save_redacted_file(text, original_file_path, output_directory):
    output_file_name = os.path.basename(original_file_path) + ".censored"
    output_file_path = os.path.join(output_directory, output_file_name)

    os.makedirs(output_directory, exist_ok=True)

    with open(output_file_path, 'w') as output_file:
        if text is not None:
            output_file.write(text)

def redact_text(text, flags, file_path, args):
    if flags['names']:
        text = redact_names(text)
        text = redact_names_in_emails(text)
    if flags['phones' or 'address' or 'dates']:
        text = gcp_usage(text, file_path, args) 
    return text