import string

import country_converter as coco


def covert_country_name_to_country_code(country_names):
    """
    Converts an array of country names to ISO2 country codes through regex
    :param country_names: An array of strings representing country names
    :return: An array of strings representing the equivalent ISO2 codes
    """
    country_names = [c.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))) for c in
                     country_names]  # Replace punctuation from country names with whitespace
    standard_names = coco.convert(names=country_names, to='ISO2')  # Convert to ISO2 codes
    return standard_names


if __name__ == '__main__':
    """
    Test main function
    """
    countries = ['Greece', '(Hellas)', 'greece', 'South_Korea', 'South Korea', 'south Korea', 'GREECE']
    print(covert_country_name_to_country_code(countries))
