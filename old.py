#Creating the app
app = Dash(__name__)


# Grafico de las asistencias por encima y por debajo del 70% 
fig = px.bar(df, x=text, y=data, barmode = "group")


#Grafico de las asistencias por ciudades
trace = go.Scatter(x=attendance_per_city,
                   y=cities,
                   mode = 'markers',
                   marker = dict(size=4, sizemode = 'diameter'))

layout = go.Layout(title = "Grafico de asistencias por ciudades",
                  xaxis_title = "Eje x",
                  yaxis_title = "Eje y",
                  showlegend= True)

city_fig = go.Figure(data=trace, layout=layout)

app.layout = html.Div([
    dcc.Graph(figure=city_fig)
    ])


app.layout = html.Div(children=[
    html.H1(children='Learning dash app'),

    html.Div(children='''
        Porcentaje de asistencias!
    '''),
    
    # First graph
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    
    # Second graph

    html.Div(children='''
    Porcentaje de asistencias de acuerdo a la ciudad
    '''),
    dcc.Graph(
        id='example-graph-2',
        figure=city_fig
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)







meses = {}
#print(asistencias_diarias.values)
#print(total_inasist)

mes= ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

control = 7
for x in range(0,11):
    a = df.iloc[:, control]
    print(a)
    b = df.iloc[:, control+1]
    meses[mes[x]] = [a, b]
    control += 2

#print(meses)
moth = pd.DataFrame(meses)
moth.to_excel('testing.xlsx', index=False)
print("Dataframe exportado")

#print("here \n\n", df_asistencias.values)







# Asistencias anuales
# Creando tabla anual, tomando de las 32 asistencias, 24 dias y dividiendolo entre dos. De modo que dos dias representen un mes para mostrar grafico a modo de ejemplo.

# Crear una lista con los nombres de los meses
meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

# Crear un diccionario para almacenar los dataframes correspondientes a cada mes
dfs_meses = {}
asistencias_totales = {}
dfs_estadisticas_mensuales = {}

# Iterar sobre los nombres de los meses
for mes in meses:
    dfs_meses[mes] = pd.DataFrame()
    # Filtrar las columnas correspondientes al mes y unirlas en un dataframe
    df_mes = df.filter(like='DAY' + str((meses.index(mes) * 2) + 1)).join(df.filter(like='DAY' + str((meses.index(mes) * 2) + 2)))
    # Añadir el dataframe correspondiente al mes al diccionario
    dfs_meses[mes]['ASISTENCIA_' + mes.upper()] = dfs_meses[mes].iloc[:, 0] + dfs_meses[mes].iloc[:, 1]

    asistencia_mes = dfs_meses[mes].iloc[:, 0] + dfs_meses[mes].iloc[:, 1]
    dfs_meses[mes]['ASISTENCIA_' + mes.upper()] = asistencia_mes

        # Sumar la columna 'ASISTENCIA_MES' para obtener la asistencia total del mes
    asistencia_total_mes = dfs_meses[mes]['ASISTENCIA_' + mes.upper()].sum()
    # Añadir la asistencia total correspondiente al mes al diccionario
    asistencias_totales[mes] = asistencia_total_mes
    
    dfs_meses[mes]['ASISTENCIA_TOTAL'] = asistencias_totales[mes]

    df_estadisticas_mes = df[['ID', 'NOMBRE', 'APELLIDO', 'TEL', 'EMAIL', 'ASISTENCIA_' + mes.upper(), 'ASISTENCIA_TOTAL_' + mes.upper()]]

    dfs_estadisticas_mensuales[mes] = df_estadisticas_mes

print(dfs_estadisticas_mensuales['enero'])










                    children = [
                        dcc.Graph(
                            figure = px.pie(
                                df_asistencias,
                                values = df_asistencias.values[0],
                                names = df_asistencias.colums,
                                hole = .4
                                title = 'Asistencias vs Inasistencias'                            )
                        ),
                        style = {'height': '300px'}
                    )
                ]
            ),
            html.Div(
                className = 'chart',

            )
        
    dcc.Graph(figure=px.pie(df_asistencias, values=df_asistencias.values[0], names= df_asistencias.columns, hole = .4  )),

    html.Div(children='Traer tabla de asistencias', style={'color': 'blue', 'text_align': 'center', 'font_size': 14}),
    dash_table.DataTable(data=df_asistencias_diarias.to_dict('records'), page_size=5, css = 'style.custom-table'),
    dcc.Graph(figure=px.histogram(
                                df_asistencias_diarias,
                                x=df_asistencias_diarias.index,
                                y=asistencias_diarias,
                                histfunc='max',
                                title = 'Asistencias Diarias',
                                labels = {'xasis_title' : 'Clases', 'y' : 'No. Asistencias'}),
                                style = {'textAlign': 'center'})
])



#Esto le pase al bot

app = Dash(__name__)

# Layoutt

app.layout = html.Div([
    html.Div(children='PORCENTAJE TOTAL: ASISTENCIAS VS INASISTENCIAS'),
    dcc.Graph(figure=px.pie(df_asistencias, values=df_asistencias.values[0], names= df_asistencias.columns, hole = .4  )),

    html.Div(children='Traer tabla de asistencias', style={'color': 'blue', 'text_align': 'center', 'font_size': 14}),
    dash_table.DataTable(data=df_asistencias_diarias.to_dict('records'), page_size=5),
    dcc.Graph(figure=px.histogram(
                                df_asistencias_diarias,
                                x=df_asistencias_diarias.index,
                                y=asistencias_diarias,
                                histfunc='max',
                                title = 'Asistencias Diarias',
                                labels = {'xasis_title' : 'Clases', 'y' : 'No. Asistencias'}),
                                style = {'textAlign': 'center'})
])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)