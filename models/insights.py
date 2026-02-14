import pandas as pd
import numpy as np

class InsightGenerator:
    def __init__(self, dataframe):
        self.df = dataframe.copy()
    
    def generate_summary(self):
        """
        Generate automatic business insights from the data.
        
        Returns:
            String containing insights about the data
        """
        insights = []
        
        # Basic dataset information
        insights.append(f"Dataset Overview:")
        insights.append(f"- Total rows: {len(self.df)}")
        insights.append(f"- Total columns: {len(self.df.columns)}")
        insights.append(f"- Column names: {', '.join(self.df.columns)}")
        
        # Data types analysis
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        
        insights.append(f"\nData Types:")
        insights.append(f"- Numeric columns: {len(numeric_cols)} ({', '.join(numeric_cols) if numeric_cols else 'None'})")
        insights.append(f"- Categorical columns: {len(categorical_cols)} ({', '.join(categorical_cols) if categorical_cols else 'None'})")
        
        # Numeric columns insights
        if numeric_cols:
            insights.append(f"\nNumeric Analysis:")
            for col in numeric_cols:
                try:
                    insights.append(f"- {col}:")
                    insights.append(f"  * Mean: {self.df[col].mean():.2f}")
                    insights.append(f"  * Median: {self.df[col].median():.2f}")
                    insights.append(f"  * Std Dev: {self.df[col].std():.2f}")
                    insights.append(f"  * Min: {self.df[col].min()}")
                    insights.append(f"  * Max: {self.df[col].max()}")
                    
                    # Identify outliers (using IQR method)
                    Q1 = self.df[col].quantile(0.25)
                    Q3 = self.df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                    
                    if len(outliers) > 0:
                        insights.append(f"  * Outliers detected: {len(outliers)} values")
                    else:
                        insights.append(f"  * No outliers detected")
                        
                except Exception as e:
                    insights.append(f"  * Error analyzing {col}: {str(e)}")
        
        # Categorical columns insights
        if categorical_cols:
            insights.append(f"\nCategorical Analysis:")
            for col in categorical_cols:
                try:
                    value_counts = self.df[col].value_counts()
                    insights.append(f"- {col}:")
                    insights.append(f"  * Unique values: {len(value_counts)}")
                    insights.append(f"  * Most common: {value_counts.index[0]} ({value_counts.iloc[0]} occurrences)")
                    
                    if len(value_counts) > 1:
                        insights.append(f"  * Second most common: {value_counts.index[1]} ({value_counts.iloc[1]} occurrences)")
                    
                    # Check for potential issues
                    if len(value_counts) > len(self.df) * 0.5:
                        insights.append(f"  * Note: High cardinality column")
                        
                except Exception as e:
                    insights.append(f"  * Error analyzing {col}: {str(e)}")
        
        # Correlation analysis for numeric columns
        if len(numeric_cols) >= 2:
            insights.append(f"\nCorrelation Analysis:")
            try:
                correlation_matrix = self.df[numeric_cols].corr()
                
                # Find strong correlations
                strong_correlations = []
                for i in range(len(correlation_matrix.columns)):
                    for j in range(i+1, len(correlation_matrix.columns)):
                        corr_value = correlation_matrix.iloc[i, j]
                        if abs(corr_value) > 0.7:  # Strong correlation threshold
                            strong_correlations.append(
                                f"{correlation_matrix.columns[i]} & {correlation_matrix.columns[j]}: {corr_value:.2f}"
                            )
                
                if strong_correlations:
                    insights.append(f"- Strong correlations found:")
                    for corr in strong_correlations:
                        insights.append(f"  * {corr}")
                else:
                    insights.append(f"- No strong correlations (>0.7) found between numeric columns")
                    
            except Exception as e:
                insights.append(f"- Error in correlation analysis: {str(e)}")
        
        # Data quality insights
        insights.append(f"\nData Quality:")
        total_missing = self.df.isnull().sum().sum()
        if total_missing > 0:
            missing_percentage = (total_missing / (len(self.df) * len(self.df.columns))) * 100
            insights.append(f"- Missing values: {total_missing} ({missing_percentage:.1f}% of total data)")
            
            # Columns with missing data
            missing_cols = self.df.columns[self.df.isnull().any()].tolist()
            for col in missing_cols:
                missing_count = self.df[col].isnull().sum()
                insights.append(f"  * {col}: {missing_count} missing values")
        else:
            insights.append(f"- No missing values detected")
        
        # Duplicate rows
        duplicate_rows = self.df.duplicated().sum()
        if duplicate_rows > 0:
            insights.append(f"- Duplicate rows: {duplicate_rows}")
        else:
            insights.append(f"- No duplicate rows detected")
        
        return "\n".join(insights)