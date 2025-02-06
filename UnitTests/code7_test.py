import unittest
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
import wbdata

class TestNetMigrationAmericas(unittest.TestCase):

    def test_region_assignment(self):
        """Test if countries in the Americas are correctly assigned to the respective regions"""
        indicator = {"SM.POP.NETM": "Net Migration"}
        data = wbdata.get_dataframe(indicator, country="all").dropna().reset_index()

        # Define country groups
        north_america = ["United States", "Canada", "Mexico"]
        central_america = ["Belize", "Costa Rica", "El Salvador", "Guatemala", "Honduras", "Nicaragua", "Panama"]
        south_america = ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana",
                         "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"]
        
        # Add a "Region" column to the data
        data["Region"] = data["country"].apply(lambda x: "North America" if x in north_america else
                                                "Central America" if x in central_america else
                                                "South America" if x in south_america else None)
        
        # Drop rows with missing region data
        data = data.dropna(subset=["Region"])
        
        # Check if all countries have been correctly assigned to a region
        for country in data["country"]:
            self.assertIn(data.loc[data["country"] == country, "Region"].values[0],
                          ["North America", "Central America", "South America"],
                          f"Country {country} is not correctly assigned to a region.")

if __name__ == '__main__':
    unittest.main()
