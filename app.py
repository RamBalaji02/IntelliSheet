import streamlit as st
import pandas as pd
import os
from models.filtering import SmartFilter
from models.text_commands import TextCommandProcessor
from models.insights import InsightGenerator
from models.error_detection import ErrorDetector
from models.automation import AutomationEngine

# Controller

def main():
    st.title("IntelliSheet - AI Powered Spreadsheet Assistant")

    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    # Only show features if file is uploaded
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("### Uploaded Data", df)
            
            # Store dataframe in session state
            st.session_state.df = df
            st.session_state.file_uploaded = True
            
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
            st.session_state.file_uploaded = False
    
    # Check if file is uploaded before showing features
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    
    if st.session_state.file_uploaded and 'df' in st.session_state:
        df = st.session_state.df

        # Smart Filtering
        st.sidebar.header("Smart Filtering")
        conditions = []
        add_condition = st.sidebar.checkbox("Add filter condition")
        while add_condition:
            filter_col = st.sidebar.selectbox("Select column to filter", df.columns, key=f"col_{len(conditions)}")
            filter_op = st.sidebar.selectbox("Select operator", ['>', '<', '==', '!=', '>=', '<='], key=f"op_{len(conditions)}")
            filter_val = st.sidebar.text_input("Value to compare", key=f"val_{len(conditions)}")
            conditions.append((filter_col, filter_op, filter_val))
            add_condition = st.sidebar.checkbox("Add another condition", key=f"add_cond_{len(conditions)}")

        logic = st.sidebar.selectbox("Logic for multiple conditions", ['AND', 'OR'])

        if st.sidebar.button("Apply Filter"):
            try:
                # Convert values to appropriate types
                parsed_conditions = []
                for col, op, val in conditions:
                    if val.replace('.', '', 1).isdigit():
                        val = float(val)
                    parsed_conditions.append((col, op, val))

                sf = SmartFilter(df)
                filtered_df = sf.apply_filter(parsed_conditions, logic)
                st.write("### Filtered Data", filtered_df)
                sf.save_to_excel(filtered_df, "filtered_output.xlsx")
                st.success("Filtered file saved as filtered_output.xlsx")
                st.download_button("Download Filtered Excel", data=open("filtered_output.xlsx", "rb"), file_name="filtered_output.xlsx")
            except Exception as e:
                st.error(f"Error applying filter: {e}")

        # Text Command Section
        st.sidebar.header("Text Commands")
        
        # Initialize text command processor
        tcp = TextCommandProcessor()
        
        # Show command examples
        with st.sidebar.expander("Command Examples"):
            for example in tcp.get_command_examples():
                st.code(example)
        
        # Command input
        command_input = st.sidebar.text_input(
            "Enter command:",
            placeholder="e.g., filter marks > 80",
            help="Type your command and press Enter"
        )
        
        # Process command button
        if st.sidebar.button("Execute Command") or command_input:
            if command_input.strip():
                if 'df' not in st.session_state:
                    st.sidebar.error("Please upload an Excel file first!")
                    return
                    
                with st.sidebar:
                    with st.spinner("Processing command..."):
                        try:
                            result = tcp.process_command(command_input, df)
                            
                            if result["action"] == "filter":
                                st.success(result["message"])
                                st.write("### Filtered Results", result["data"])
                                
                                # Save filtered results
                                result["data"].to_excel("filtered_results.xlsx", index=False)
                                st.download_button(
                                    "Download Filtered Excel",
                                    data=open("filtered_results.xlsx", "rb").read(),
                                    file_name="filtered_results.xlsx"
                                )
                            
                            elif result["action"] == "chart":
                                st.success(f"Creating chart for {result['column']}...")
                                ae = AutomationEngine(df)
                                chart_path = ae.plot_bar_chart(result["column"])
                                if chart_path:
                                    st.write(f"### Chart for {result['column']}")
                                    st.image(chart_path)
                            
                            elif result["action"] == "highlight":
                                st.info(result["message"])
                                if not result["data"].empty:
                                    st.write("### Highlighted Rows", result["data"])
                            
                            elif result["action"] == "summary":
                                st.success("Analysis complete!")
                                st.write("### Data Summary")
                                st.json(result["data"])
                            
                            elif result["action"] == "error":
                                st.error(result["message"])
                            
                            elif result["action"] == "unknown":
                                st.warning(result["message"])
                                
                        except Exception as e:
                            st.error(f"Error processing command: {str(e)}")
            else:
                st.sidebar.warning("Please enter a command!")


        else:
        # Show message when no file is uploaded
        st.info("👆 Please upload an Excel file to get started")
        
        # Show command examples even without file
        st.sidebar.header("Text Commands")
        tcp = TextCommandProcessor()
        with st.sidebar.expander("Command Examples"):
            for example in tcp.get_command_examples():
                st.code(example)
        
        st.sidebar.info("💡 Upload an Excel file above to enable all features")


if __name__ == '__main__':
    main()
