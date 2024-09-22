from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Altere para uma chave secreta segura

# Configurações do MySQL
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="db_pet")
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        endereco = request.form['endereco']    
        
        try:
            # Inserir dados na tabela user
            cursor.execute("INSERT INTO user (nome, telefone, endereco) VALUES (%s, %s, %s)", (nome, telefone, endereco))
            user_id = cursor.lastrowid
            
            db.commit()
            
            return redirect(url_for('list_pets'))
        except MySQLdb.Error as e:
            db.rollback()
            return f"Erro: {e}"
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor.execute("SELECT password FROM login WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if result:
            session['username'] = username
            return redirect(url_for('list_pets'))
        else:
            return "Nome de usuário ou senha incorretos"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if 'username' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        nome = request.form['nome']
        especie = request.form['especie']
        idade = request.form['idade']
        data_vacinacao = request.form['data_vacinacao']
        local_vacinacao = request.form['local_vacinacao']
        user_id = request.form['user_id']  

        try:
            cursor.execute(
                "INSERT INTO animal (nome, especie, idade, user_id, data_vacinacao, local_vacinacao) VALUES (%s, %s, %s, %s, %s, %s)",
                (nome, especie, idade, user_id, data_vacinacao, local_vacinacao)
            )
            db.commit()
            return redirect(url_for('list_pets'))
        except MySQLdb.Error as e:
            db.rollback()
            return f"Erro: {e}"

    # Buscar todos os usuários do banco de dados
    cursor.execute("SELECT id, nome FROM user")
    usuarios = cursor.fetchall()

    return render_template('add_pet.html', usuarios=usuarios)

@app.route('/list_pets', methods=['GET', 'POST'])
def list_pets():
    if 'username' not in session:
        return redirect(url_for('home'))

    filtro = request.form.get('filtro', '')

    if filtro:
        cursor.execute("SELECT * FROM animal WHERE nome LIKE %s", (f'%{filtro}%',))
    else:
        cursor.execute("SELECT * FROM animal")

    pets = cursor.fetchall()
    return render_template('list_pets.html', pets=pets)

if __name__ == '__main__':
    app.run(debug=True)
