"""
Module contains criteria functions to define what conditions make a paragraph a section header.
Each function should return True if the paragraph meet the specific criterion to be a section header

NOTE: These criteria are necessary as there is not an exact method to determine a section header
due to inconsistencies in the way documents are created. For instance, some documents use table of contents and
attach style attributes to the text, while others do not. Additionally, the definition of a section is partially
a personal preference. Thus, these criteria are merely heuristics to get as close as possible to
separating the different sections in a document .
"""

import string


def heading(p):
    """has Header formatting (common for table of contents section headers)"""
    if 'HEADING' in p.style.name.upper():
        return True


def capitalization(p):
    """has capitalization of every letter"""
    if p.text.isupper():
        return True


def style(p, use_bold=True, use_underline=True, use_bold_until_colon=True):
    """uses bold, underline, or colon text style criteria"""
    bold_runs = []
    underline_runs = []
    colon_runs = []
    colon_continue = True
    for run in p.runs:
        # ignore runs (style) for blank space at end of sentence
        if run.text.strip() == '':
            continue
        if use_underline:
            underline_runs.append(run.underline)
        if use_bold:
            bold_runs.append(run.bold)
        if use_bold_until_colon:
            # keep adding runs until a colon is found
            # for sections that have bold text until colon
            # (e.g. SECTION: ...)
            if colon_continue:
                colon_runs.append(run.bold)
                if ':' in run.text:
                    colon_continue = False
    bold_cond = all(bold_runs) and bold_runs != list()
    underline_cond = all(underline_runs) and underline_runs != list()
    colon_cond = all(colon_runs) and colon_runs != list()
    if bold_cond or underline_cond or colon_cond:
        return True


def capital_letter_list(p):
    """ uses list items that start with a capital letter
        e.g.  A. section text
              B. section text
              C. section text
    """

    upper_case_letters = [''.join([char, '. ']) for char in string.ascii_uppercase]
    upper_case_letter_list = (p.text.strip()[0:3] in upper_case_letters)
    if upper_case_letter_list:
        return True


def roman_numeral_list(p):
    """ find list items that start with a roman_numeral
    e.g.  I.   section text
          II.  section text
          III. section text

    NOTE: this function only identifies roman numerial up to XII
    """

    one_letter_numeral = (p.text.strip()[0:3] in ['I. ', 'V. ', 'X. '])
    two_letter_numeral = (p.text.strip()[0:4] in ['II. ', 'IV. ', 'VI. ', 'IX. ', 'XI. '])
    three_letter_numeral = (p.text.strip()[0:5] in ['III. ', 'VII. ', 'XII. '])
    four_letter_numeral = (p.text.strip()[0:6] in ['VIII.'])
    roman_numeral_start = (one_letter_numeral or two_letter_numeral
                           or three_letter_numeral or four_letter_numeral)
    if roman_numeral_start:
        return True


def ignore_bullets(p):
    """ bullets points are often converted into the letter 'O' followed by a space.
    Sections rarely start with a bullet point.
    """

    if p.text.strip()[0:2] in ['o ', 'O ']:
        return False
