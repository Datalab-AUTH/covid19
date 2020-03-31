import string

import country_converter as coco


def covert_country_name_to_country_code(country_names, punctuation=True, convert_to='ISO2'):
    """
    Converts an array of country names to ISO2 country codes through regex
    :param convert_to: The standard you want to use for conversion, e.g., ISO2, ISO3, etc.
    :param punctuation: True if function should check for punctuation inside country_names, false otherwise
    :param country_names: An array of strings representing country names
    :return: An array of strings representing the equivalent ISO2 codes
    """
    if punctuation:
        country_names = [c.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))) for c in
                         country_names]  # Replace punctuation from country names with whitespace
    # Convert to ISO2 or ISO3 codes
    standard_names = coco.convert(names=country_names, to=convert_to, include_obsolete=True)
    return standard_names


if __name__ == '__main__':
    """
    Test main function
    """
    countries = ['Greece', '(Hellas)', 'greece', 'South_Korea', 'South Korea', 'south Korea', 'GREECE', 'EL']
    print(covert_country_name_to_country_code(countries))
