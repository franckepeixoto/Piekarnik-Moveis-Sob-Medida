from flask import Flask, jsonify, render_template

app = Flask(__name__)

PROJECT_NAME = "KAMILLA & FRANCKE"
PROJECT_REF = "Ref.#SC001.26"

PROJETO = {
    "projeto": {
        "fases": [
            {
                "nome": "PROJETO",
                "etapas": [
                    {
                        "nome": "Levantamento",
                        "concluido": True,
                        "comentario": "Medidas do ambiente coletadas. Conferidos pontos elétricos, hidráulicos, portas e janelas. Fotos anexadas ao projeto."
                    },
                    {
                        "nome": "Projeto 3D",
                        "concluido": True,
                        "comentario": ""
                    },
                    {
                        "nome": "Apresentação",
                        "concluido": True,
                        "comentario": ""
                    },
                    {
                        "nome": "Revisões",
                        "concluido": True,
                        "comentario": "Cliente solicitou alteração na quantidade de gavetas e ajuste na altura do armário. Alterações realizadas e aprovadas."
                    }
                ]
            },
            {
                "nome": "ESPECIFICAÇÃO",
                "etapas": [
                    {
                        "nome": "Cores",
                        "concluido": False,
                        "comentario": "Cliente escolheu MDF padrão amadeirado para estrutura e padrão branco para portas."
                    },
                    {
                        "nome": "Texturas",
                        "concluido": False,
                        "comentario": ""
                    }
                ]
            },
            {
                "nome": "COMERCIAL",
                "etapas": [
                    {
                        "nome": "Orçamento",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Proposta",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Aprovação",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Contrato",
                        "concluido": False,
                        "comentario": "Contrato será enviado após aprovação da proposta e confirmação das condições de pagamento."
                    }
                ]
            },
            {
                "nome": "CONFERÊNCIA",
                "etapas": [
                    {
                        "nome": "Medição final",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Visita técnica",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Projeto executivo",
                        "concluido": False,
                        "comentario": ""
                    }
                ]
            },
            {
                "nome": "PRODUÇÃO",
                "etapas": [
                    {
                        "nome": "Corte",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Usinagem",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Bordeamento",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Montagem",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Acabamento",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Conferência",
                        "concluido": False,
                        "comentario": ""
                    }
                ]
            },
            {
                "nome": "INSTALAÇÃO",
                "etapas": [
                    {
                        "nome": "Montagem",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Vistoria",
                        "concluido": False,
                        "comentario": ""
                    }
                ]
            },
            {
                "nome": "ENTREGA",
                "etapas": [
                    {
                        "nome": "Entrega",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Pós-venda",
                        "concluido": False,
                        "comentario": ""
                    },
                    {
                        "nome": "Encerramento",
                        "concluido": False,
                        "comentario": ""
                    }
                ]
            }
        ]
    }
}


def get_step_status(steps, index):
    if all(step["concluido"] for step in steps):
        return "concluido"

    first_incomplete = next((i for i, step in enumerate(steps) if not step["concluido"]), None)

    if first_incomplete is None:
        return "concluido"
    if index < first_incomplete:
        return "concluido"
    if index == first_incomplete:
        return "em_andamento"
    return "proxima"


@app.route("/")
def index():
    fases = PROJETO["projeto"]["fases"]
    total_steps = sum(len(fase["etapas"]) for fase in fases)
    completed_steps = sum(
        1
        for fase in fases
        for etapa in fase["etapas"]
        if etapa["concluido"]
    )
    progress = round((completed_steps / total_steps) * 100) if total_steps else 0

    return render_template(
        "index.html",
        projeto=PROJETO["projeto"],
        project_name=PROJECT_NAME,
        project_ref=PROJECT_REF,
        progress=progress,
        completed_steps=completed_steps,
        total_steps=total_steps,
        get_step_status=get_step_status,
    )


@app.route("/api/projeto")
def projeto_api():
    return jsonify(PROJETO)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
