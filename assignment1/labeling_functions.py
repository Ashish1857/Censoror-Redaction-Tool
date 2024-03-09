from snorkel.labeling import labeling_function
import spacy
import spacy.cli
from google.cloud import language
from google.cloud import language_v1

#spacy.cli.download("en_core_web_lg")
nlp = spacy.load('en_core_web_lg')  # Larger models may have better NER capabilities


ABSTAIN = -1
NAME = 0
DATE = 1
PHONE = 2
ADDRESS = 3

@labeling_function()
def lf_contains_name(x):
    doc = nlp(x)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            x = x.replace(ent.text, "\u2588" * len(ent.text))
    return x if x else ABSTAIN
