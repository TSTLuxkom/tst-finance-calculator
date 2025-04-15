import streamlit as st
import pandas as pd


def main():
    st.title("Techcom Finance Calculator")
    
    # Project type selection dropdown
    project_type = st.selectbox(
        "Select Project Type",
        ["TAS# TechCom 2025", "ESA ARTES OP/FP", "SES-TAS#5 H1 2025", "SES-TAS#6 H2 2024", "SES-TAS#7 H1 2025", "SES-TAS#8 H1 2025", "SES-TAS#9 H1 2025", "TSTLuxkom"]
    )
    # project_type = 'TAS# TechCom 2025'
    
    # File uploader
    uploaded_file = st.file_uploader("Upload Techcom Time Sheet (Excel)", type=["xlsx", "xls"])

    # File uploader 2
    uploaded_file_2 = st.file_uploader("Upload Employee/Activity Rate Sheet (Excel)", type=["xlsx", "xls"])
    
    if uploaded_file and uploaded_file_2 is not None:
        try:
            # Show success message
            st.success(f"Files uploaded successfully!")

            # Read the Excel file
            df = pd.read_excel(uploaded_file)
            employee_rates_df = pd.read_excel(uploaded_file_2)
            activity_rates_df = pd.read_excel(uploaded_file_2, sheet_name=1)

            df = df[df['Project description']== project_type] 

            # Display Hours per Activity for each Employee
            employee_activity_hours_df = df.groupby(['Employees', 'Activity'])['Duration'].sum().reset_index()

            # First, merge employee_activities with activity_rates
            employee_activity_hours_df = pd.merge(employee_activity_hours_df, activity_rates_df, on='Activity', how='left')

            # Then, merge with employee_rates
            employee_activity_hours_df = pd.merge(employee_activity_hours_df, employee_rates_df, on='Employees', how='left')

            # Compute Total cost
            employee_activity_hours_df['Total cost'] = employee_activity_hours_df['Duration'] * employee_activity_hours_df['Rate in percentage']/100 * employee_activity_hours_df['Cost per Hour']
            
            # Compute Total Cost when Activity is 'ONC' or '210015_OnCall_BD(22-08:00orSat)'
            for index, row in employee_activity_hours_df.iterrows():
                if row['Activity']=='ONC' or row['Activity']=='210015_OnCall_BD(22-08:00orSat)':
                    row['Total cost'] = row['Duration'] * row['Rate in percentage']

            # Group by Activity
            act_array, act_tot_array = [],[]
            activities = employee_activity_hours_df['Activity'].unique()
            for activity in activities:
                activity_total = employee_activity_hours_df[employee_activity_hours_df['Activity']==activity]['Total cost'].sum()
                act_array.append(activity)
                act_tot_array.append(activity_total) 
            activity_data = {
                    "Activity": act_array, "Total Cost": act_tot_array
            }
            activity_df = pd.DataFrame(activity_data) 
            st.subheader("Costs Per Activity")
            st.write(activity_df)
            st.subheader("Total Costs for all activities is "+str(activity_df['Total Cost'].sum()))

            # Group by Employee and create separate dataframes with subtotals 
            employees = employee_activity_hours_df['Employees'].unique()
            for emp in employees: 
                employee_df = employee_activity_hours_df[employee_activity_hours_df['Employees']==emp]
                subtotal = employee_df['Total cost'].sum()
                st.subheader("Costs for "+ emp +"  is "+str(subtotal))
                st.write(employee_df)
            

        except Exception as e:
            st.error(f"Error processing the file: {e}")

if __name__ == "__main__":
    main()