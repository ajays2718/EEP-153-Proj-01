import unittest
import pandas as pd
from plotly.graph_objs import Figure
import wbdata

class TestNetMigrationAndUrbanGrowth(unittest.TestCase):

    def test_region_summary(self):
        """Test if the regional summary (aggregation) is calculated correctly."""
        # Define regional country mapping
        regions = {
            "Asia-Pacific": ["Australia", "Bangladesh", "Brunei Darussalam", "Cambodia", "China", "Fiji", "Indonesia", "Japan",
                             "Kiribati", "Korea, Rep.", "Lao PDR", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal",
                             "New Zealand", "Pakistan", "Papua New Guinea", "Philippines", "Singapore", "Solomon Islands",
                             "Sri Lanka", "Thailand", "Timor-Leste", "Tonga", "Tuvalu", "Vanuatu", "Vietnam"]
        }

        indicators = {"SP.URB.GROW": "Urban Population Growth", "SM.POP.NETM": "Net Migration"}
        # Fetch the data
        data = wbdata.get_dataframe(indicators, country="all", parse_dates=True).dropna().reset_index()

        # Assign regions to countries
        data['Region'] = data['country'].apply(lambda x: next((region for region, countries in regions.items() if x in countries), None))

        # Aggregate data by region and year
        region_summary = (
            data.dropna(subset=["Region"])
            .assign(Year=lambda df: df['date'].dt.year)
            .groupby(["Region", "Year"])[["Urban Population Growth", "Net Migration"]].mean().reset_index()
        )

        # Test if the aggregation is correct (check if summary has expected columns)
        self.assertIn("Region", region_summary.columns, "The aggregated summary does not contain 'Region' column.")
        self.assertIn("Year", region_summary.columns, "The aggregated summary does not contain 'Year' column.")
        self.assertIn("Urban Population Growth", region_summary.columns, "The aggregated summary does not contain 'Urban Population Growth' column.")
        self.assertIn("Net Migration", region_summary.columns, "The aggregated summary does not contain 'Net Migration' column.")

if __name__ == '__main__':
    unittest.main()
