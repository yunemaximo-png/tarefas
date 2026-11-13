from flask import Flask, redirect, render_template, request, url_for

from tarefas.models.database import init_db
from tarefas.models.tarefa import Tarefa

app = Flask(__name__)

with app.app_context():
    init_db()

@app.route('/test')
def test():
    return 'Servidor Online!'

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':  
        titulo_form = request.form['tituloTarefa'] # casa com o nome do imput no form
        data_conclusao_form = request.form['dataConclusao'] # casa com o nome do imput no form

        data_corrigida = data_conclusao_form or None

        #Instanciamos uma nova tarefa com os dados recebidos do form
        tarefa = Tarefa(titulo = titulo_form, data_conclusao=data_corrigida)

        # Salvamos a tarefa no banco
        tarefa.salvarTarefa()

        return redirect(url_for('home'))

    tarefas = Tarefa.listarTarefas()

    return render_template('base.html', 
                           titulo_da_pagina='Lista de Tarefas', 
                           tarefas_da_pagina=tarefas
                           )

# Crie uma nova funcionalidade para apagar cada uma das tarefas cadastradas
@app.route('/delete/<int:id>')
def apagar_id_especifico(id):
    Tarefa.apagarTarefa(id)
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    if request.method == 'POST':
        titulo = request.form['tituloTarefa']
        data = request.form['dataConclusao'] or None
        Tarefa.atualizarTarefa(id, titulo, data)
        return redirect('/')
    else:
        tarefas = Tarefa.listarTarefas()
        tarefa_em_edicao = None
        
        for t in tarefas:
            if t['id_tarefa'] == id:  
                tarefa_em_edicao = t
                break
                
        return render_template('base.html',
                               titulo_da_pagina='Editar Tarefa',
                               tarefas_da_pagina=tarefas,
                               tarefa_em_edicao=tarefa_em_edicao)

if __name__ == '__main__':
    app.run()