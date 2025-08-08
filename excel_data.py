import  pandas as pd


def extract_household_data(file_path):
    # Load the 'Data' sheet
    df = pd.read_excel(file_path, sheet_name='Data', skiprows=2)

    # Focus on relevant columns
    df = df.iloc[:, [0, 1, 3, 5, 7, 9]]  # Columns: Label, Total, Married-couple, Male, Female, Nonfamily
    df.columns = [
        'Label',
        'Total_Households',
        'Married_Couple',
        'Male_Householder',
        'Female_Householder',
        'Nonfamily_Household'
    ]

    # Drop rows with NaN labels
    df = df.dropna(subset=['Label'])

    # Clean up columns
    for col in df.columns[1:]:
        df[col] = df[col].str.replace(",", "").str.replace("±.*", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Filter relevant labels
    relevant_labels = [
        'Total households',
        'Average household size',
        'Total families',
        'Married-couple family household',
        'Male householder, no spouse present',
        'Female householder, no spouse present',
        'Nonfamily household'
    ]
    df = df[df['Label'].isin(relevant_labels)]

    # Pivot the data for easier integration
    df = df.set_index('Label').T.reset_index()
    df.rename(columns={'index': 'Category'}, inplace=True)

    return df

# Process the Excel file for household data
household_data = extract_household_data("ACSST1Y2023.S1101-2024-12-07T234848.xlsx").to_csv("household_data.csv")

