# TST Finance Calculator

## Overview
A Streamlit application for calculating financial costs for TST projects based on employee timesheet data and rate information.

## Requirements
- Python 3.6+
- Streamlit
- Pandas

## Installation
```bash
pip install streamlit pandas
```

## How to Run
1. Open a terminal and navigate to the directory containing the script
3. Run the application using Streamlit:
   ```bash
   streamlit run main.py
   ```
4. A browser window will open with the application interface

## Usage Instructions
1. Select the project type from the dropdown menu
2. Upload the timesheet Excel file
3. Upload the employee/activity rate Excel file
4. View the calculated costs per activity
5. View the detailed breakdown of costs per employee

## Special Calculation Notes
- For regular activities, costs are calculated as: `Duration × Rate percentage × Cost per Hour`
- For 'ONC' or '210015_OnCall_BD(22-08:00orSat)' activities, costs are calculated differently: `Duration × Rate percentage`
