BAD_WORDS = [
    "badword1", 
    "badword2",
    "badword3",
    # keep adding, one per line, all lowercase, may need to refresh the server after making chages 
]

def contains_bad_words(text):
    text_lower = text.lower()
    for word in BAD_WORDS:
        if word in text_lower:
            return True
    return False

def blur_bad_words(text):
    for word in BAD_WORDS:
        import re
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        replacement = f'<span class="blurred">{word}</span>'
        text = pattern.sub(replacement, text)
    return text
