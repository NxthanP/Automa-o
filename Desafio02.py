# Importa a biblioteca requests para fazer requisições HTTP
import requests
# Importa as bibliotecas datetime e timedelta para trabalhar com datas
from datetime import datetime, timedelta

data_fim = datetime.now().strftime("%d/%m/%Y")
data_ini = (datetime.now() - timedelta(days=16)).strftime("%d/%m/%Y")

response = requests.get(f"https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=gerarCSVFechamentoMoedaNoPeriodo&ChkMoeda=61&DATAINI={data_ini}&DATAFIM={data_fim}")

# Pega o conteúdo da resposta da requisição e substitui as vírgulas por pontos
data = response.text.replace(",", "." )
# Imprime o conteúdo do arquivo
print(data)
