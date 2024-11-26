import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('video30Min.csv')

st.title("Análise de atividades")
st.write("Dia  11/11/2024")

working_df = df[df['atividade'] != 'descansando']

# Filter out "desconhecido"
working_df = working_df[working_df['funcionario'] != 'desconhecido']

# Group by employee to calculate total duration in seconds
total_duration_by_employee = working_df.groupby('funcionario')['duracao'].sum().reset_index()

# Convert duration to minutes
total_duration_by_employee['duracao'] = total_duration_by_employee['duracao'] / 60

# Sort by duration in descending order
total_duration_by_employee = total_duration_by_employee.sort_values('duracao', ascending=False)

# Bar chart using Streamlit's native `bar_chart`
st.subheader('Tempo de trabalho por funcionário')
st.bar_chart(total_duration_by_employee, x='funcionario', y='duracao')

# Calculate average duration for each activity
average_duration_by_activity = filtered_df.groupby('atividade')['duracao'].mean().reset_index()

# Convert duration to minutes
average_duration_by_activity['duracao'] = average_duration_by_activity['duracao'] / 60

st.subheader('Average Duration of Activities (in minutes)')
st.bar_chart(average_duration_by_activity, x='atividade', y='duracao')

# Calculate minimum and maximum duration for each activity
min_duration_by_activity = filtered_df.groupby('atividade')['duracao'].min().reset_index()
max_duration_by_activity = filtered_df.groupby('atividade')['duracao'].max().reset_index()

# Display minimum and maximum durations
st.subheader('Minimum and Maximum Durations')
st.write('Minimum Durations:')
st.write(min_duration_by_activity)
st.write('Maximum Durations:')
st.write(max_duration_by_activity)