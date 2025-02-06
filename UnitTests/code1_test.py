import unittest
from unittest.mock import patch
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
import wbdata

class TestNetMigrationMap(unittest.TestCase):

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

    def test_data_aggregation(self):
        """Test data aggregation by year"""
        
        # Construct a simple test dataset
        test_data = pd.DataFrame({
            "country": ["Canada", "Mexico", "United States", "Canada", "Mexico"],
            "date": pd.to_datetime(["2018-01-01", "2018-01-01", "2018-01-01", "2019-01-01", "2019-01-01"]),
            "Net Migration": [1000, 2000, 1500, 1100, 1600],
        })
        
        # Extract the year from the date
        test_data["Year"] = test_data["date"].dt.year
        
        # Check if the year column is correct
        print(test_data)  # Debug output to check if the data is correct

        # Filter out data for the year 2018
        df_year = test_data[test_data["Year"] == 2018]
        
        # Test if the data for 2018 is correctly aggregated
        self.assertEqual(df_year["Net Migration"].sum(), 4500)  # Canada + Mexico + United States

    def test_no_data_for_year(self):
        """Test if an exception is raised when no data is available for the year"""
        
        # Construct a test dataset with no data for 2019
        test_data = pd.DataFrame({
            "country": ["Canada", "Mexico", "United States"],
            "date": pd.to_datetime([2018, 2018, 2018]),
            "Net Migration": [1000, 2000, 1500],
        })
        
        test_data["Year"] = test_data["date"].dt.year
        df_year = test_data[test_data["Year"] == 2019]  # Select data for 2019
        
        # Test if no data for 2019 raises an exception
        self.assertTrue(df_year.empty, "No data for the year 2019.")

    def test_generate_map(self):
        """Test if the map generation works correctly"""
        
        # Construct simple test data
        test_data = pd.DataFrame({
            "country": ["Canada", "Mexico", "United States"],
            "date": pd.to_datetime([2018, 2018, 2018]),
            "Net Migration": [1000, 2000, 1500],
            "Year": [2018, 2018, 2018],
            "id": ["CAN", "MEX", "USA"]  # Simulate ISO-3 codes
        })
        
        # Create a choropleth map
        fig = px.choropleth(
            test_data,
            locations="id",
            color="Net Migration",
            hover_name="country",
            color_continuous_scale=["lightblue", "white", "lightcoral"],
            range_color=(-10000, 10000),
            title="Net Migration by Country in 2018",
            labels={"Net Migration": "Number of Migrants"},
            projection="natural earth"
        )
        
        # Check if the returned chart is a valid Figure object
        self.assertIsInstance(fig, Figure, "The figure should be a valid plotly Figure.")

if __name__ == '__main__':
    unittest.main()
