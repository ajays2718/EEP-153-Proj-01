import unittest
import pandas as pd
from plotly.graph_objs import Figure
import wbdata

class TestNetMigrationMiddleEast(unittest.TestCase):

    def test_region_filtering(self):
        """Test if the filtering for Middle East countries is correct."""
        # Fetch Net Migration data
        indicator = {"SM.POP.NETM": "Net Migration"}
        data = wbdata.get_dataframe(indicator, country="all").dropna().reset_index()

        # Define Middle East countries
        middle_east_countries = [
            "Bahrain", "Iran, Islamic Rep.", "Iraq", "Israel", "Jordan", "Kuwait",
            "Lebanon", "Oman", "Qatar", "Saudi Arabia", "Syrian Arab Republic",
            "United Arab Emirates", "West Bank and Gaza", "Yemen, Rep."
        ]
        
        # Filter the data for Middle East countries
        data_filtered = data[data["country"].isin(middle_east_countries)]
        
        # Ensure that all countries in the filtered data belong to the Middle East list
        for country in data_filtered["country"]:
            self.assertIn(country, middle_east_countries, f"Country {country} is not in the Middle East list.")

if __name__ == '__main__':
    unittest.main()
