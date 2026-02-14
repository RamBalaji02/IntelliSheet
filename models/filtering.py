import pandas as pd
import os

class SmartFilter:
    def __init__(self, dataframe):
        self.df = dataframe.copy()
    
    def apply_filter(self, conditions, logic='AND'):
        """
        Apply filter conditions to the dataframe.
        
        Args:
            conditions: List of tuples (column, operator, value)
            logic: 'AND' or 'OR' for combining multiple conditions
        
        Returns:
            Filtered DataFrame
        """
        if not conditions:
            return self.df
        
        mask = None
        
        for i, (column, operator, value) in enumerate(conditions):
            if column not in self.df.columns:
                raise ValueError(f"Column '{column}' not found in dataframe")
            
            # Create condition mask
            if operator == '>':
                condition_mask = self.df[column] > value
            elif operator == '<':
                condition_mask = self.df[column] < value
            elif operator == '>=':
                condition_mask = self.df[column] >= value
            elif operator == '<=':
                condition_mask = self.df[column] <= value
            elif operator == '==':
                condition_mask = self.df[column] == value
            elif operator == '!=':
                condition_mask = self.df[column] != value
            else:
                raise ValueError(f"Unsupported operator: {operator}")
            
            # Combine with logic
            if i == 0:
                mask = condition_mask
            elif logic == 'AND':
                mask = mask & condition_mask
            elif logic == 'OR':
                mask = mask | condition_mask
            else:
                raise ValueError(f"Unsupported logic: {logic}")
        
        return self.df[mask]
    
    def save_to_excel(self, dataframe, filename):
        """Save filtered dataframe to Excel file."""
        try:
            dataframe.to_excel(filename, index=False)
            return True
        except Exception as e:
            print(f"Error saving to Excel: {e}")
            return False