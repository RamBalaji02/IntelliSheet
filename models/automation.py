import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class AutomationEngine:
    def __init__(self, dataframe):
        self.df = dataframe.copy()
    
    def highlight_low_marks(self, threshold=40):
        """
        Highlight students with marks below threshold.
        
        Args:
            threshold: Minimum acceptable marks
        
        Returns:
            DataFrame with students having low marks
        """
        # Look for columns that might contain marks/grades
        marks_columns = []
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in ['mark', 'grade', 'score', 'result', 'percentage']):
                marks_columns.append(col)
        
        if not marks_columns:
            # If no obvious marks column, look for numeric columns with reasonable range
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.df[col].between(0, 100).all():  # Typical marks range
                    marks_columns.append(col)
        
        low_marks_data = pd.DataFrame()
        
        for col in marks_columns:
            low_marks = self.df[self.df[col] < threshold]
            if not low_marks.empty:
                low_marks_data = pd.concat([low_marks_data, low_marks])
        
        return low_marks_data.drop_duplicates()
    
    def highlight_low_stock(self, threshold=10):
        """
        Highlight items with low stock levels.
        
        Args:
            threshold: Minimum acceptable stock level
        
        Returns:
            DataFrame with items having low stock
        """
        # Look for columns that might contain stock/quantity
        stock_columns = []
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in ['stock', 'quantity', 'inventory', 'available', 'units']):
                stock_columns.append(col)
        
        if not stock_columns:
            # If no obvious stock column, look for numeric columns
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.df[col].min() >= 0:  # Stock should be non-negative
                    stock_columns.append(col)
        
        low_stock_data = pd.DataFrame()
        
        for col in stock_columns:
            low_stock = self.df[self.df[col] < threshold]
            if not low_stock.empty:
                low_stock_data = pd.concat([low_stock_data, low_stock])
        
        return low_stock_data.drop_duplicates()
    
    def plot_bar_chart(self, column_name, chart_path="bar_chart.png"):
        """
        Create a bar chart for the specified column.
        
        Args:
            column_name: Name of the column to plot
            chart_path: Path to save the chart
        
        Returns:
            Path to the saved chart file
        """
        if column_name not in self.df.columns:
            raise ValueError(f"Column '{column_name}' not found in dataframe")
        
        try:
            plt.figure(figsize=(10, 6))
            
            # Check if column is numeric or categorical
            if pd.api.types.is_numeric_dtype(self.df[column_name]):
                # For numeric columns, create value counts or show distribution
                if len(self.df[column_name].unique()) <= 20:  # Discrete values
                    value_counts = self.df[column_name].value_counts().sort_index()
                    plt.bar(value_counts.index, value_counts.values)
                    plt.xlabel(column_name)
                    plt.ylabel('Frequency')
                    plt.title(f'Distribution of {column_name}')
                else:  # Continuous values - create bins
                    plt.hist(self.df[column_name].dropna(), bins=20, alpha=0.7)
                    plt.xlabel(column_name)
                    plt.ylabel('Frequency')
                    plt.title(f'Histogram of {column_name}')
            else:
                # For categorical columns, show value counts
                value_counts = self.df[column_name].value_counts()
                
                # Limit to top 15 categories for readability
                if len(value_counts) > 15:
                    value_counts = value_counts.head(15)
                    plt.title(f'Top 15 categories in {column_name}')
                else:
                    plt.title(f'Distribution of {column_name}')
                
                plt.bar(range(len(value_counts)), value_counts.values)
                plt.xlabel(column_name)
                plt.ylabel('Count')
                plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
            
            plt.tight_layout()
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            print(f"Error creating chart: {e}")
            return None
    
    def plot_pie_chart(self, column_name, chart_path="pie_chart.png"):
        """
        Create a pie chart for the specified column.
        
        Args:
            column_name: Name of the column to plot
            chart_path: Path to save the chart
        
        Returns:
            Path to the saved chart file
        """
        if column_name not in self.df.columns:
            raise ValueError(f"Column '{column_name}' not found in dataframe")
        
        try:
            plt.figure(figsize=(8, 8))
            
            # Get value counts
            value_counts = self.df[column_name].value_counts()
            
            # Limit to top 8 categories for readability
            if len(value_counts) > 8:
                other_count = value_counts.iloc[8:].sum()
                value_counts = value_counts.head(8)
                value_counts['Other'] = other_count
            
            # Create pie chart
            plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title(f'Distribution of {column_name}')
            plt.axis('equal')
            
            plt.tight_layout()
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            print(f"Error creating pie chart: {e}")
            return None
    
    def plot_line_chart(self, x_column, y_column, chart_path="line_chart.png"):
        """
        Create a line chart for two columns.
        
        Args:
            x_column: Name of the x-axis column
            y_column: Name of the y-axis column
            chart_path: Path to save the chart
        
        Returns:
            Path to the saved chart file
        """
        if x_column not in self.df.columns or y_column not in self.df.columns:
            raise ValueError(f"One or both columns not found in dataframe")
        
        try:
            plt.figure(figsize=(10, 6))
            
            # Sort by x column for proper line plotting
            sorted_df = self.df.sort_values(x_column)
            
            plt.plot(sorted_df[x_column], sorted_df[y_column], marker='o', linewidth=2, markersize=4)
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f'{y_column} vs {x_column}')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            print(f"Error creating line chart: {e}")
            return None
    
    def create_summary_statistics(self):
        """
        Create summary statistics for all numeric columns.
        
        Returns:
            DataFrame with summary statistics
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return pd.DataFrame()
        
        summary = self.df[numeric_cols].describe()
        
        # Add additional statistics
        additional_stats = pd.DataFrame(index=['skewness', 'kurtosis', 'missing_count'])
        
        for col in numeric_cols:
            additional_stats[col] = [
                self.df[col].skew(),
                self.df[col].kurtosis(),
                self.df[col].isnull().sum()
            ]
        
        summary = pd.concat([summary, additional_stats])
        
        return summary
    
    def detect_trends(self, column_name):
        """
        Detect basic trends in numeric data.
        
        Args:
            column_name: Name of the column to analyze
        
        Returns:
            Dictionary with trend information
        """
        if column_name not in self.df.columns:
            raise ValueError(f"Column '{column_name}' not found in dataframe")
        
        if not pd.api.types.is_numeric_dtype(self.df[column_name]):
            return {"error": "Column must be numeric for trend analysis"}
        
        try:
            data = self.df[column_name].dropna()
            
            if len(data) < 2:
                return {"error": "Insufficient data for trend analysis"}
            
            # Calculate basic trend metrics
            trend_info = {
                "mean": data.mean(),
                "median": data.median(),
                "std": data.std(),
                "min": data.min(),
                "max": data.max(),
                "range": data.max() - data.min(),
                "q1": data.quantile(0.25),
                "q3": data.quantile(0.75),
                "iqr": data.quantile(0.75) - data.quantile(0.25)
            }
            
            # Simple trend detection (first half vs second half)
            mid_point = len(data) // 2
            first_half = data.iloc[:mid_point]
            second_half = data.iloc[mid_point:]
            
            if len(first_half) > 0 and len(second_half) > 0:
                first_mean = first_half.mean()
                second_mean = second_half.mean()
                
                if second_mean > first_mean * 1.1:
                    trend_info["trend"] = "Increasing"
                elif second_mean < first_mean * 0.9:
                    trend_info["trend"] = "Decreasing"
                else:
                    trend_info["trend"] = "Stable"
                
                trend_info["first_half_mean"] = first_mean
                trend_info["second_half_mean"] = second_mean
                trend_info["trend_percentage"] = ((second_mean - first_mean) / first_mean) * 100 if first_mean != 0 else 0
            
            return trend_info
            
        except Exception as e:
            return {"error": f"Error in trend analysis: {str(e)}"}