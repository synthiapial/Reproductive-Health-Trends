import pandas as pd
import numpy as np

df = pd.read_csv('art_data.csv')

print(df.shape)
print(df.columns)
print(df.head())
print(df.info())
print(df.describe())

# Show all column names
print(df.columns.tolist())
#drop unnecessary columns
columns_to_drop = [
'LocationAbbr',
    'MedicalDirector',
    'Address',
    'ZipCode',
    'Phone',
    'Clinic Status',
    'Filter',
    'Breakout_Category',
    'Data_Value_num',
    'Data_Value_Footnote_Symbol',
    'Data_Value_Footnote',
    'ClinicId',
    'TypeId',
    'TopicId',
    'QuestionId',
    'FilterId',
    'BreakOutCategoryId',
    'BreakOutId'
]
#rename columns
df.rename(columns={
    'LocationDesc': 'State',
    'FacilityName': 'Clinic',
    'Type': 'Cycle Type',
    'Topic': 'Metric Category',
    'Question': 'Metric',
    'Breakout': 'Age Group',
    'Data_Value': 'Success Rate (%)',
    'Cycle_Count': 'Cycle Count',
    'GeoLocation': 'Geo Location'
}, inplace=True)

# Remove rows where 'Success Rate (%)' is not a number
df = df[df['Success Rate (%)'].str.rstrip('%').str.replace('.', '', 1).str.isnumeric()]

# convert to float
df['Success Rate (%)'] = df['Success Rate (%)'].str.rstrip('%').astype(float)

print(df.isnull().sum())
df.dropna(subset=['Success Rate (%)'], inplace=True)
df.drop(columns=['Data_Value_Footnote_Symbol', 'Data_Value_Footnote'], inplace=True)

#split into latitude and longitude
df[['Longitude', 'Latitude']] = df['Geo Location'].str.extract(r'POINT \(([-\d.]+) ([-\d.]+)\)').astype(float)

#summarize data
summary = df.groupby(['Age Group']).agg({
    'Success Rate (%)': 'mean',
    'Cycle Count': 'sum'
}).reset_index()

print(summary)

# Replace odd characters like en dash (–) with hyphen (-)
df['Age Group'] = df['Age Group'].str.replace('–', '-', regex=False).str.strip()

#visualize in python
import matplotlib.pyplot as plt

summary = df.groupby('Age Group').agg({
    'Success Rate (%)': 'mean'
}).sort_values('Success Rate (%)', ascending=False)

summary.plot(kind='bar', legend=False)
plt.title('Average ART Success Rate by Age Group')
plt.ylabel('Success Rate (%)')
plt.xlabel('Age Group')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#save the cleaned data
#summary.to_csv('art_summary_data.csv', index=False)

summary = df.groupby('Age Group').agg({
    'Success Rate (%)': 'mean',
    'Cycle Count': 'sum'
}).reset_index()

summary.to_csv('art_summary_data.csv', index=False)

