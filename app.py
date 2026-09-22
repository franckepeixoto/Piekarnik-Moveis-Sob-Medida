from flask import Flask, jsonify, render_template, request
import urllib
import urllib.parse
from projeto import load_project_data,calculate_project_progress,get_step_status
app = Flask(__name__)

#PROJECT_DATA, PROJECT_NAME, PROJECT_REF = load_project_data()
#for fase in PROJECT_DATA.get("projeto", {}).get("fases", []):
#    for etapa in fase.get("etapas", []):
#        print(f"Fase: {fase['nome']}, Etapa: {etapa['nome']}, Status: {etapa['status']}, Concluido: {etapa['concluido']}, Comentario: {etapa['comentario']}")
#print()
#exit()

@app.route("/", methods=['GET', 'POST'])
def index():
    PROJECT_SHEET_ID = request.args.get('id', default="", type=str) 
    PROJECT_SHEET_ID="1L7eOVVQq0pWrdbflqnewR8648o8WVUxoGIkUl49nA5o"
    PROJECT_DATA, PROJECT_NAME, PROJECT_REF = load_project_data(PROJECT_SHEET_ID    )
    summary = calculate_project_progress(PROJECT_DATA)
    PROJECT_DATA['summary'] = summary
    fases = PROJECT_DATA["projeto"]["fases"]
    whatsapp_msg = f"Olá! Estou com algumas dúvidas, pode me ajudar? Segue o código de referência do projeto: {PROJECT_REF}  - {PROJECT_NAME} - {summary['progress']}% concluído. Obrigado! "
    return render_template(
        "index.html",
        projeto=PROJECT_DATA["projeto"],
        project_name=PROJECT_NAME,
        project_ref=PROJECT_REF,
        progress=summary["progress"],
        completed_steps=summary["completed_steps"],
        total_steps=summary["total_steps"],
        is_complete=summary["is_complete"],
        get_step_status=get_step_status,
        whatsapp_msg=urllib.parse.quote_plus(whatsapp_msg)
    )


@app.route("/api/projeto")
def projeto_api():
    PROJECT_DATA, PROJECT_NAME, PROJECT_REF = load_project_data()
    summary = calculate_project_progress(PROJECT_DATA)
    PROJECT_DATA['summary'] = summary
    return jsonify(PROJECT_DATA)



if __name__ == "__main__":
    app.run()
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=False)
