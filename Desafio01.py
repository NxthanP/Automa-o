# Importa as bibliotecas necessárias para o nosso projeto
import pandas as pd
from selenium import webdriver
import time

# Lê o arquivo Excel 'correios.xlsx' e carrega os dados em uma DataFrame
df = pd.read_excel("correios.xlsx")

#Inicia listas de ruas e bairros vazias para armazenar ambos assim que o código rodar
ruas = []
bairros = []

#Inicializa o navegador web. Obs: No nosso caso é o Chrome.. porém e possivel alterar
navegador = webdriver.Chrome()
#Abre a página de busca de CEP nos Correios
navegador.get('https://buscacepinter.correios.com.br/app/endereco/index.php')

#Adiciona o que falta sobre os CEPS do DataFrame
for cep in df['CEP']:
    #Encontra o campo de entrada para o CEP na página web e insere o CEP da nossa procura
    cep_input = navegador.find_element('xpath', '//*[@id="endereco"]') #Comando para clicar automaticamente no campo de CEP
    cep_input.clear()  #Limpa o campo de entrada caso algo esteja escrito
    cep_input.send_keys(str(cep)) #Insere o CEP atual da nossa planilha
    time.sleep(5)  #Aguarda 5 segundos para caso o sistema esteja lento ser possivel carregar corretamente

    # Localiza e clica no botão de pesquisa
    botao_pesquisar = navegador.find_element('xpath', '//*[@id="btn_pesquisar"]')
    botao_pesquisar.click() 
    time.sleep(5) #Aguarda 5 segundos para caso o sistema esteja lento ser possivel carregar corretamente

    try:
        # Feito para tentar localizar o elemento que contém o nome da rua e do bairro e extrai seus textos para a nossa planilha
        elemento_rua = navegador.find_element('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[1]')
        nome_rua = elemento_rua.text

        elemento_bairro = navegador.find_element('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[2]')
        nome_bairro = elemento_bairro.text

        # Adiciona os nomes de rua e bairro na ordem em listas
        ruas.append(nome_rua)
        bairros.append(nome_bairro)
    except:
        # Caso não encontre as informações, adiciona uma mensagem padrão às listas. Obs: Pode ser alterado da forma que for melhor
        ruas.append("Informações não encontradas")
        bairros.append("Informações não encontradas")

    # Clica no botão de nova pesquisa para limpar os campos e estar pronto para a próxima consulta
    botao_nova_pesquisa = navegador.find_element('xpath', '//*[@id="btn_nbusca"]')
    botao_nova_pesquisa.click()

# Adiciona as listas de ruas e bairros como colunas adicionais no DataFrame
df['Rua'] = ruas
df['Bairro'] = bairros

# Salva o DataFrame atualizado de as informações no arquivo do excel
df.to_excel("correios.xlsx", index=False)
