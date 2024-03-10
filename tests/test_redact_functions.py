import pytest
from assignment1.redact_functions import redact_names, redact_names_in_emails

# Here we define a series of test cases as functions with assertions.
def test_redact_names():
    input_text = "Steve, Wang and Ryan are working together."
    # Count the number of characters in each name to be redacted
    expected_output = "\u2588" * 5 + ", " + "\u2588" * 4 + " and " + "\u2588" * 4 + " are working together."
    assert redact_names(input_text) == expected_output

def test_redact_names_with_no_names():
    input_text = "No names mentioned here."
    expected_output = "No names mentioned here."
    assert redact_names(input_text) == expected_output

def test_redact_names_case_insensitive():
    input_text = "john doe and jane smith are working together."
    # "john doe" is 8 characters including the space, "jane smith" is 10 characters including the space
    expected_output = "\u2588" * 8 + " and " + "\u2588" * 10 + " are working together."
    assert redact_names(input_text) == expected_output

def test_redact_names_in_emails():
    input_text = "Emails to test: jane.doe@example.com, jane.smith@work.org"
    expected_output = "Emails to test: " + "\u2588" * len("jane.doe") + "@example.com, " + "\u2588" * len("jane.smith") + "@work.org"
    assert redact_names_in_emails(input_text) == expected_output

if __name__ == "__main__":
    pytest.main()
