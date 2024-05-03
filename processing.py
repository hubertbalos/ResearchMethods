import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv('Results_21Mar2022.csv')

target = ['mean_ghgs', 'mean_land', 'mean_watuse', 'mean_bio']
columns_to_keep = ['sex', 'diet_group', 'age_group'] + target

df = df.drop(columns=df.columns.difference(columns_to_keep))

# Normalise
for col in target:
    max_value = df[col].max()
    df[col] = df[col] / max_value

# New evaluation variable
df['net_impact'] = df[target].sum(axis=1) / len(target)

# Define the mappings for age groups
age_group_mapping = {
    '20-29': 'young',
    '30-39': 'young',
    '40-49': 'middle_aged',
    '50-59': 'middle_aged',
    '60-69': 'elderly',
    '70-79': 'elderly'
}
df['age_group'] = df['age_group'].replace(age_group_mapping)

# Group the DataFrame by 'diet_group' and 'age_group'
grouped = df.groupby(['diet_group', 'age_group'])

# Calculate the sum of net impact values for males and females within each group
sum_male = grouped['net_impact'].transform(lambda x: x[df['sex'] == 'male'].sum())
sum_female = grouped['net_impact'].transform(lambda x: x[df['sex'] == 'female'].sum())

# Calculate the difference in the sum of net impact values between males and females within each group
net_impact_difference = sum_male - sum_female
df['Sex Impact Difference'] = net_impact_difference

# Treemap
fig = px.treemap(df, path=[px.Constant("world"), 'diet_group', 'age_group'], values='net_impact',
                  color='Sex Impact Difference',
                  color_continuous_scale='RdBu_r',
                  color_continuous_midpoint=0)
fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
fig.show()