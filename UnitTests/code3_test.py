import unittest
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
import wbdata

class TestNetMigrationAfrica(unittest.TestCase):
    def test_african_data_filtering(self):
        """Test filtering data for African countries"""
        indicator = {"SM.POP.NETM": "Net Migration"}
        data = wbdata.get_dataframe(indicator, country="all").dropna().reset_index()

        # Define the list of African countries
        africa = [
            "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon",
            "Central African Republic", "Chad", "Comoros", "Congo, Dem. Rep.", "Congo, Rep.", "Cote d'Ivoire",
            "Djibouti", "Egypt, Arab Rep.", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon",
            "Gambia, The", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar",
            "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria",
            "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
            "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
        ]

        # Filter data to get only African countries
        africa_data = data[data["country"].isin(africa)]
        
        # Ensure that all countries in the filtered data are from Africa
        self.assertTrue(all(country in africa for country in africa_data["country"].unique()), 
                        "Some countries in the data are not in the African region.")

if __name__ == '__main__':
    unittest.main()
