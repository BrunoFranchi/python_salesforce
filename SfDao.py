from simple_salesforce import Salesforce, SalesforceLogin
from servicos_sales import Servico
import pandas as pd

class MyOrg:

    def start_conection_sf(self, login="brunof@gmail.com", senha="Franchi3236", token="orZOSooDM3fujIeoVxS96pF8",  sf=''):
        self.login = login
        self.senha = senha
        self.token = token
        self.sf = sf
        session_id, instance = SalesforceLogin(self.login, self.senha,
                                               security_token=self.token)  # Linha obrigatória para conectar ao sslesforce
        self.sf = Salesforce(instance=instance, session_id=session_id)

    def query_from_salesforce(self):
        self.queryOutput = self.sf.bulk.Servico_Cadastrado__c.query("SELECT Servico__c, Valor__c, Duracao__c FROM Servico_Cadastrado__c")  #Comando para obter os dados do Objeto Salesforce
        self.queryDts = self.sf.bulk.Tudo__c.query("SELECT Data_do_Atendimento__c, Horario__c FROM Tudo__c ")
        self.queryEvent = self.sf.bulk.Event.query("SELECT ActivityDateTime, Subject FROM Event ")


    def create_dataframe(self):
        self.plan = pd.DataFrame(self.queryOutput)
        self.dts = pd.DataFrame(self.queryDts)
        self.dts.drop(columns=['attributes'],inplace=True)

    def activityDateTime_subject(self):
        self.evt = pd.DataFrame(self.queryEvent)
        self.evt['ActivityDateTime'] = self.evt['ActivityDateTime'].astype('datetime64[ms]')
        self.evt.drop(columns=['attributes'],inplace=True)


        self.mylistdate = []
        self.mylistsub = []

        for j, evtdate in enumerate(self.evt['ActivityDateTime']):
            self.mylistdate.append(evtdate)

        for sub, evtsub in enumerate(self.evt['Subject']):
            self.mylistsub.append(evtsub)

        #for i in range(len(self.evt['ActivityDateTime'])):
         #   print(f'Nome: {self.mylistsub[i]} - Horário agendado: {self.mylistdate[i]}')

    def data_do_atendimento__c_horario__c_(self):
        self.all_days =[]
        self.all_time =[]
        sf_days_time =[]
        #data = pd.to_datetime('20:00:00').time().replace(tzinfo=utc)


        for sf_schedule in self.dts['Data_do_Atendimento__c']:
            self.all_days.append(sf_schedule)

        for sf_time_schedule in self.dts['Horario__c']:
            self.all_time.append(pd.to_datetime(sf_time_schedule).time())  # Se eu deixar apenas to_datetime, pegarei a data de hoje mais o horario salvo, o .time do final, pega apenas o horario
            #print(all_time)

    def chek_time(self):

        '''
        for sf_dt in range(len(all_days)):
            sf_days_time.append(Scheduling(all_days[sf_dt], all_time[sf_dt].replace(tzinfo=utc)))
            #print(f'{sf_days_time[sf_dt].data } - {sf_days_time[sf_dt].horario}')
            #if sf_days_time[sf_dt].horario > data:
            #    print(f'{sf_days_time[sf_dt].horario} --- é maior {data}')
            #else:
            #   print(f'{sf_days_time[sf_dt].horario} --- é menor {data}')
        #print(f'{sf_days_time[0].data} -- {sf_days_time[0].horario}')
        '''

    def servico__c_valor__c_duracao__c (self):
        self.list_ser = []
        self.list_value = []
        self.list_duracao = []

        for serv in self.plan['Servico__c']:
            self.list_ser.append(serv)

        for value in self.plan['Valor__c']:
            self.list_value.append(value)

        for duracao in self.plan['Duracao__c']:
            self.list_duracao.append(pd.to_datetime(duracao, ).time())

        self.v_s_d = []
        for i in range(len(self.list_ser)):
            self.v_s_d.append(Servico(self.list_ser[i], self.list_value[i], self.list_duracao[i]))
        return self.v_s_d