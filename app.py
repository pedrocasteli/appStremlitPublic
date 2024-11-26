import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    file_path = "video30Min.csv"  # Replace with your local path if running locally
    return pd.read_csv(file_path)

data = load_data()
filtered_data = data[(data['funcionario'] != 'desconhecido') & (data['atividade'] != 'caixa_vazia')]

filtered_data['inicio'] = pd.to_datetime(filtered_data['inicio'])
filtered_data['fim'] = pd.to_datetime(filtered_data['fim'])
filtered_data['duracao'] = (filtered_data['fim'] - filtered_data['inicio']).dt.total_seconds() / 60  # Convert to minutes

employees = filtered_data['funcionario'].unique()
activities = filtered_data['atividade'].unique()

st.title("Atividades no posto")
st.write("19/11/2024")

data = data[data['funcionario'] != 'desconhecido']
data['inicio'] = pd.to_datetime(data['inicio'])
data['fim'] = pd.to_datetime(data['fim'])

activity_summary = data.groupby(['funcionario', 'atividade'])['duracao'].sum().reset_index()
activity_summary['duracao'] = (activity_summary['duracao'] / 60).round(2) 


arrival_departure = data.groupby('funcionario').agg(
    arrival_time=('inicio', 'min'),
    departure_time=('fim', 'max')
).reset_index()

arrival_departure.rename(
    columns={'funcionario': 'Funcionário', 'arrival_time': 'Chegada', 'departure_time': 'Saída'},
    inplace=True
)

arrival_departure['Chegada'] = arrival_departure['Chegada'].dt.strftime('%H:%M:%S')
arrival_departure['Saída'] = arrival_departure['Saída'].dt.strftime('%H:%M:%S')

activity_counts = data[data['atividade'] != 'caixa_vazio']['atividade'].value_counts()

activity_data = activity_counts.reset_index()
activity_data.columns = ['Activity', 'Frequency']

working_activities = data[data['atividade'].isin(['abastecendo', 'no_caixa'])]
working_time = working_activities.groupby('funcionario')['duracao'].sum().reset_index()
working_time['duracao'] = (working_time['duracao'] / 60).round(2)
working_time.rename(columns={'funcionario': 'Funcionário', 'duracao': 'Total trabalhado (minutos)'}, inplace=True)

st.warning('Os dados mostrados aqui podem estar incorretos.', icon="⚠️")

st.header("Horários de chegada e saída")
st.write("Essa tabela mostra o último horário de detecção de cada funcionário")
st.dataframe(arrival_departure)

st.header("Tempo trabalhado")
st.write("O tempo total que cada funcionário passou trabalhando.")
st.bar_chart(working_time.set_index('Funcionário'))

# Horizontal Bar Graph of Activity Frequency
st.header("Atividades mais frequentes")
st.write("Atividades mais frequentes durante o dia")

# Plot the horizontal bar graph
st.bar_chart(activity_data.set_index('Activity'))

# Bar Graph
st.header("Tempo por atividade")
st.write("O tempo total que cada usuário passou em cada atividade")

selected_employee = st.selectbox("Selecione um funcionário", options=["All"] + list(employees), index=0)
selected_activity = st.selectbox("Select uma atividade", options=["All"] + list(activities), index=0)

filtered_display = filtered_data.copy()
if selected_employee != "All":
    filtered_display = filtered_display[filtered_display['funcionario'] == selected_employee]
if selected_activity != "All":
    filtered_display = filtered_display[filtered_display['atividade'] == selected_activity]

grouped_data = (
    filtered_display.groupby(['funcionario', 'atividade'])['duracao']
    .sum()
    .reset_index()
    .rename(columns={'duracao': 'Total Time (minutes)'})
)

pivot_data = grouped_data.pivot(index='funcionario', columns='atividade', values='Total Time (minutes)').fillna(0)


if pivot_data.empty:
    st.write("Sem dados para os filtros passados.")
else:
    st.bar_chart(pivot_data)