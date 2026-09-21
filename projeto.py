import requests
import csv
import io 
PROJECT_SHEET_ID=""#"1L7eOVVQq0pWrdbflqnewR8648o8WVUxoGIkUl49nA5o"
PROJECT_DATA_URL = f"https://docs.google.com/spreadsheets/d/{PROJECT_SHEET_ID}/export?format=csv&gid=0"
PROJECT_IDENTITY_URL = f"https://docs.google.com/spreadsheets/d/{PROJECT_SHEET_ID}/export?format=csv&gid=2047631131"
 
def parse_status(status_value):
    value = (status_value or "").strip().lower()

    if not value:
        return "proxima"

    if any(token in value for token in ["conclu", "finaliz", "feito", "ok", "completo", "encerrado"]):
        return "concluido"

    if any(token in value for token in ["andamento", "em andamento", "iniciado", "processo"]):
        return "em_andamento"

    if any(token in value for token in ["proxima", "próxima", "pendente", "aguardando", "next"]):
        return "proxima"

    return "proxima"


def build_project_from_rows(rows):
    project = {"projeto": {"fases": []}}
    current_phase = None

    for row in rows:
        if not row or all((cell or "").strip() == "" for cell in row):
            continue

        first_cell = (row[0] if len(row) > 0 else "").strip()
        if not first_cell:
            continue

        if first_cell.startswith("#"):
            current_phase = {"nome": first_cell.lstrip("#").strip().upper(), "etapas": []}
            project["projeto"]["fases"].append(current_phase)
            continue

        if current_phase is None:
            continue

        status_value = (row[1] if len(row) > 1 else "").strip()
        comment_value = (row[2] if len(row) > 2 else "").strip()
        status_key = parse_status(status_value)

        current_phase["etapas"].append(
            {
                "nome": first_cell,
                "concluido": status_key == "concluido",
                "status": status_key,
                "comentario": comment_value,
            }
        )

    return project


def fetch_csv_rows(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    text = response.text
    reader = csv.reader(io.StringIO(text))
    return [[(cell or "").strip() for cell in row] for row in reader if any((cell or "").strip() for cell in row)]



def read_project_identity(rows):
    name = ""
    ref = ""

    for row in rows:
        if not row:
            continue
        values = [cell.strip() for cell in row if (cell or "").strip()]
        if not values:
            continue

        if not name and values[0]:
            name = values[0]

        if len(values) > 1 and not ref and values[1]:
            ref = values[1]

        if name and ref:
            break

    return (name or "N/D").strip(), (ref or "-").strip()


def load_project_data(PROJECT_SHEET_ID):
    
    PROJECT_DATA_URL = f"https://docs.google.com/spreadsheets/d/{PROJECT_SHEET_ID}/export?format=csv&gid=0"
    PROJECT_IDENTITY_URL = f"https://docs.google.com/spreadsheets/d/{PROJECT_SHEET_ID}/export?format=csv&gid=2047631131"
    try:
        rows = fetch_csv_rows(PROJECT_DATA_URL)
        #print(rows)
        project = build_project_from_rows(rows)
        if not project["projeto"]["fases"]:
            raise ValueError("No project phases found in sheet")
    except Exception:
        project = {"projeto": {"fases": []}}

    try:
        identity_rows = fetch_csv_rows(PROJECT_IDENTITY_URL)
        project_name, project_ref = identity_rows[1][1], identity_rows[1][0]
    except Exception:
        project_name = "N/D"
        project_ref = "-"

    return project, project_name, project_ref


def calculate_project_progress(project_data):
    fases = project_data.get("projeto", {}).get("fases", [])
    total_steps = sum(len(fase.get("etapas", [])) for fase in fases)
    completed_steps = sum(
        1
        for fase in fases
        for etapa in fase.get("etapas", [])
        if etapa.get("concluido")
    )
    progress = round((completed_steps / total_steps) * 100) if total_steps else 0
    is_complete = total_steps > 0 and completed_steps == total_steps

    return {
        "total_steps": total_steps,
        "completed_steps": completed_steps,
        "progress": progress,
        "is_complete": is_complete,
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



#PROJECT_DATA, PROJECT_NAME, PROJECT_REF = load_project_data()
#for fase in PROJECT_DATA.get("projeto", {}).get("fases", []):
#    for etapa in fase.get("etapas", []):
#        print(f"Fase: {fase['nome']}, Etapa: {etapa['nome']}, Status: {etapa['status']}, Concluido: {etapa['concluido']}, Comentario: {etapa['comentario']}")
#print()
#exit()