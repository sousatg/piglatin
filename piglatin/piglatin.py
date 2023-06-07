import re


def hasVowel(el):
    return el in "AEIOUaeiou"


def hasY(el):
    return el in "Yy"


def is_first_letter_capitalized(word):
    return word[0].isupper()


def capitalize_word_first_letter(word):
    """Capitalize first letter of word leaving the rest of the words with their formating"""
    first_letter = word[0]

    return first_letter.upper() + word[1:len(word)]


def translate_word_started_with_vowel(word):
    suffix = 'way'
    last_letter = word[-1]

    if (last_letter == last_letter.isupper and len(word) > 1):
        suffix = 'way'.upper()

    return word + suffix


def translate_word_started_with_consonante(sWord):
    sSuffix = ''
    sFirst = sWord[0]

    if sWord != sWord.upper():
        sFirst = sFirst.lower()

    for i in range(len(sWord)):
        sSuffix += sFirst
        sLast = sFirst

        isCapitalized = sFirst.isupper()

        sWord = sWord[1:]

        if len(sWord) > 0:
            sFirst = sWord[0]

        if (hasVowel(sFirst) or hasY(sFirst)) and (sLast not in "qQ" or sFirst not in "uU"):
            break

    if (isCapitalized):
        sSuffix += 'ay'.upper()
    else:
        sSuffix += 'ay'

    return sWord + sSuffix


def translateWord(psWord):
    sWord = psWord
    sFirst = sWord[0]
    was_first_letter_capitalized = is_first_letter_capitalized(sWord)

    if hasVowel(sFirst):
        sWord = translate_word_started_with_vowel(sWord)
    else:
        sWord = translate_word_started_with_consonante(sWord)

    if (was_first_letter_capitalized):
        sWord = capitalize_word_first_letter(sWord)

    return sWord


def translatePhrase(phrase):
    words = re.split(r"(\w[\w']*\w)", phrase)

    words = map(lambda word: translateWord(word) if word.isalpha() else word, words)

    return ''.join(words)