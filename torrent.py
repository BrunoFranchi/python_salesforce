from selenium import webdriver

class Downloads:
    def __init__(self, nome=False):
        self.nome = nome
        self.links = 'http://www.filmesviatorrents.info/'
        self.escolhido = input('Faça sua busca: ')
        self.nome = self.escolhido
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        self.driver.implicitly_wait(10)
        self.driver.get(self.links)
        self.driver.implicitly_wait(3)
        self.searching = self.driver.find_element_by_name('s').click()
        self.write = self.driver.find_element_by_name('s')
        self.write.send_keys(self.nome)
        self.write = self.driver.find_element_by_name('s').submit()
        self.driver.implicitly_wait(3)
        for c in range(5, 10):
            parcial_xpath = (f'//*[@id="mainWrapper"]/div/div[{c}]/h2/a')
            results = []
            try:
                results.append(self.driver.find_element_by_xpath(parcial_xpath).text)
                print(results)
            except:
                print('--')


class FilmesTorrent(Downloads):
    def __init__(self, nome=False):
        super().__init__(nome)


class SeriesTorrent(Downloads):
    def __init__(self, nome=False, temporada=False):
        super().__init__(nome)
        self.temporada = temporada
        print('--s--')


#baixar_Filme = Downloads()
#baixar_Serie = SeriesTorrent()
