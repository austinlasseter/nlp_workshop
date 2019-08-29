from project.documents import section_criteria

class Section:
    """ Validate and collect the text for a section """
    def __init__(self, section_name='', section_criteria=[
                  section_criteria.heading
                , section_criteria.capitalization
                , section_criteria.style
                , section_criteria.capital_letter_list
                , section_criteria.roman_numeral_list
                , section_criteria.ignore_bullets
        ]):
        """
        :param section_name: Name of the section. Empty default for the first section
        :param section_criteria: callables with criteria to define the start of a new section
        """

        section_name = section_name.replace('\t',' ').replace('/S','').replace('\n','').strip()
        self.section_name = section_name.upper()
        self.criteria = ''
        self.section_text = []
        self.section_criteria_callables = [s_c for s_c in section_criteria]

    def set_section_name(self, text):
        # replace the 'First_Section' with actual section name
        # only occurs if the first paragraph is a section header
        if self.section_name == 'FIRST SECTION':
            self.section_name = ''
        text = text.replace('\t',' ').replace('/S','').replace('\n','').strip()
        self.section_name = ' '.join([self.section_name, text.upper()])

    def add_section_text(self, text):
        text = text.replace('\t',' ').replace('/S','').replace('\n','').strip()
        self.section_text.append(text)

    def get_section_text(self):
        return ' '.join(self.section_text).strip()

    def section_has_text(self):
        if ''.join(self.section_text).strip() != '':
            return True
        return False

    @staticmethod
    def paragraph_doesnt_have_text(p, alpha_only=True):
        """ check if a paragraph contains text

        :param p: paragraph
        :param alpha_only: if True, keep only paragraph with letters (e.g. ignore phone #)
        :return: bool (True) if the paragraph does not contain any text
        """

        empty_string = p.text.strip() == ''

        has_required_characters = True
        if alpha_only:
            # ignores phone numbers and string of non-text characters (e.g. _____)
            has_required_characters = any(char.isalpha() for char in p.text)

        if empty_string or not has_required_characters:
            return True
        return False

    def is_section_header(self, p):
        """ determine if a paragraph is a section header

        :param p: paragraph
        :return section_header: boolean, True if paragraph is a section header
        """

        section_header = False
        for criteria_callable in self.section_criteria_callables:
            if criteria_callable(p):
                section_header = True
                self.criteria = str(criteria_callable)

        return section_header
