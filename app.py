import dash
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, dash_table


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Import data
df = pd.read_csv('MOCK_DATA.csv', delimiter=',')


# Cuantos dias de clases fueron?
filtrado = df.filter(like='day').columns
cant_dias = len(filtrado)

# print('cant de dias de clases: ', cant_dias)


# Contando asistencias / inasistencias dia 1
true_d1 = (df['day1'] == True).sum()
# print("C/A dia 1: ", true_d1)
false_d1 = (df['day1'] == False).sum()
# print("C/I dia 1: ", false_d1)


# Aqui se agregan dos columnas nuevas al dataframe, que indican
# la cantidad de asistencias e inasistencias por estudiante al final del curso.
# contar cantidad de días de asistencia por estudiante
df['cant_asistencias'] = df.iloc[:, 6:36].sum(axis=1)

# contar cantidad de días de inasistencia por estudiante
df['cant_inasistencias'] = (32 - df.iloc[:, 6:36].sum(axis=1))

# print(df)
# print(df.columns)
# print(len(df.columns))


# Contando asistencia por dia


asistencias_diarias = (df.iloc[:, 4:36] == 1).astype(int).sum()
inasistencias_diarias = (df.iloc[:, 4:36] == 0).astype(int).sum()

# print("\n\nAsistencias\n")
# print(asistencias_diarias)
# print("\n\nInaistencias\n")
# print(inasistencias_diarias)

# Asignar una columna única a `asistencias_diarias`
# asistencias_diarias['fecha'] = pd.to_datetime('today')                                                         # SI ALGO DA ERROR FUE ESTA LINEA XD

df_test = pd.DataFrame(
    {'id': [0], 'first_name': [0], 'last_name': [0], 'email': [0]})
temp = pd.DataFrame(asistencias_diarias.to_frame().T)
df_test = pd.concat([df_test, temp], ignore_index=True).drop(0)

# Asignar índices únicos a `df_test`
df_test = df_test.reset_index(drop=True)

# Concatenar `df_test` al final de `df` y eliminar duplicados
df = pd.concat([df, df_test]).drop_duplicates()
df = df.reset_index(drop=True)
# Mostrar el dataframe resultante
# print(df)


# Agregando fila al final del df en la que se cuentan las asistencias por dia del grupo.
# Bloque de asistencias
# For some reason se estan agregando dos lineas de respuesta. O sea, en la 1002 y en la 1003
# Estan los mismos datos de asistencia. Se debe verificar eso.
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

asistencias_diarias = (df.iloc[:, 4:36] == 1).astype(int).sum()

# print("\n\nAsistencias\n")
# print(asistencias_diarias)

df_test = pd.DataFrame(
    {'id': [0], 'first_name': [0], 'last_name': [0], 'email': [0]})
temp = pd.DataFrame([asistencias_diarias])
df_test = df_test.append(temp, ignore_index=True).drop(0)
df_test.reset_index(drop=True, inplace=True)

df = df.append(df_test, ignore_index=True)
df.dropna(thresh=3, inplace=True)

# print(df)


# Agregando fila al final del df en la que se cuentan las asistencias por dia del grupo.
# En este bloque se cuentan inasistencias y se agregan debajo de las asistencias.
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

inasistencias_diarias = (df.iloc[:, 4:36] == 0).astype(int).sum()

# print("\n\ninasistencias\n")
# print(inasistencias_diarias)

df_test = 0
temp = 0

df_test = pd.DataFrame(
    {'id': [0], 'first_name': [0], 'last_name': [0], 'email': [0]})
temp = pd.DataFrame([inasistencias_diarias])
df_test = df_test.append(temp, ignore_index=True).drop(0)
df_test.reset_index(drop=True, inplace=True)

df = df.append(df_test, ignore_index=True)
df.dropna(thresh=3, inplace=True)

# print(df)


# Porcentaje de asistencias con respecto a la cantidad de alumnos.
no_asist = df.iloc[1001, 4:36].values
# print(no_asist)
temp = 0
por_asist = []

for x in no_asist.astype(int):
    # Divido la cantidad de asistentes enter la cantidad de alumnos * 100 para obtener el porcentaje de asistencias
    temp = (x / 1000) * 100
    por_asist.append(temp)

por_asist = np.round(por_asist, decimals=0)
# print("\n\nPorcentajes: ", por_asist)


# Porcentaje de inasistencias con respecto a la cantidad de alumnos.
por_inasist = []
temp = 0

for x in por_asist.astype(int):
    # Resto el porcentaje de asistencia al 100%, el resto es la cantidad de inasistencias.
    temp = 100 - x
    por_inasist.append(temp)

por_inasist = np.round(por_inasist, decimals=0)
# print(por_inasist)

# por_asist   ---> Porcentaje de asistencia por dia de un grupo
# por_inasist ---> Porcentaje de inasistencia por dia de un grupo
# no_asist    ---> Array con las asistencias totales por dia del grupo


# Total de asistencias contra total de inasistencias
total_asist = np.sum(asistencias_diarias.values)
total_inasist = np.sum(inasistencias_diarias.values)
# print(total_asist)
# print(total_inasist)

# asistencias_diarias.values  ---> array con las asistencias por dia del grupo
# inasistencias_diarias.values  ---> array con las inasistencias por dia del grupo
# total_asist   ---> suma de todas las asistencias del grupo al final del mes   = 16005
# total_inasist ---> suma de todas las inasistencias del grupo al final del mes = 15995

print(df.keys())


# -------------------------------- DASHBOARD -----------------------------============

# cake graph

data = {'asistencias': total_asist, 'inasistencias': total_inasist}
df_asistencias = pd.DataFrame([data])
df_asistencias_diarias = asistencias_diarias.to_frame()


#print("\n\n", type(asistencias_diarias))
# print(df_asistencias_diarias)
# asistencias_diarias = asistencias_diarias.append({'DAYS', 'ATTENDANCE'})
#print("\n\n", df_asistencias_diarias.index)
#print("\n\n", len(df_asistencias_diarias.values))
#print(df.columns)
#print("\n\n")
# --------------------------------

# Asistencias anuales


app = Dash(__name__)

# Layoutt

app.layout = html.Div(
    className='container',
    children=[

        html.Header(
            className='header',
            children=[
                    html.Link(
                        rel='stylesheet',
                        href='https://bootswatch.com/4/flatly/bootstrap.min.css'
                    ),
                html.Div(className="Header", children=[
                    html.H1(children='Dashboard de asistencia' , style= {'textAlign' : 'center', 'marginTop': '50px'}),
                    
                ])    
                
            ]
        ),

        html.Div(
            className='content',
            style={'display': 'flex', 'flex-wrap': 'wrap'},
            children=[
                html.H4(children='Porcentaje de asistencias vs porcentaje de inasistencias' , style= {'width': '100%', 'textAlign' : 'center', 'marginTop': '20px'}),
                html.Div(
                    className='chart',
                    style={'flex': '50%'},
                    children=[
                        dcc.Graph(
                            figure=px.histogram(
                                df_asistencias_diarias,
                                x=df_asistencias_diarias.index,
                                y=asistencias_diarias,
                                histfunc='max',
                                title='Asistencias Diarias',
                                labels={'x': 'Clases',
                                        'y': 'No. Asistencias diarias'},
                                color_discrete_sequence=['#0099ff']
                            ),
                            style={'height': '350px', 'width': '100%', 'flex': 'nowrap'}
                        )
                    ]
                ),
                html.Div(
                    className='chart',
                    style={'flex': '50%'},
                    children=[

                        dcc.Graph(
                            figure=px.histogram(
                                df_asistencias_diarias,
                                x=df_asistencias_diarias.index,
                                y=inasistencias_diarias,
                                histfunc='max',
                                title='Inasistencias Diarias',
                                labels={'x': 'Clases',
                                        'y': 'No. Inasistencias diarias'},
                                color_discrete_sequence=['#83072D']
                            ),
                            style={'height': '350px', 'width': '100%', 'flex': 'nowrap'}
                        )
                    ]
                ),

                html.Div(
                    className='pie',
                    style={'flex': '50%', 'marginTop': '10px'},
                    children=[
                        dcc.Graph(
                            figure=px.pie(
                                df_asistencias,
                                values=df_asistencias.values[0],
                                names=df_asistencias.columns,
                                hole=.4,
                                color_discrete_sequence=['#0099ff', '#83072D'],
                            ).update_traces(
                                hovertemplate='<b>%{label}</b><br><br>' +
                                'Asistencias: %{value}<br>' +
                                # Actualiza el formato del texto de información sobre herramientas (hover)
                                'Porcentaje: %{percent:.1%}%',
                                # Actualiza el tamaño y el color de la fuente de las etiquetas
                                textfont=dict(color='white', size=15),
                                # Agrega un borde blanco alrededor de cada sección
                                marker=dict(line=dict(color='white', width=2)),
                                # Actualiza la forma en que se muestra el texto en cada sección del pastel
                                texttemplate='%{label}<br>%{percent:.1%}%'
                            ).update_layout(
                                showlegend = False,
                                margin=dict(l=100),
                            ),
                            style={'height': '350px', 'width': '100%'},
                        )
                    ]
                ),

                html.Div(
                    className='table',
                    style={'flex': '50%'},

                    children=[
                        html.H4("Tabla de participantes", style= {'textAlign' : 'center',  'marginTop': '20px'}),
                        dash_table.DataTable(data=df.to_dict('records'),  # Ahora agregar otra columna con el no de asistencais.
                                             columns=[{'name': col, 'id': col} for col in df.iloc[:, 0:4]] + [
                                                 {'name': col, 'id': col} for col in df.iloc[:, 36:38]],
                                             style_header={
                                                 'fontWeight': 'bold', 'backgroundColor': '#0099ff', 'color': 'black'},
                                             style_cell={
                            'textAlign': 'center',
                            'padding': '8px',
                            'backgroundColor': '#f2f2f2',
                            'color': '#444444',
                            'border': '1px solid #ccc'
                        },
                            page_size=10,

                            style_data_conditional=[
                                {
                                    'if': {'column_id': 'cant_inasistencias'},
                                    'backgroundColor': '#f9dbd7',
                                    'color': 'black'
                                }
                            ]
                            
                        )
                    ]
                ),

                

            ]
        )
    ],
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
