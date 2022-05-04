import telebot
import requests
import json
import time

from replit import db

chat_id = -671941311

comprador_email_lista = []
assinatura_status_lista = []
venda_status_lista = []
forma_pagamento_lista	 = []
data_assinatura_lista	 = []

assinatura_status = None
venda_status = None
comprador_email = None
forma_pagamento = None
data_assinatura = None

bool_confir = False

def monetizze():
  global comprador_email_lista,comprador_nome_lista,assinatura_status_lista
  global venda_status_lista,forma_pagamento_lista
  global data_assinatura_lista
  global bool_requests
  global chat_id

  comprador_email_lista = []
  assinatura_status_lista = []
  venda_status_lista = []

  forma_pagamento_lista	 = []
  data_assinatura_lista	 = []

  api_endpoint = "https://api.monetizze.com.br/2.1/token"

  headers = {
    "X_CONSUMER_KEY": "sWNgcjDye2nClAkok0Xd1TDKz7LnpABa",
    "Content-Type": "application/json"
  }

  response = requests.get(api_endpoint,headers = headers)

  dados = response.json()

  api_endpoint =   "https://api.monetizze.com.br/2.1/transactions"

  #https://api.monetizze.com.br/2.1/transactions
  #https://app.monetizze.com.br/relatorios/assinaturas

  CAT_API_KEY = dados['token']

  headers = {
    "TOKEN": CAT_API_KEY
    ,"Content-Type": "application/json"
  }

  response = requests.get(api_endpoint,headers = headers)

  dados = response.json()

  max_record = int(dados['recordCount'])

  x = 0
  bool_requests = True
  
  while True:

    for i in range(len(comprador_email_lista)):
      if(dados['dados'][x]['comprador']['email'] == comprador_email_lista[i]):
        bool_requests = False

    if bool_requests == True:
      forma_pagamento_lista.append(dados['dados'][x]['venda']['formaPagamento'])
      comprador_email_lista.append(dados['dados'][x]['comprador']['email'])
      venda_status_lista.append(dados['dados'][x]['venda']['status'])
        
      if(dados['dados'][x]['venda']['status'] == "Finalizada"):
          
        assinatura_status_lista.append(dados['dados'][x]['assinatura']['status'])
        data_assinatura_lista.append(dados['dados'][x]['assinatura']['data_assinatura'])
          
      else:
        assinatura_status_lista.append("None")
        data_assinatura_lista.append("None")
    
    x = x + 1
    #print("\n")
    if x == max_record:
      #print("break")
      break

def res(bot,mensagem,email,user_id,telefone):
  global bool_confir
  global comprador_email_lista,comprador_nome_lista
  global assinatura_status_lista
  global venda_status_lista
  global forma_pagamento,data_assinatura
  global assinatura_status, venda_status, comprador_email
  
  bool_confir = False
  
  monetizze()
  
  for i in range(len(comprador_email_lista)):
    if(email == comprador_email_lista[i] and assinatura_status_lista[i] == "Ativa" or assinatura_status_lista[i] == "Inadimplente" ):
      bool_confir = True
      
      assinatura_status = assinatura_status_lista[i]
      venda_status = venda_status_lista[i]
      comprador_email = comprador_email_lista[i]

      if(forma_pagamento_lista[i] == "Cartão de crédito"):
        forma_pagamento = "Crédito"
      else:
        forma_pagamento = forma_pagamento_lista[i]
      
      data_assinatura = data_assinatura_lista[i]

      db[f"Key {comprador_email}"] = f"{comprador_email} {assinatura_status} {venda_status} {forma_pagamento} {data_assinatura} {user_id} {telefone}"


  if bool_confir == True:
    texto = f"Sua assinatura está {assinatura_status}. Status de venda {venda_status}.\nVou te enviar o link de acesso. 😉"
    bot.send_message(mensagem.chat.id, texto)
    
    link = bot.export_chat_invite_link(chat_id)
    bot.send_message(mensagem.chat.id, link)
    time.sleep(5)
    link = bot.export_chat_invite_link(chat_id)
    #print(link)

  else:
    texto = "Sua assinatura ainda não está ativa. Se o pagamento foi por boleto, aguarde até o próximo dia útil."
    bot.send_message(mensagem.chat.id, texto)
    texto = "Envie o comando /grupo para tentar novamente."
    bot.send_message(mensagem.chat.id, texto)
    texto = "Certifique-se de que o e-mail cadastrado é o mesmo utilizado na compra através do comando /eu e altere no comando /alterar_dados se necessário"
    bot.send_message(mensagem.chat.id, texto)

def ver_membros(bot):
  global comprador_email_lista, comprador_nome_lista
  global venda_status_lista, assinatura_status_lista
  global forma_pagamento,data_assinatura
  global chat_id
  
  monetizze()
  email = ""

  matches = db.prefix("Key")
  
  for i in range(len(matches)):
    email = matches[i].split()[1]
    value_db = db[f"Key {email}"]
    print(email)
    for y in range(len(comprador_email_lista)):
      if(email == comprador_email_lista[y] and (assinatura_status_lista[y] == "Cancelada" or assinatura_status_lista[y] == "None")):
        Texto = "Desculpe. Você foi expulso pois não renovou a sua assinatura. 😔"
        bot.send_message(value_db.split()[6], Texto)
        bot.kick_chat_member(chat_id, value_db.split()[6]) 
        del db[f"Key {email}"]