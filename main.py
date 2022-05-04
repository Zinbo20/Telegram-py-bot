import telebot
import re 
import schedule

from functions import api_requests

from replit import db

CHAVE_API = "5109773340:AAF3UeHyztqv0DBBujmDfyfuZ5P2J2oFMhI"
#5348564437:AAEYyzFxUyxLhd1KiBgEFV70xb1pgp0HdE0

bot = telebot.TeleBot(CHAVE_API)

schedule.every().day.at("12:00").do(api_requests.ver_membros,bot)

word_list = ["correto", "sim", "isso", "certo"]

name = None
bool_name = False

telefone = None
bool_telefone = False

email = None
bool_email = False

bool_assinatura = False

bool_word = False

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

texto_Inicial = """Olá, eu sou o Bot Método Cripto Gringo e vou verificar se seu pagamento ja foi aprovado!

Vou precisar que você me ajude com algumas informações...

Você pagou com boleto ou cartão? 😊"""

bool_start = False

def on_private(mensagem):
  if mensagem.chat.type == "private":
    return True

@bot.message_handler(commands=["start"],func=on_private)
def start(mensagem):  
  global name, telefone, email, bool_start, bool_assinatura
  name = None
  telefone = None
  email = None
  bool_assinatura = False
  bot.reply_to(mensagem, texto_Inicial)
  bool_start = True

@bot.message_handler(commands=["suporte"],func=on_private)
def grupo(mensagem):
  texto = "Informações de Contato:\n\nt.me/suportemetodocriptogringo\n\n@suportemetodocriptogringo\n\n/help."
  bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["help"],func=on_private)
def grupo(mensagem):
  texto = "Olá está tendo dificuldades ? Veja alguns comandos que podem te ajudar...\n\n/start\n/grupo\n/alterar_dados\n/eu\n/suporte\n\n "
  bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["get_id"],func=on_private)
def grupo(mensagem):
  id = mensagem.chat.id
  print(id)
  print("\n")

@bot.message_handler(commands=["grupo"],func=on_private)
def grupo(mensagem):
  global name,email,telefone
  if(email == None):
    matches = db.prefix("Key")
    for i in range(len(matches)):
      dados = matches[i].split()[1]
      value_db = db[f"Key {dados}"]
      if(value_db.split()[6] == str(mensagem.from_user.id)):
        email = value_db.split()[0]
        name = f"{mensagem.from_user.first_name} {mensagem.from_user.last_name}"
        telefone = value_db.split()[7]
  user_id = mensagem.from_user.id
  api_requests.res(bot,mensagem,email,user_id,telefone)
  

@bot.message_handler(commands=["Nome"],func=on_private)
def alterar_dados(mensagem):
  global bool_name,name, bool_assinatura
  name = None
  bool_name = True
  bool_assinatura = False
  texto = "Poderia me enviar seu nome completo?"
  bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["Telefone"],func=on_private)
def alterar_dados(mensagem):
  global bool_telefone, telefone, bool_assinatura
  telefone = None
  bool_telefone = True
  bool_assinatura = False
  texto = "Qual é o seu telefone?"
  bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["Email"],func=on_private)
def alterar_dados(mensagem):
  global bool_email, email, bool_assinatura
  email = None
  bool_email = True
  bool_assinatura = False
  texto = "Qual é o seu email utilizado na compra?"
  bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["alterar_dados"],func=on_private)
def alterar_dados(mensagem):
  texto = "Qual informação deseja alterar? Selecione os botões abaixo"
  bot.send_message(mensagem.chat.id, texto)
  bot.send_message(mensagem.chat.id, "/Nome")
  bot.send_message(mensagem.chat.id, "/Telefone")
  bot.send_message(mensagem.chat.id, "/Email")

@bot.message_handler(commands=["eu"],func=on_private)
def eu(mensagem):
  global name,email,telefone
  if(email == None):
    matches = db.prefix("Key")
    for i in range(len(matches)):
      dados = matches[i].split()[1]
      value_db = db[f"Key {dados}"]
      if(value_db.split()[6] == str(mensagem.from_user.id)):
        email = value_db.split()[0]
        name = f"{mensagem.from_user.first_name} {mensagem.from_user.last_name}"
        telefone = value_db.split()[7]
        
  texto = f"""Seus dados de cadastro são

👤 Nome: {name}

📞 Telefone: {telefone}

✉️ Email: {email}

Se algo estiver incorreto ou quiser alterar seus dados, me envie
 o comando /alterar_dados."""
  bot.send_message(mensagem.chat.id, texto)

#---------------------------------------------------#
  
def on_message(mensagem):
  global bool_name, name, bool_telefone, telefone, bool_email, email, bool_start, bool_assinatura,bool_word

  schedule.run_pending()
  
  if mensagem.chat.type == "private":
    bool_word = False
    for i in range(len(word_list)):
      if word_list[i] == mensagem.text.lower():
        bool_word = True
          
    matches = db.prefix("Key")
  
    if(bool_assinatura == True and bool_name == False and bool_telefone == False and bool_email == False and bool_start == True):
      texto = f"Olá, {mensagem.from_user.first_name}!\n\nParece que você não tem uma assinatura ativa 😔\n\nSe algo estiver errado, verifique seus dados com o comando /eu ou entre em contato com o /suporte."
      bot.send_message(mensagem.chat.id, texto)
    elif(bool_name == False and bool_telefone == False and bool_email == False and bool_start == True):
      for i in range(len(matches)):
        dados = matches[i].split()[1]
        value_db = db[f"Key {dados}"]
        if(value_db.split()[6] == str(mensagem.from_user.id)):
          texto = "Sua assinatura está Ativa. Use o comando /grupo para obter um novo link de acesso. Ou /eu para ver suas informações. Se algo estiver errado utilize o comando /suporte."
          bot.send_message(mensagem.chat.id, texto)
  
    if bool_email == True and email == None:
      email = mensagem.text
      if(re.search(regex,email)):
        conf_email = f"Seu email é {email}, correto?"
        bot.reply_to(mensagem,conf_email)
      else:
        email = None
        texto = "Este e-mail não me parece válido... Vamos tentar novamente"
        bot.send_message(mensagem.chat.id, texto)
      
    elif email != None and bool_email == True and bool_word == True:
      bool_email = False
      texto = "Obrigado pelas informações!"
      bot.send_message(mensagem.chat.id, texto)
    
      texto = "Me dá um momento enquanto verifico as informações com o empresa que processa os pagamentos.."
      bot.send_message(mensagem.chat.id, texto)
        
      user_id = mensagem.from_user.id
      api_requests.res(bot,mensagem,email,user_id,telefone)
      if(api_requests.assinatura_status != "Ativa" or api_requests.assinatura_status != "Inadimplente"):
        bool_assinatura = True
        
  
    elif bool_email == True and email != None:
      email = None
      texto = "Qual é o seu email utilizado na compra?"
      bot.send_message(mensagem.chat.id, texto)
    
    if bool_telefone == True and telefone == None:
      try:
        telefone = int(mensagem.text)
        conf_numero = f"Conferindo... Seu telefone é {telefone}, correto?"
        bot.reply_to(mensagem,conf_numero)
      except Exception:
        texto = "Qual é o seu telefone?"
        bot.send_message(mensagem.chat.id, texto)
      
    elif telefone != None and bool_telefone == True and bool_word == True:
      bool_telefone = False
      if(email == None):
        bool_email = True
        texto = "Perfeito, agora só vou precisar que me mande seu email, o mesmo que usou para efetuar o pagamento, assim vou achar no sistema 🤓𝗧𝗲𝗻𝗵𝗮 𝗰𝗲𝗿𝘁𝗲𝘇𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁á 𝗺𝗮𝗻𝗱𝗮𝗻𝗱𝗼 𝗼 𝗲𝗺𝗮𝗶𝗹 𝗰𝗼𝗿𝗿𝗲𝘁𝗼 𝗮𝗻𝘁𝗲𝘀 𝗱𝗲 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗮𝗿!"
        bot.reply_to(mensagem,texto)
      else:
        texto = "Perfeito, seu telefone foi alterado."
        bot.reply_to(mensagem,texto)
          
        user_id = mensagem.from_user.id
        api_requests.res(bot,mensagem,email,user_id,telefone)
        if(api_requests.assinatura_status != "Ativa" or api_requests.assinatura_status != "Inadimplente"):
          bool_assinatura = True
  
    elif bool_telefone == True and telefone != None:
      telefone = None
      texto = "Poderia me enviar o seu telefone com DDD?"
      bot.send_message(mensagem.chat.id, texto)
  
    if bool_name == True and name == None:
      name = mensagem.text
      conf_name = f"Só pra conferir, seu nome é {name}, correto?"
      bot.reply_to(mensagem,conf_name)
      
    elif name != None and bool_name == True and bool_word == True:
      bool_name = False
      if(telefone == None):
        bot.reply_to(mensagem,"Perfeito!")
        texto = "Poderia me enviar o seu telefone com DDD?"
        bot.send_message(mensagem.chat.id, texto)
        bool_telefone = True
      else:
        texto = "Perfeito!"
        bot.reply_to(mensagem,texto)
          
        user_id = mensagem.from_user.id
        api_requests.monetizze()
        if(api_requests.assinatura_status != "Ativa" or api_requests.assinatura_status != "Inadimplente"):
          bool_assinatura = True
  
    elif bool_name == True and name != None:
      name = None
      bool_name = False
    
    if name == None and bool_start == True:
      texto = "Vou precisar de algumas informações suas para verificar o seu pagamento, ok? Será bem rapidinho!"
      bot.send_message(mensagem.chat.id, texto)
      texto = "Poderia me enviar seu nome completo?"
      bot.send_message(mensagem.chat.id, texto)
      bool_name = True
  
    if bool_start == False:
      return True

@bot.message_handler(func=on_message)
def responder(mensagem):
  global name, telefone, email, bool_start
  bool_start = True

  if(email == None):
    matches = db.prefix("Key")
    for i in range(len(matches)):
      dados = matches[i].split()[1]
      value_db = db[f"Key {dados}"]
      if(value_db.split()[6] == str(mensagem.from_user.id)):
        email = value_db.split()[0]
        name = f"{mensagem.from_user.first_name} {mensagem.from_user.last_name}"
        telefone = value_db.split()[7]
        texto = "Sua assinatura está Ativa. Use o comando /grupo para obter um novo link de acesso. Ou /eu para ver suas informações."
        bot.send_message(mensagem.chat.id, texto)
        bool_start = False
        
  elif(bool_start == True and email == None):
    bot.reply_to(mensagem, texto_Inicial)
  
bot.polling()