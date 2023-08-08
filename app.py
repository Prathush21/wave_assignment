from h2o_wave import main, site, ui, Q, app, data
from weather_predictor import run_predicion_model, get_today_weather_state, get_weather_state_day, get_monthly_data


def init(q: Q):

    q.page['meta'] = ui.meta_card(
        box='', title='Safe Take Off', layouts=[
            ui.layout(breakpoint='xs', zones=[
                ui.zone('header'),
                ui.zone('content', zones=[
                    ui.zone('weather_summary',
                            direction=ui.ZoneDirection.ROW,
                            align='center',
                            justify='around',),
                    ui.zone('graph_form'),
                    ui.zone('visualization',
                        direction=ui.ZoneDirection.ROW),
                    ui.zone('prediction_form'),
                    ui.zone('prediction_results')

                ])
            ])
        ]
    )

    q.page['header'] = ui.header_card(
        box='header',
        title='Safe TakeOff',
        subtitle='Flakes.inc',
        image='https://previews.123rf.com/images/dedegrphc/dedegrphc1912/dedegrphc191201468/134847629-airplane-logo-template-vector-illustration-icon-design-plane-icon-vector.jpg'

    )

    q.page['graph_form'] = ui.form_card(box='graph_form', items=[
        ui.dropdown(name='state', label='Weather State', value='temperature', choices=[
            ui.choice(name='temperature', label='Temperature'),
            ui.choice(name='windspeed', label='Wind speed'),
            ui.choice(name='pressure', label='Pressure'),
            ui.choice(name='cloudcover', label='Cloud cover')
        ]),
        ui.button(name='button', label='Apply', primary=True)


    ])

    q.page['prediction_form'] = ui.form_card(box='prediction_form', items=[
        ui.date_picker(name='date_picker', label='Date'),
        ui.button(name='button', label='Predict', primary=True)
    ])


@app('/dashboard')
async def serve(q: Q):

    if not q.client.initialized:
        init(q)
        run_predicion_model()
        q.client.initialized = True
        json_data = get_today_weather_state()

        q.page['temp_card'] = ui.tall_info_card(
            box=ui.box('weather_summary', width='200px', height='200px'), name='', title='Temperature', icon='Sunny', caption=str(round(json_data['temperature'], 2)) + '°C')
        q.page['wind_card'] = ui.tall_info_card(
            box=ui.box('weather_summary', width='200px', height='200px'), name='', title='Wind Speed', icon='SwitcherStartEnd', caption=str(round(json_data['windspeed'], 2)) + ' kmph')
        q.page['pressure'] = ui.tall_info_card(
            box=ui.box('weather_summary', width='200px', height='200px'), name='', title='Pressure', icon='TestBeakerSolid', caption=str(round(json_data['pressure'], 2)) + ' Pa')
        q.page['cloud_cover'] = ui.tall_info_card(
            box=ui.box('weather_summary', width='200px', height='200px'), name='', title='Cloud Cover', icon='CloudWeather', caption=str(abs(round(json_data['cloudcover'], 2))))

    monthly_data = get_monthly_data()
    weather_state = 'temperature'

    if q.args.state:
        weather_state = q.args.state

    q.page['line_chart'] = ui.plot_card(
        box='visualization',
        title='Last 30 days average ' + weather_state + ' change',
        data=data('date ' + weather_state,
                  rows=[
                      (i['date'], i[weather_state]) for i in monthly_data
                  ]),
        plot=ui.plot([ui.mark(type='line', x_scale='time', x='=date',
                              y='='+weather_state, y_min=15, x_title='Date', y_title=weather_state)])

    )

    date = q.args.date_picker

    if date:
        weather_states = get_weather_state_day(date)
        q.page['prediction_results'] = ui.form_card(
            box='prediction_results',
            title='24 Hour Weather States',
            items=[
                ui.table(
                    name='table',
                    columns=[
                        ui.table_column(name='hour', label='Hour'),
                        ui.table_column(name='temperature',
                                        label='Temperature(°C)'),
                        ui.table_column(name='windspeed',
                                        label='Wind speed(kmph)'),
                        ui.table_column(name='pressure', label='Pressure(Pa)'),
                        ui.table_column(name='cloudcover', label='Cloud Cover')
                    ],
                    rows=[ui.table_row(name=str(weather_states[i]['hour']), cells=[
                        str(weather_states[i]['time']), str(round(weather_states[i]['temperature'], 2)), str(
                            round(weather_states[i]['windspeed'], 2)),
                        str(round(weather_states[i]['pressure'], 2)), str(
                            abs(round(weather_states[i]['cloudcover'], 2)))
                    ]) for i in range(24)]

                )
            ]
        )

    await q.page.save()