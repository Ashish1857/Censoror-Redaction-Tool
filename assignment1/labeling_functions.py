from snorkel.labeling import labeling_function

ABSTAIN = -1
NAME = 0
DATE = 1
PHONE = 2
ADDRESS = 3

@labeling_function()
def lf_contains_name(x):
    # Add your logic to detect names
    return NAME if 'John' in x else ABSTAIN

@labeling_function()
def lf_contains_date(x):
    # Add your logic to detect dates
    return DATE if '2020' in x else ABSTAIN

@labeling_function()
def lf_contains_phone_number(x):
    # Add your logic to detect phone numbers
    return PHONE if '123-456-7890' in x else ABSTAIN

@labeling_function()
def lf_contains_address(x):
    # Add your logic to detect addresses
    return ADDRESS if 'Main Street' in x else ABSTAIN
