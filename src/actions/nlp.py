from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six


def get_parts_of_speech(text):
    client = language.LanguageServiceClient()
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    tokens = client.analyze_syntax(document).tokens
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
    output = []
    for token in tokens:
        output.append(
            {
                'parts_of_speech': pos_tag[token.part_of_speech.tag],
                'token': token.text.content
            }
        )
    return output


def get_sentiment(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    if 0.5 < sentiment.score <= 1:
        return 'very happpy'
    elif 0 < sentiment.score <= 0.5:
        return 'happy'
    else:
        return 'sad'