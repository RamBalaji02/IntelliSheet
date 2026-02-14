import streamlit as st
import pandas as pd
import os
from models.filtering import SmartFilter
from models.voice_commands import VoiceCommandProcessor
from models.insights import InsightGenerator
from models.error_detection import ErrorDetector
from models.automation import AutomationEngine

# Controller

def main():
    st.title("IntelliSheet - AI Powered Spreadsheet Assistant")

    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("### Uploaded Data", df)

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

        # Voice Command Section
        st.sidebar.header("Voice Commands")
        
        # Initialize session state for voice command
        if 'listening' not in st.session_state:
            st.session_state.listening = False
            st.session_state.command_result = None
        
        # Show voice command status
        vcp = VoiceCommandProcessor()
        st.sidebar.info(vcp.get_status_message())
        
        # Voice command button with status
        if st.sidebar.button("🎤 Start Voice Command", 
                           disabled=st.session_state.listening,
                           help="Click and speak your command"):
            st.session_state.listening = True
            st.session_state.command_result = None
            
            # Show recording status
            with st.sidebar:
                status = st.empty()
                status.info("🎤 Listening... Speak now")
                
                try:
                    # Process voice command
                    command_text = vcp.listen_and_recognize()
                    
                    if command_text:
                        status.success("✅ Processing command...")
                        st.session_state.command_result = {
                            'text': command_text,
                            'action': vcp.process_command(command_text)
                        }
                    else:
                        status.warning("🔇 No speech detected. Please try again.")
                        
                except Exception as e:
                    status.error(f"❌ Error processing voice command: {str(e)}")
                    st.error(f"Error: {str(e)}")
                finally:
                    st.session_state.listening = False
                    st.rerun()
        
        # Display command results
        if st.session_state.command_result:
            result = st.session_state.command_result
            st.sidebar.write("### Last Command")
            st.sidebar.write(f"**You said:** {result['text']}")
            
            # Process the command
            action = result['action']
            if action["action"] == "filter":
                try:
                    sf = SmartFilter(df)
                    filtered_df = sf.apply_filter(action["conditions"], action["logic"])
                    st.sidebar.success("✅ Filter applied successfully!")
                    st.write("### Filtered Data (Voice Command)", filtered_df)
                except Exception as e:
                    st.sidebar.error(f"❌ Error applying filter: {str(e)}")
                    
            elif action["action"] == "chart":
                try:
                    ae = AutomationEngine(df)
                    chart_path = ae.plot_bar_chart(action["column"])
                    if chart_path and os.path.exists(chart_path):
                        st.sidebar.success("✅ Chart generated successfully!")
                        st.write(f"### Bar Chart for {action['column']}")
                        st.image(chart_path)
                    else:
                        st.sidebar.error("❌ Failed to generate chart")
                except Exception as e:
                    st.sidebar.error(f"❌ Error creating chart: {str(e)}")
                    
            elif action["action"] == "unknown":
                st.sidebar.warning("⚠️ Command not recognized. Try saying things like 'show students above 80' or 'create bar chart for marks'")
        
        # Voice Command Help
        with st.sidebar.expander("Voice Command Examples"):
            st.markdown("""
            **Try saying:**
            - "Show students above 80"
            - "Create bar chart for marks"
            - "Filter where age greater than 20"
            
            **Note:** Make sure your microphone is connected and you're in a quiet environment.
            """)


        # Automatic Insights
        st.header("Automatic Insights")
        ig = InsightGenerator(df)
        insights = ig.generate_summary()
        st.text_area("Insights", insights, height=150)

        # Error Detection
        st.header("Error Detection")
        ed = ErrorDetector(df)
        missing = ed.detect_missing_values()
        inconsistencies = ed.detect_formula_inconsistencies()
        if not missing.empty:
            st.error(f"Missing Values Detected:\n{missing}")
        else:
            st.success("No missing values detected.")
        if inconsistencies:
            st.error(f"Inconsistencies Detected:\n{inconsistencies}")
        else:
            st.success("No inconsistencies detected.")

        # Automation Rules
        st.header("Automation Rules")
        ae = AutomationEngine(df)
        low_marks = ae.highlight_low_marks()
        if not low_marks.empty:
            st.warning(f"Marks below threshold:\n{low_marks}")

        low_stock = ae.highlight_low_stock()
        if not low_stock.empty:
            st.warning(f"Stock below threshold:\n{low_stock}")

        # Bar Chart
        chart_col = st.selectbox("Select column for bar chart", df.columns)
        if st.button("Create Bar Chart"):
            ae.plot_bar_chart(chart_col)
            st.image("bar_chart.png")


if __name__ == '__main__':
    main()
