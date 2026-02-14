import pandas as pd
import re

class TextCommandProcessor:
    def __init__(self):
        self.command_examples = [
            "filter marks > 80",
            "show students with marks above 70", 
            "create chart for marks column",
            "highlight low marks below 40",
            "filter age > 20",
            "show rows where score >= 85"
        ]
    
    def process_command(self, command_text: str, df):
        """
        Process text command and return action dict with results.
        
        Args:
            command_text: User's text command
            df: DataFrame to operate on
            
        Returns:
            Dict with action type and processed data
        """
        command = command_text.lower().strip()
        
        # Filter commands
        if any(op in command for op in ['>', '<', '>=', '<=', '==', 'above', 'below', 'greater', 'less']):
            return self._process_filter_command(command, df)
        
        # Chart commands
        elif 'chart' in command or 'plot' in command or 'graph' in command:
            return self._process_chart_command(command, df)
        
        # Highlight commands
        elif 'highlight' in command or 'mark' in command:
            return self._process_highlight_command(command, df)
        
        # Summary commands
        elif 'summary' in command or 'insights' in command or 'analyze' in command:
            return self._process_summary_command(command, df)
        
        return {"action": "unknown", "message": "Command not recognized. Try: 'filter marks > 80' or 'create chart for marks'"}
    
    def _process_filter_command(self, command, df):
        """Process filtering commands."""
        try:
            # Parse different filter patterns
            if '>' in command:
                parts = command.split('>')
                if len(parts) >= 2:
                    column = parts[0].strip().split()[-1]  # Get last word before >
                    value = float(parts[1].strip().split()[0])  # Get first number after >
                    return self._apply_filter(df, column, '>', value)
            
            elif 'above' in command:
                match = re.search(r'above (\d+)', command)
                if match:
                    value = float(match.group(1))
                    # Try to find a numeric column
                    for col in df.select_dtypes(include=['number']).columns:
                        if 'mark' in col.lower() or 'score' in col.lower():
                            return self._apply_filter(df, col, '>', value)
            
            elif 'greater than' in command:
                match = re.search(r'(\w+)\s+greater than\s+(\d+)', command)
                if match:
                    column = match.group(1)
                    value = float(match.group(2))
                    return self._apply_filter(df, column, '>', value)
                    
        except Exception as e:
            return {"action": "error", "message": f"Filter error: {str(e)}"}
        
        return {"action": "error", "message": "Could not parse filter command"}
    
    def _process_chart_command(self, command, df):
        """Process chart creation commands."""
        try:
            # Extract column name for chart
            for col in df.columns:
                if col.lower() in command:
                    return {"action": "chart", "column": col, "data": df}
            
            return {"action": "error", "message": "Column not found for chart"}
            
        except Exception as e:
            return {"action": "error", "message": f"Chart error: {str(e)}"}
    
    def _process_highlight_command(self, command, df):
        """Process highlight commands."""
        try:
            if 'low marks' in command or 'below' in command:
                match = re.search(r'below? (\d+)', command)
                if match:
                    threshold = float(match.group(1))
                    return self._highlight_low_values(df, threshold)
            
            return {"action": "error", "message": "Could not parse highlight command"}
            
        except Exception as e:
            return {"action": "error", "message": f"Highlight error: {str(e)}"}
    
    def _process_summary_command(self, command, df):
        """Process summary/insight commands."""
        try:
            summary = {
                "total_rows": len(df),
                "columns": list(df.columns),
                "numeric_columns": list(df.select_dtypes(include=['number']).columns),
                "data_types": df.dtypes.to_dict()
            }
            
            # Add basic statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['number'])
            if not numeric_cols.empty:
                summary["statistics"] = numeric_cols.describe().to_dict()
            
            return {"action": "summary", "data": summary}
            
        except Exception as e:
            return {"action": "error", "message": f"Summary error: {str(e)}"}
    
    def _apply_filter(self, df, column, operator, value):
        """Apply filter to dataframe."""
        if column not in df.columns:
            # Try to find similar column names
            similar_cols = [col for col in df.columns if column.lower() in col.lower()]
            if similar_cols:
                column = similar_cols[0]
            else:
                return {"action": "error", "message": f"Column '{column}' not found"}
        
        try:
            if operator == '>':
                filtered_df = df[df[column] > value]
            elif operator == '<':
                filtered_df = df[df[column] < value]
            elif operator == '>=':
                filtered_df = df[df[column] >= value]
            elif operator == '<=':
                filtered_df = df[df[column] <= value]
            elif operator == '==':
                filtered_df = df[df[column] == value]
            else:
                return {"action": "error", "message": f"Operator '{operator}' not supported"}
            
            return {
                "action": "filter", 
                "data": filtered_df,
                "message": f"Filtered {len(filtered_df)} rows where {column} {operator} {value}"
            }
            
        except Exception as e:
            return {"action": "error", "message": f"Filter application error: {str(e)}"}
    
    def _highlight_low_values(self, df, threshold):
        """Highlight rows with values below threshold."""
        try:
            # Find numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            highlighted_rows = []
            for col in numeric_cols:
                if 'mark' in col.lower() or 'score' in col.lower():
                    low_rows = df[df[col] < threshold]
                    if not low_rows.empty:
                        highlighted_rows.append(low_rows)
            
            if highlighted_rows:
                result = pd.concat(highlighted_rows).drop_duplicates()
                return {
                    "action": "highlight",
                    "data": result,
                    "message": f"Highlighted {len(result)} rows with values below {threshold}"
                }
            else:
                return {
                    "action": "highlight", 
                    "data": pd.DataFrame(),
                    "message": f"No values found below {threshold}"
                }
                
        except Exception as e:
            return {"action": "error", "message": f"Highlight error: {str(e)}"}
    
    def get_command_examples(self):
        """Get list of example commands."""
        return self.command_examples
