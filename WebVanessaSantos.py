from simple_salesforce import Salesforce, SalesforceLogin #[ Necessário importar para conectar a minha ORG do salesforce
from flask import Flask, render_template, request, redirect, session, flash
import pandas as pd
import numpy as np
from datetime import date
import datetime
import pytz

from SfDao import MyOrg
dao = MyOrg()

from servicos_sales import Days_year


dao.start_conection_sf()
dao.query_from_salesforce()
dao.create_dataframe()
dao.activityDateTime_subject()
#dao.servico__c_valor__c_duracao__c() ---- como já estou chamndo esse metodo lá no flask, não preciso chamar aqui novamente
utc=pytz.UTC


first_horario = datetime.timedelta(hours=8, minutes=00, seconds=00)
intervalo = datetime.timedelta(hours=00, minutes=15, seconds=00)
last_horario = datetime.timedelta(hours=18, minutes=00, seconds=00)
horario_comercial=[]
record= datetime.timedelta(hours=00, minutes=00, seconds=00)
list_comercial=[]

while record < last_horario:
    first_horario = first_horario + intervalo
    record = first_horario
    list_comercial.append(f'Cone{pd.to_timedelta(record)}')

#data = {'Servico__c': 'Corrente Russa', 'Valor__c': '1000'}
#sf.Servico_Cadastrado__c.create(data)                                                                        #Criando no objeto Servico_Cadastrado__c  Salesforce


app = Flask(__name__)
app.secret_key = 'Bru'

@app.route('/')
def index():
    return render_template('homePage.html', t1='Escolha o serviço desejado', obj=dao.servico__c_valor__c_duracao__c())

@app.route('/services', methods=['GET','POST' ])
def services():
    serv_selected = request.args.get('type')
    Value_selected = request.args.get('id')
    duracbao_do_servico = request.args.get('name')


    return render_template('Agendamento.html',dur=duracbao_do_servico, selecao=serv_selected, val=Value_selected)

@app.route('/valid', methods=['GET','POST' ])
def valid():
    all_year = pd.DataFrame(pd.date_range(start="2021-01-01", end="2021-12-31").to_pydatetime().tolist())
    all_year_list = []
    data_atual = date.today()
    all_year[0] = all_year[0].astype('datetime64')
    corrente = []
    for y, z in enumerate(all_year[0]):
        all_year_list.append(pd.to_datetime(z))
        if all_year_list[y] >= data_atual:
            corrente.append(all_year_list[y])

    days_html = []
    for d in range(len(corrente)):
        days_html.append(Days_year(corrente[d].date()))
    day_selected = request.args.get('type')
    return render_template('Horario.html', day_sel=day_selected)


app.run(debug=True)

#<a href = "{{ url_for('services', type='{{p.servico}}')}}" >