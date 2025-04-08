import pandas as pd


class CommsCalculations:
    def __init__(self, df):
        self.df = df

    def all_tab(self):
        """return all data"""
        return self.df

    def no_email_tab(self):
        """ 
        Returns PolicyNumbers for records where [HasEmail] = 0
        """
        policy_numbers = self.df[self.df['HasEmail'] == 0]['PolicyNumber']
        return policy_numbers

    def save_to_excel(self, output_file):
        """Save query results DataFrame to an Excel file."""

        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            # All data
            all_data = self.all_tab()
            all_data.to_excel(writer, sheet_name='All_Records', index=False)

            # Format the Excel file
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                # Add filtering capability
                worksheet.autofilter(0, 0, 0, len(all_data.columns) - 1)
                # Freeze top row
                worksheet.freeze_panes(1, 0)
                
        return output_file
