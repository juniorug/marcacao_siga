import time
import unittest

import self as self
import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

tem_horario = False

def beep():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 5000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
def start_chrome():
    #driver_path = 'driver/chromedriver'  # ou o caminho para o driver do navegador que você está usando
    #driver_path = 'C:/driver/chromedriver'  # ou o caminho para o driver do navegador que você está usando

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Opcional: maximizar a janela do navegador

    # Inicializar o navegador Chrome
    driver = webdriver.Chrome(options=options)
    return start_siga(driver)

def start_siga(driver):
    # URL do site
    url = 'https://siga.marcacaodeatendimento.pt/Marcacao/MarcacaoInicio'

    # Abrir a URL no navegador
    driver.get(url)
    return driver

def close_chrome():
    driver.quit()


def iniciar_agendamento():
    iniciar_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'btn-entidade-assunto'))
    )

    # Clicar no botão "Iniciar"
    iniciar_button.click()

    # print("Botão 'Iniciar' clicado com sucesso!")


def insere_texto_pesquisa():
    # Aguardar até que o campo de pesquisa seja visível na página
    pesquisa_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'tbPesquisa'))
    )

    # Inserir o texto "renovação de residencia" no campo de pesquisa
    pesquisa_input.send_keys("Autorização de residência") #Residence permit

    # print("Texto inserido com sucesso no campo de pesquisa!")


def seleciona_pesquisar():
    # Localizar o botão de pesquisa pelo ID
    pesquisar_assunto_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'btnPesquisarAssunto'))
    )

    # Clicar no botão de pesquisa
    pesquisar_assunto_button.click()

    # print("Botão de pesquisa clicado com sucesso!")


def seleciona_resultado_pesquisa():
    # elemento do botao de resultado da pesquisa
    selecionar_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'btn-pesquisa-results'))
    )

    # Clicar no botão de seleção
    selecionar_button.click()

    # print("Botão selecionar clicado com sucesso!")


def avanca_pagina_intermediaria():
    # Aguardar até que o botão 'proximoButton' seja visível
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    next_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Próximo')]"))
    )

    # Clicar no botão 'proximoButton'
    next_button.click()

    # print("Botão 'Próximo' clicado com sucesso!")


def seleciona_distrito(p_distrito):
    # Aguardar até que o elemento 'IdDistrito' seja visível
    id_distrito_select = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'IdDistrito'))
    )

    select = Select(id_distrito_select)
    select.select_by_visible_text(p_distrito)

    # print('Opção para distrito ' + p_distrito + ' selecionada com sucesso!')


def seleciona_localidade(p_localidade):
    id_localidade = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'IdLocalidade'))
    )

    select = Select(id_localidade)
    time.sleep(1)
    select.select_by_visible_text(p_localidade)
    # print('Opção para localidade ' + p_localidade + ' selecionada com sucesso!')


def seleciona_local_atendimento(p_local_atendimento):
    # Aguardar até que o elemento 'IdLocalAtendimento' seja visível
    id_local_atendimento_select = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'IdLocalAtendimento'))
    )

    select_local_atendimento = Select(id_local_atendimento_select)
    time.sleep(1)
    select_local_atendimento.select_by_visible_text(p_local_atendimento)

    # print('Opção local de atendimento' + p_local_atendimento + ' selecionada com sucesso!')


def avanca_para_ultima_pagina():
    last_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Próximo')]"))
    )

    # Clicar no botão 'proximoButton'
    last_button.click()
    # print("Botão 'Próximo' clicado com sucesso!")


def valida_message_error(local):
    global tem_horario
    # Aguardar até que o elemento seja visível
    error_message_div = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'error-message'))
    )

    h5_element = error_message_div.find_element(By.TAG_NAME, 'h5')

    # Imprimir a mensagem com base na presença do elemento
    if h5_element.text == "Não existem horários de marcação disponíveis para os critérios selecionados.":
        print("Não há horários em " + local)
        tem_horario = False
    else:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EXISTE HORÁRIO EM " + local)
        tem_horario = True
        while True:
           beep()
           time.sleep(5)
    time.sleep(3)


# Cenários de teste
def verifica_localidade(p_distrito, p_localidade, p_local_atendimento):
    print('------ ' + p_distrito + ' / ' + p_localidade + ' / ' + p_local_atendimento + ' ------')
    # beep()
    start_siga(driver)
    iniciar_agendamento()
    insere_texto_pesquisa()
    seleciona_pesquisar()
    seleciona_resultado_pesquisa()
    avanca_pagina_intermediaria()
    seleciona_distrito(p_distrito)
    seleciona_localidade(p_localidade)
    seleciona_local_atendimento(p_local_atendimento)
    avanca_para_ultima_pagina()
    valida_message_error(p_localidade)
    print('')


lista_de_locais = [
    ('AVEIRO','TODAS AS LOCALIDADES','Todos os Locais de Atendimento'),
    ('AVEIRO','AVEIRO','Loja de Cidadão Aveiro'),
    ('AVEIRO','ESPINHO','CRC Espinho'),
    ('BRAGANÇA','BRAGANÇA','ER Bragança'),
    ('CASTELO BRANCO','CASTELO BRANCO','Loja de Cidadão Castelo Branco'),
    ('COIMBRA','COIMBRA','Loja de Cidadão Coimbra'),
    ('ÉVORA','ÉVORA','ER Évora'),
    ('FARO','TODAS AS LOCALIDADES','Todos os Locais de Atendimento'),
    ('FARO','FARO','Loja de Cidadão Faro'),
    ('FARO','PORTIMÃO','CRC Portimão'),
    ('FARO','TAVIRA','Loja de Cidadão Tavira'),
    ('GUARDA','GUARDA','Loja de Cidadão Guarda'),
    ('ILHA DO FAIAL','HORTA','CRCPCom Horta'),
    ('LEIRIA','TODAS AS LOCALIDADES','Todos os Locais de Atendimento'),
    ('LEIRIA','LEIRIA','Loja de Cidadão Leiria'),
    ('LEIRIA','MARINHA GRANDE','Registos Marinha Grande'),
    ('LISBOA','TODAS AS LOCALIDADES','Todos os Locais de Atendimento'),
    ('LISBOA','CASCAIS','CRC Cascais'),
    ('LISBOA','LISBOA','DIC Boa Hora'),
    ('LISBOA','LISBOA','DIC Lisboa (Expo)'),
    ('LISBOA','LISBOA','Loja de Cidadão Marvila'),
    ('LISBOA','LISBOA','Loja de Cidadão Saldanha'),
    ('LISBOA','ODIVELAS','Loja de Cidadão Odivelas'),
    ('PORTALEGRE','PORTALEGRE','ER Portalegre'),
    ('PORTO','TODAS AS LOCALIDADES','Todos os Locais de Atendimento'),
    ('PORTO','PORTO','Loja de Cidadão Porto'),
    ('PORTO','POVOA DE VARZIM','ER Póvoa de Varzim'),
    ('SANTARÉM','SANTARÉM','ER Santarém'),
    ('VIANA DO CASTELO','VIANA DO CASTELO','CRC Viana do Castelo'),
    ('VILA REAL','VILA REAL','Loja de Cidadão Vila Real'),
    ('VISEU','VISEU','Loja de Cidadão Viseu')
]

while True:
    try:
        driver = start_chrome()
        while not tem_horario:
            for distrito, localidade, local_atendimento in lista_de_locais:
                verifica_localidade(distrito, localidade, local_atendimento)

    finally:
        close_chrome()