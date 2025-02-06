import unittest
from unittest.mock import patch
import pandas as pd
import wbdata
import plotly.express as px

class TestMigrationDataProcessing(unittest.TestCase):

    @patch('wbdata.get_dataframe')
    def test_data_loading(self, mock_get_dataframe):
        """Test the correctness of loading data from the World Bank"""
        # Mock the data returned by wbdata.get_dataframe
        mock_data = pd.DataFrame({
            "country": ["Canada", "United States", "Mexico"],
            "date": [2010, 2011, 2012],
            "Net Migration": [1000, 2000, 1500]
        })
        mock_get_dataframe.return_value = mock_data

        # Fetch data
        indicator = {"SM.POP.NETM": "Net Migration"}
        data = wbdata.get_dataframe(indicator, country="all")
        
        # Test if data is loaded correctly
        self.assertEqual(len(data), 3)
        self.assertIn("country", data.columns)
        self.assertIn("Net Migration", data.columns)
        self.assertTrue(data["Net Migration"].iloc[0] == 1000)

    def test_region_mapping(self):
        """Test if countries are correctly assigned to their respective regions"""
        data = pd.DataFrame({
            "country": ["Canada", "Australia", "Brazil", "Egypt"],
            "Net Migration": [1000, 2000, 1500, 500],
            "date": [2010, 2011, 2012, 2013]
        })
        
        regions = {
            "Asia-Pacific": ["Australia", "Bangladesh", "Brunei Darussalam"],
            "Africa": ["Egypt"],
            "South America": ["Brazil"],
            "North America": ["Canada"]
        }
        
        # Assign regions to countries
        region_map = {country: region for region, countries in regions.items() for country in countries}
        data["region"] = data["country"].map(region_map)

        # Test if regions are assigned correctly
        self.assertEqual(data.loc[data["country"] == "Canada", "region"].values[0], "North America")
        self.assertEqual(data.loc[data["country"] == "Australia", "region"].values[0], "Asia-Pacific")
        self.assertEqual(data.loc[data["country"] == "Brazil", "region"].values[0], "South America")
        self.assertEqual(data.loc[data["country"] == "Egypt", "region"].values[0], "Africa")

    def test_data_aggregation(self):
        """Test data aggregation by region and year, and calculate the total migration"""
        data = pd.DataFrame({
            "country": ["Canada", "United States", "Mexico", "Canada", "Mexico"],
            "date": [2010, 2010, 2010, 2011, 2011],
            "Net Migration": [1000, 2000, 1500, 1100, 1600],
            "region": ["North America", "North America", "North America", "North America", "North America"]
        })

        # Aggregate the data by region and year to calculate the total migration
        region_data = data.groupby(["date", "region"])["Net Migration"].sum().reset_index()

        # Output the aggregated data for debugging
        print(region_data)
        
        # Update the expected value to 4500
        self.assertEqual(region_data.loc[(region_data["date"] == 2010) & (region_data["region"] == "North America"), "Net Migration"].values[0], 4500)
        self.assertEqual(region_data.loc[(region_data["date"] == 2011) & (region_data["region"] == "North America"), "Net Migration"].values[0], 2700)

    def test_plot_creation(self):
        """Test if the plot object is created"""
        region_data = pd.DataFrame({
            "date": [2010, 2011, 2012],
            "region": ["North America", "South America", "Africa"],
            "Net Migration": [1000, 2000, 1500]
        })
        
        # Create the plot
        fig = px.line(region_data, x="date", y="Net Migration", color="region", title="Net Migration Trends by Region")
        
        # Test if the figure is created
        self.assertIsNotNone(fig)
        self.assertEqual(fig.layout.title.text, "Net Migration Trends by Region")

if __name__ == '__main__':
    unittest.main()
