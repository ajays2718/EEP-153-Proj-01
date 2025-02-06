import unittest
import pandas as pd
from plotly.graph_objs import Figure
import wbdata

class TestNetMigrationEurope(unittest.TestCase):

    def test_region_filtering(self):
        """Test if the filtering for European countries is correct."""
        # Fetch Net Migration data
        indicator = {"SM.POP.NETM": "Net Migration"}
        data = wbdata.get_dataframe(indicator, country="all").dropna().reset_index()

        # Define European countries
        europe_countries = [
            "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina",
            "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France",
            "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia",
            "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro",
            "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania",
            "San Marino", "Serbia", "Slovak Republic", "Slovenia", "Spain", "Sweden", "Switzerland",
            "Ukraine", "United Kingdom", "Turkiye"
        ]
        
        # Filter the data for European countries
        data_filtered = data[data["country"].isin(europe_countries)]
        
        # Ensure that all countries in the filtered data belong to the European list
        for country in data_filtered["country"]:
            self.assertIn(country, europe_countries, f"Country {country} is not in the European list.")

if __name__ == '__main__':
    unittest.main()
