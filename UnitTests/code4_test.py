import unittest
import pandas as pd
from plotly.graph_objs import Figure
import wbdata

class TestNetMigrationAsiaPacific(unittest.TestCase):

    def test_region_filtering(self):
        """Test if the filtering for Asia-Pacific countries is correct."""
        # Fetch Net Migration data
        indicator = {"SM.POP.NETM": "Net Migration"}
        data = wbdata.get_dataframe(indicator, country="all").dropna().reset_index()

        # Define Asia-Pacific countries
        asia_pacific = [
            "Australia", "Bangladesh", "Brunei Darussalam", "Cambodia", "China", "Fiji", "Indonesia", "Japan",
            "Kiribati", "Korea, Rep.", "Lao PDR", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "New Zealand",
            "Pakistan", "Papua New Guinea", "Philippines", "Singapore", "Solomon Islands", "Sri Lanka", "Thailand",
            "Timor-Leste", "Tonga", "Tuvalu", "Vanuatu", "Vietnam"
        ]
        
        # Filter the data for Asia-Pacific countries
        data_filtered = data[data["country"].isin(asia_pacific)]
        
        # Ensure that all countries in the filtered data belong to the Asia-Pacific region
        for country in data_filtered["country"]:
            self.assertIn(country, asia_pacific, f"Country {country} is not in the Asia-Pacific list.")

if __name__ == '__main__':
    unittest.main()
