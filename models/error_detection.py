import pandas as pd
import numpy as np
import re

class ErrorDetector:
    def __init__(self, dataframe):
        self.df = dataframe.copy()
    
    def detect_missing_values(self):
        """
        Detect missing values in the dataframe.
        
        Returns:
            DataFrame with missing value information
        """
        missing_data = []
        
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                missing_percentage = (missing_count / len(self.df)) * 100
                missing_data.append({
                    'Column': col,
                    'Missing Count': missing_count,
                    'Missing Percentage': f"{missing_percentage:.1f}%"
                })
        
        if missing_data:
            return pd.DataFrame(missing_data)
        else:
            return pd.DataFrame()  # Empty DataFrame if no missing values
    
    def detect_formula_inconsistencies(self):
        """
        Detect potential formula inconsistencies in Excel-like data.
        This is a simplified version that looks for patterns that might indicate formula issues.
        
        Returns:
            List of detected inconsistencies
        """
        inconsistencies = []
        
        # Check for common formula inconsistency patterns
        for col in self.df.columns:
            # Skip if column is entirely numeric (less likely to contain formulas)
            if pd.api.types.is_numeric_dtype(self.df[col]):
                continue
            
            # Look for cells that start with common Excel formula starters
            formula_starters = ['=', '+', '-', '@']
            formula_cells = self.df[col].astype(str).str.startswith(tuple(formula_starters), na=False)
            
            if formula_cells.any():
                # Check if only some cells have formulas (potential inconsistency)
                formula_count = formula_cells.sum()
                total_non_empty = self.df[col].notna().sum()
                
                if formula_count < total_non_empty and formula_count > 0:
                    inconsistencies.append({
                        'column': col,
                        'issue': 'Mixed formula and non-formula cells',
                        'details': f'{formula_count} cells with formulas, {total_non_empty - formula_count} without'
                    })
            
            # Look for potential error values
            error_patterns = [
                r'#DIV/0!', r'#N/A', r'#NAME\?', r'#NULL!', r'#NUM!', r'#REF!', r'#VALUE!',
                r'#DIV/0', r'#N/A', r'#NAME', r'#NULL', r'#NUM', r'#REF', r'#VALUE'
            ]
            
            for pattern in error_patterns:
                error_cells = self.df[col].astype(str).str.contains(pattern, case=False, na=False)
                if error_cells.any():
                    error_count = error_cells.sum()
                    inconsistencies.append({
                        'column': col,
                        'issue': f'Excel error values detected: {pattern}',
                        'details': f'{error_count} cells contain this error'
                    })
        
        # Check for data type inconsistencies within columns
        for col in self.df.columns:
            if self.df[col].dtype == 'object':  # Object columns can have mixed types
                non_null_values = self.df[col].dropna()
                
                if len(non_null_values) > 1:
                    # Check if values have different data types
                    types = set(type(x).__name__ for x in non_null_values)
                    if len(types) > 1:
                        inconsistencies.append({
                            'column': col,
                            'issue': 'Mixed data types in column',
                            'details': f'Column contains: {", ".join(types)}'
                        })
        
        # Check for outliers in numeric columns that might indicate calculation errors
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            try:
                # Use IQR method to detect extreme outliers
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR  # More extreme threshold for potential errors
                upper_bound = Q3 + 3 * IQR
                
                extreme_outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                
                if len(extreme_outliers) > 0:
                    inconsistencies.append({
                        'column': col,
                        'issue': 'Extreme outliers detected',
                        'details': f'{len(extreme_outliers)} values may indicate calculation errors'
                    })
            except:
                continue  # Skip if calculation fails
        
        return inconsistencies
    
    def detect_duplicate_rows(self):
        """
        Detect completely duplicate rows.
        
        Returns:
            DataFrame with duplicate rows
        """
        duplicates = self.df[self.df.duplicated(keep=False)]
        return duplicates
    
    def detect_data_anomalies(self):
        """
        Detect various data anomalies that might indicate errors.
        
        Returns:
            Dictionary of anomaly types and their details
        """
        anomalies = {}
        
        # Check for negative values in columns that shouldn't have them
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if any(keyword in col.lower() for keyword in ['age', 'price', 'count', 'quantity', 'stock']):
                negative_values = self.df[self.df[col] < 0]
                if len(negative_values) > 0:
                    anomalies[f'negative_{col}'] = {
                        'issue': f'Negative values in {col}',
                        'count': len(negative_values),
                        'details': f'Rows: {negative_values.index.tolist()}'
                    }
        
        # Check for unusually high values
        for col in numeric_cols:
            try:
                mean_val = self.df[col].mean()
                std_val = self.df[col].std()
                
                if std_val > 0:  # Avoid division by zero
                    # Values more than 5 standard deviations from mean
                    extreme_high = self.df[self.df[col] > mean_val + 5 * std_val]
                    if len(extreme_high) > 0:
                        anomalies[f'extreme_high_{col}'] = {
                            'issue': f'Extremely high values in {col}',
                            'count': len(extreme_high),
                            'details': f'Max value: {self.df[col].max()}, Mean: {mean_val:.2f}'
                        }
            except:
                continue
        
        return anomalies