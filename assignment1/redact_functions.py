import re
import spacy
import usaddress
import spacy.cli

spacy.cli.download("en_core_web_lg")
nlp = spacy.load('en_core_web_lg')  # Larger models may have better NER capabilities

def redact_folder_names(text):
    # Regular expression to find folder names following 'X-Folder:'
    folder_pattern = re.compile(r'X-Folder: [\\]*\\([^\n\\]+)\\')
    matches = folder_pattern.findall(text)
    for match in matches:
        # Split the match by underscores or commas and check each part with spaCy NER
        parts = re.split('_|, ', match)
        for part in parts:
            doc = nlp(part)
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    # Replace the entire matched folder name with [REDACTED]
                    text = text.replace(match, '[REDACTED]')
                    break  # If a name is detected, no need to check the rest of the entity matches
    return text
    
    
def redact_names(text):
    # Use spaCy's NER to redact names throughout the text
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            # Create a pattern to match the full name
            name_pattern = r'\b' + re.escape(ent.text) + r'\b'
            # Redact the full name with [REDACTED]
            text = re.sub(name_pattern, '[REDACTED]', text)
    
    # Handling for the list of names
    # This assumes the list is separated by newlines and each name follows the format: Lastname, Firstname
    name_list_pattern = re.compile(r'(?:\n[A-Z][a-z]+, [A-Z][a-z]+)+')
    matches = name_list_pattern.findall(text)
    for match in matches:
        # Split the matched text into individual names
        names = match.strip().split('\n')
        for name in names:
            if name:
                # Redact each name individually
                text = text.replace(name, '[REDACTED]')
    text = redact_folder_names(text)
    return text


def redact_emails(text):
    # This regex finds all email addresses
    email_pattern = re.compile(r'\b[\w.-]+?@\w+?\.\w+?\b')
    # This lambda function replaces the username part with [REDACTED]
    return email_pattern.sub(lambda x: '[REDACTED]@' + x.group().split('@')[1], text)

def redact_names_in_emails(text):
    # Regular expression to find email addresses
    email_pattern = re.compile(r'\b[\w.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
    # Use spaCy NER to check each username in the email address
    emails = email_pattern.findall(text)
    for email in emails:
        username = email.split('@')[0]
        # Split the username by dots to check each part with spaCy NER
        for name_part in username.split('.'):
            doc = nlp(name_part)
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    # Replace the username part of the email with [REDACTED]
                    redacted_email = email.replace(username, '[REDACTED]')
                    text = text.replace(email, redacted_email)
                    break  # If a name is detected, no need to check the rest of the username
    return text

def redact_dates(text):
    # Pattern to match the date format 'Day, DD Mon YYYY HH:MM:SS -TZ (TZD)'
    date_pattern = re.compile(r'''
    (?:\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\s)?  # Weekday
    (?:\d{1,2}\s)?                              # Day (optional)
    (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?,?\s  # Month
    (?:\d{1,2},?\s)?                            # Day (optional)
    \d{2,4}                                     # Year
    (?:\s\d{1,2}:\d{2}(:\d{2})?\s?(?:AM|PM|am|pm)?)?  # Time (optional)
    (?:\s-\d{4})?                               # Time zone offset (optional)
    |                                           # OR
    \b\d{1,2}/\d{1,2}/\d{2,4}\b                 # Numeric date
    (?:\s\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm))?  # Time (optional)
    ''', re.VERBOSE | re.IGNORECASE)

    
    # Replace the entire date with [REDACTED]
    redacted_text = date_pattern.sub('[REDACTED]', text)
    return redacted_text

def redact_phone_numbers(text):
    phone_pattern = re.compile(
    r'''
    (\+\d{1,3}([-.\s]?))?          # International code + separator (optional)
    (\(\d{1,4}\)|\d{1,4})          # Area code or country code with/without parentheses
    ([-.\s]?\d{1,4}){1,3}          # One to three groups of up to 4 digits, separated by optional separators
    ''', re.VERBOSE)

    return phone_pattern.sub('[REDACTED]', text)

def redact_addresses(text):
    # logic to redact addresses
    doc = nlp(text)
    tagged_address, _ = usaddress.tag(text)

    # Example for redacting the street number
    if 'AddressNumber' in tagged_address:
        text = text.replace(tagged_address['AddressNumber'], '[REDACTED]')
        
    text = re.sub(r'\b\d{5}(-\d{4})?\b', '[REDACTED]', text)
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            text = text.replace(ent.text, "[REDACTED]")
    return text

def redact_text(text, flags):
    if flags['names']:
        text = redact_names(text)
    if flags['dates']:
        text = redact_dates(text)
    if flags['phones']:
        text = redact_phone_numbers(text)
    if flags['address']:
        text = redact_addresses(text)
    if flags['names']:
        text = redact_names_in_emails(text)   
    return text
