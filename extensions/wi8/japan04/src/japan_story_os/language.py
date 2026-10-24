"""Loss-aware Japanese-script and display helpers. Never guess readings."""
import unicodedata

def display_record(record, order='japanese'):
    if order not in ('japanese','international'):raise ValueError('unsupported order')
    family=record.get('family_name');given=record.get('given_name')
    if not isinstance(family,str) or not isinstance(given,str) or not family or not given:raise ValueError('missing name components')
    return f'{family} {given}' if order=='japanese' else f'{given} {family}'

def macron_ascii(text):
    """Lossy DISPLAY transliteration only; never reversible or a reading oracle."""
    if not isinstance(text,str):raise ValueError('text required')
    table=str.maketrans({'ā':'a','ī':'i','ū':'u','ē':'e','ō':'o','Ā':'A','Ī':'I','Ū':'U','Ē':'E','Ō':'O'})
    return unicodedata.normalize('NFC',text).translate(table)

def script_tags(text):
    found=set()
    for c in text:
        n=ord(c)
        if 0x3040<=n<=0x309f:found.add('hiragana')
        elif 0x30a0<=n<=0x30ff:found.add('katakana')
        elif 0x3400<=n<=0x9fff:found.add('kanji')
        elif c.isalpha():found.add('latin')
    return sorted(found)
