from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email
import requests
from flask_mail import Mail, Message
import schedule
import time
import threading

app = Flask(__name__)
app.secret_key = 'chave_secreta_simples'  # Mude para algo seu, como sua senha

# Configuração de email (use Gmail para teste)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'seuemail@gmail.com'  # Coloque seu email Gmail aqui
app.config['MAIL_PASSWORD'] = 'suasenha'  # Coloque sua senha de app do Gmail (veja abaixo como criar)
mail = Mail(app)

# Como criar senha de app no Gmail: Vá em contas Google > Segurança > Senhas de app > Crie uma para "Mail" no seu dispositivo.

# Armazenamento simples (em vez de banco de dados, use um arquivo)
config_file = 'config.txt'

class ConfigForm(FlaskForm):
    frequency = SelectField('Frequência de busca', choices=[('diaria', 'Diária'), ('semanal', 'Semanal')], validators=[DataRequired()])
    databases = SelectMultipleField('Bases de dados', choices=[('pubmed', 'PubMed'), ('scielo', 'SciELO'), ('bvs', 'BVS'), ('elsevier', 'Elsevier'), ('lilacs', 'Lilacs')], validators=[DataRequired()])
    descriptors = StringField('Descritores (palavras-chave, ex: diabetes)', validators=[DataRequired()])
    email = StringField('Seu email', validators=[DataRequired(), Email()])
    periodicity = SelectField('Frequência de envio de email', choices=[('diaria', 'Diária'), ('semanal', 'Semanal')], validators=[DataRequired()])
    submit = SubmitField('Salvar e Iniciar')

def save_config(data):
    with open(config_file, 'w') as f:
        f.write(f"frequency:{data['frequency']}\n")
        f.write(f"databases:{','.join(data['databases'])}\n")
        f.write(f"descriptors:{data['descriptors']}\n")
        f.write(f"email:{data['email']}\n")
        f.write(f"periodicity:{data['periodicity']}\n")

def load_config():
    config = {}
    try:
        with open(config_file, 'r') as f:
            for line in f:
                key, value = line.strip().split(':', 1)
                config[key] = value
        config['databases'] = config['databases'].split(',')
    except:
        return None
    return config

def busca_artigos(descriptors, databases):
    resultados = []
    # Exemplo simples para PubMed (adicione mais se quiser)
    if 'pubmed' in databases:
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={descriptors}&retmax=5&sort=date"
        response = requests.get(url)
        # Aqui, pegue resultados simples (em XML, mas para básico, só texto)
        resultados.append(response.text)  # Mude para parsear melhor se quiser
    # Adicione para outras bases (similar)
    return "\n".join(resultados)

def envia_email(email, conteudo):
    msg = Message("Medical News @Chapermann: Atualizações", sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = conteudo
    mail.send(msg)

def tarefa_periodica():
    config = load_config()
    if config:
        artigos = busca_artigos(config['descriptors'], config['databases'])
        envia_email(config['email'], f"Artigos encontrados: {artigos}")

def agendador():
    schedule.every(1).day.do(tarefa_periodica)  # Mude para .week para semanal
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/', methods=['GET', 'POST'])
def config():
    form = ConfigForm()
    if form.validate_on_submit():
        data = {
            'frequency': form.frequency.data,
            'databases': form.databases.data,
            'descriptors': form.descriptors.data,
            'email': form.email.data,
            'periodicity': form.periodicity.data
        }
        save_config(data)
        return redirect(url_for('config'))
    config_atual = load_config()
    return render_template('config.html', form=form, config=config_atual)

if __name__ == '__main__':
    threading.Thread(target=agendador).start()
    app.run(debug=True)
