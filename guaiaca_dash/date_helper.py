class DateHelper:
    def __init__(self) -> None:
        pass

    def get_month_number_abbr(self,month_name_abbr):
        # Define a mapping of month abbreviations to month numbers
        month_abbr_to_number = {
            'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4,
            'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8,
            'set': 9, 'out': 10, 'nov': 11, 'dez': 12
        }
        
        # Convert the abbreviation to lowercase to handle case-insensitivity
        month_name_abbr_lower = month_name_abbr.lower()
        
        # Lookup the month number based on the abbreviation
        month_number = month_abbr_to_number.get(month_name_abbr_lower)
        
        return month_number