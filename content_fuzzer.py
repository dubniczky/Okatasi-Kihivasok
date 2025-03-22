from weasyprint import HTML
from wonderwords import RandomWord
import random


page_text = '<h2>1. Task</h2>Create a random generator function, that generates 100 random numbers between 1 and 1000, and returns their average. <h2>2. Task</h2>Create a function that takes a string as an input, and shuffles the output so that the words are in a random order. <h2>3. Task</h2>Make a function that encrypts a string with the ROT 9 cipher.'
output_file = 'test.pdf'


ww = RandomWord()
internal_padding_bytes = 0
internal_padding_words = 0

def make_random_words_of_length(length):
    random_words = []
    while sum(map(len, random_words)) < length:
        random_words.append(ww.word(word_min_length=3, word_max_length=8))
    random_words[-1] = random_words[-1][:length - sum(map(len, random_words))]
    return random_words


def fuzz_text(page_text, space_length=32):
    global internal_padding_bytes, internal_padding_words
    words = page_text.split()
    print(f'Fuzzing {len(page_text)} bytes, {len(words)} words...', flush=True)
    fuzzed_text = []
    for word in words:
        fuzzed_text.append(word)
        random_padding = make_random_words_of_length(space_length) + [' '] # adding spaces to make word wrapping correct
        print(f'{len(random_padding)-1} ', flush=True, end='')
        internal_padding_words += len(random_padding) - 1
        random.shuffle(random_padding)
        invisible_padding = '<d>' + ''.join(random_padding) + '</d>'
        internal_padding_bytes += len(invisible_padding)
        fuzzed_text.append(invisible_padding)
    return ''.join(fuzzed_text)


fuzzed_text = fuzz_text(page_text)
html = f'''
<!DOCTYPE html>
<html>
<head>
    <style>
        * {{
            word-wrap: break-word;
            white-space: pre-wrap;
        }}
        d {{
            color: white;
            font-weight: thin;
            font-size: 0.25px;
            font-family: Roboto, sans-serif;
        }}
    </style>
</head>
<body>
    <h1>3. Programming Homework</h1>
    <p>{fuzzed_text}</p>
</body>
</html>
'''

print()
print(f'Original text: {len(page_text)} bytes, {len(page_text.split())} words.')
print(f'Padded text with {internal_padding_bytes} bytes, {internal_padding_words} words.')
print(f'TOTAL: {len(html)} bytes, {len(html.split())} words.')

pdf = HTML(string=html)
pdf.write_pdf(output_file)
print(f'PDF saved to {output_file}.')