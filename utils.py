

def get_recognized_components(text, recognizer, max_len=100):
    while len(text) > 1:
        for i in range(len(text), 0, -1):
            if i >= max_len: continue
            if i == 1:
                yield text[0]
                text = text[1:]
                break
            if recognizer(text[0:i]):
                yield text[0:i]
                text = text[i:]
                break
    if len(text):
        yield text


def split_into_lines(text, max_len=80):
    while len(text) > max_len:
        split_idx = text.rfind(' ', 0, max_len)
        yield text[:split_idx]
        text = text[split_idx:].strip()
    yield text
