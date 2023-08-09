from h2o_wave import main, site, ui, Q, app, data
from weather_predictor import run_predicion_model, get_today_weather_state, get_weather_state_day, get_monthly_data
from utils import write_dates_to_file, check_today_date_in_file, create_empty_text_file
import os
import datetime

def init(q: Q):

    q.page['meta'] = ui.meta_card(
        box='', title='Safe Take Off', layouts=[
            ui.layout(breakpoint='xs', zones=[
                ui.zone('header'),
                ui.zone('content', zones=[
                    ui.zone('summary_title'),
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

    q.page['summary_title'] = ui.form_card(box='summary_title', items=[
        ui.text_l('Average weather states for today'),
    ])

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
        ui.date_picker(name='date_picker', label='Select a Date for weather forecast'),
        ui.button(name='prediction_button', label='Predict', primary=True)
    ])


@app('/')
async def serve(q: Q):

    weather_state = q.client.state or 'temperature' 


    if not q.client.initialized:
        init(q)

        if not os.path.exists('dates.txt'):
            create_empty_text_file('dates.txt')

        if not check_today_date_in_file('dates.txt'):
            run_predicion_model()
            write_dates_to_file(datetime.datetime.now().date(), 'dates.txt')
                    
        # 
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


    if q.args.button:
        q.client.state = weather_state = q.args.state

    q.page['line_chart'] = ui.plot_card(
        box='visualization',
        title='Last 30 days average ' + weather_state + ' change',
        data=data('date ' + weather_state,
                  rows=[
                      (i['date'], round(i[weather_state],2)) for i in monthly_data
                  ]),
        plot=ui.plot([ui.mark(type='line', x_scale='time', x='=date',
                              y='='+weather_state, x_title='Date', y_title=weather_state)])

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
