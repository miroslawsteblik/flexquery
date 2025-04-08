import pandas as pd


class SmartpathCommsCalculations:
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