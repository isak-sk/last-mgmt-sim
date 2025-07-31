import pandas as pd
from datetime import datetime
import config


class ExcelLoader:
    def __init__(self, year=2024):
        self.filepath = config.EXCEL_FILE
        self.year = year
        self.df = None

    def load_data(self):

        self.df = pd.read_excel(self.filepath, usecols="A:C", engine="openpyxl")
        self.df.columns = ['Bezug', 'Produktion', 'timestamp']
        self.df['parsed_time'] = self.df['timestamp'].apply(self._parse_date)
        return self.df


    def _parse_date(self, text):
        try:
            clean_text = str(text).replace('. ', ' ', 1).strip()
            return datetime.strptime(f"{clean_text} {self.year}", "%d.%m %H:%M %Y")
        except ValueError as e:
            print(f"Failed to parse date: '{text} - {e}")
            return None
