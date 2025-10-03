#!/usr/bin/env python3
import csv, os, requests, time, sys

# ========= Config =========
GITHUB_TOKEN  = os.getenv("GITHUB_TOKEN")
REPO_FULLNAME = os.getenv("REPO_FULLNAME")        # ej: "AdyuerHack/Inner-Light-AI"
PROJECT_TITLE = os.getenv("PROJECT_TITLE")        # ej: "Inner-Light-AI" (opcional)

# Limpieza previa: cierra issues abiertos y borra items del Project v2
CLEAR_EXISTING_ISSUES  = True
CLEAR_PROJECT_ITEMS    = True

if not GITHUB_TOKEN or not REPO_FULLNAME:
    print("ERROR: exporta GITHUB_TOKEN y REPO_FULLNAME.\n"
          "Ejemplo:\n  export GITHUB_TOKEN='xxx'\n  export REPO_FULLNAME='usuario/repo'\n")
    sys.exit(1)

OWNER = REPO_FULLNAME.split("/")[0]
REST = "https://api.github.com"
GRAPHQL = "https://api.github.com/graphql"
HEADERS_JSON = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}
HEADERS_GQL  = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# ========= Utilidades REST / GraphQL =========
def rest_get(url, params=None):
    r = requests.get(url, headers=HEADERS_JSON, params=params or {})
    if r.status_code != 200:
        raise Exception(f"GET {url} -> {r.status_code} {r.text}")
    return r.json(), r.headers

def rest_post(url, data):
    r = requests.post(url, headers=HEADERS_JSON, json=data)
    if r.status_code not in (200, 201):
        raise Exception(f"POST {url} -> {r.status_code} {r.text}")
    return r.json()

def rest_patch(url, data):
    r = requests.patch(url, headers=HEADERS_JSON, json=data)
    # ✅ Arreglo: comparar directamente
    if r.status_code != 200:
        raise Exception(f"PATCH {url} -> {r.status_code} {r.text}")
    return r.json()

def gql(query, variables):
    r = requests.post(GRAPHQL, headers=HEADERS_GQL, json={"query": query, "variables": variables})
    j = r.json()
    if r.status_code != 200 or "errors" in j:
        raise Exception(f"GraphQL {r.status_code}: {j}")
    return j

# ========= Limpieza previa =========
def close_all_open_issues():
    """Cierra todos los issues abiertos (no PRs) del repo."""
    print("🧹 Cerrando issues abiertos existentes…")
    page = 1
    total_closed = 0
    while True:
        issues, headers = rest_get(f"{REST}/repos/{REPO_FULLNAME}/issues",
                                   {"state": "open", "per_page": 100, "page": page})
        if not issues:
            break
        for it in issues:
            # saltar PRs
            if "pull_request" in it:
                continue
            num = it["number"]
            rest_patch(f"{REST}/repos/{REPO_FULLNAME}/issues/{num}", {"state": "closed"})
            total_closed += 1
            print(f"   ✖ Closed #{num}: {it['title']}")
            time.sleep(0.15)
        page += 1
    print(f"   ✅ Total issues cerrados: {total_closed}")

def delete_all_project_items(project_id):
    """Elimina todos los items del Project v2 (requiere projectId en el input)."""
    if not project_id:
        print("   (No hay Project v2 para limpiar)")
        return
    print("🧹 Eliminando items existentes del Project v2…")
    has_next = True
    cursor = None
    total_deleted = 0
    while has_next:
        q = """
        query($id:ID!, $after:String){
          node(id:$id){
            ... on ProjectV2{
              items(first:100, after:$after){
                nodes{ id content{ __typename ... on Issue { number title } } }
                pageInfo{ hasNextPage endCursor }
              }
            }
          }
        }"""
        data = gql(q, {"id": project_id, "after": cursor})
        items = data["data"]["node"]["items"]["nodes"]
        page  = data["data"]["node"]["items"]["pageInfo"]
        for it in items:
            item_id = it["id"]
            # ✅ Arreglo: mutation requiere projectId + itemId
            m = """
            mutation($projectId:ID!, $itemId:ID!){
              deleteProjectV2Item(input:{ projectId:$projectId, itemId:$itemId }){
                deletedItemId
              }
            }"""
            gql(m, {"projectId": project_id, "itemId": item_id})
            total_deleted += 1
            content = it.get("content") or {}
            if content.get("__typename") == "Issue":
                print(f"   🗑️  Item (Issue #{content.get('number')}: {content.get('title')}) eliminado")
            else:
                print("   🗑️  Item eliminado")
            time.sleep(0.1)
        has_next = page["hasNextPage"]
        cursor   = page["endCursor"]
    print(f"   ✅ Total items eliminados del Project: {total_deleted}")

# ========= Labels =========
def ensure_label(name, color="b5b5b5"):
    labels, _ = rest_get(f"{REST}/repos/{REPO_FULLNAME}/labels", {"per_page": 100})
    if not any(l["name"].lower() == name.lower() for l in labels):
        rest_post(f"{REST}/repos/{REPO_FULLNAME}/labels", {"name": name, "color": color})

# ========= Milestones =========
def get_milestone_number_by_title(title):
    res, _ = rest_get(f"{REST}/repos/{REPO_FULLNAME}/milestones", {"state": "all", "per_page": 100})
    for m in res:
        if m.get("title") == title:
            return m.get("number")
    return None

def ensure_milestone_number(title):
    num = get_milestone_number_by_title(title)
    if num is not None:
        return num
    created = rest_post(f"{REST}/repos/{REPO_FULLNAME}/milestones", {"title": title})
    return created.get("number")

# ========= Projects v2 =========
def get_project_id(owner_login, project_title):
    q = """
    query($login:String!){
      user(login:$login){
        projectsV2(first:50){ nodes{ id title } }
      }
    }"""
    res = gql(q, {"login": owner_login})
    for p in res["data"]["user"]["projectsV2"]["nodes"]:
        if p["title"] == project_title:
            return p["id"]
    return None

def get_project_fields(project_id):
    q = """
    query($id:ID!){
      node(id:$id){
        ... on ProjectV2{
          fields(first:50){
            nodes{
              __typename
              ... on ProjectV2FieldCommon { id name dataType }
              ... on ProjectV2SingleSelectField { id name options{ id name } }
            }
          }
        }
      }
    }"""
    return gql(q, {"id": project_id})["data"]["node"]["fields"]["nodes"]

def add_issue_to_project(project_id, issue_node_id):
    q = """
    mutation($p:ID!, $c:ID!){
      addProjectV2ItemById(input:{projectId:$p, contentId:$c}){
        item{ id }
      }
    }"""
    resp = gql(q, {"p": project_id, "c": issue_node_id})
    return resp["data"]["addProjectV2ItemById"]["item"]["id"]

def set_project_single_select(project_id, item_id, field_id, option_id):
    q = """
    mutation($project:ID!, $item:ID!, $field:ID!, $option:String!){
      updateProjectV2ItemFieldValue(
        input:{
          projectId:$project
          itemId:$item
          fieldId:$field
          value:{ singleSelectOptionId:$option }
        }
      ){ clientMutationId }
    }"""
    gql(q, {"project": project_id, "item": item_id, "field": field_id, "option": option_id})

# ========= Crear Issue =========
def create_issue(title, body, labels_csv, milestone_title, status_value, project_id):
    # Labels
    labels = []
    if labels_csv:
        labels = [x.strip() for x in labels_csv.split(";") if x.strip()]
        for lb in labels: ensure_label(lb)

    data = {"title": title or "(sin título)", "body": body or ""}
    if labels:
        data["labels"] = labels

    # Milestone: convertir título -> número
    if milestone_title:
        ms_num = ensure_milestone_number(milestone_title)
        if ms_num:
            data["milestone"] = ms_num

    # Crear Issue
    issue = rest_post(f"{REST}/repos/{REPO_FULLNAME}/issues", data)
    issue_node_id = issue["node_id"]
    number = issue["number"]
    print(f"✅ Creado Issue #{number}: {title}")

    # Añadir al Project v2
    if not project_id:
        return
    try:
        item_id = add_issue_to_project(project_id, issue_node_id)
        print("   ↪ Añadido al Project v2.")
    except Exception as e:
        print("   ⚠ No se pudo añadir al Project v2:", e)
        return

    # Status
    if status_value:
        try:
            fields = get_project_fields(project_id)
            status_field = None
            for f in fields:
                if f.get("__typename") == "ProjectV2SingleSelectField" and f.get("name","").lower() == "status":
                    status_field = f
                    break
            if not status_field:
                print("   ⚠ Campo 'Status' no encontrado en el Project.")
                return

            options = status_field.get("options") or []
            opt = next((o for o in options if o["name"].lower() == status_value.lower()), None)
            if not opt:
                aliases = {
                    "todo":"Backlog","to do":"Backlog","backlog":"Backlog",
                    "ready":"Ready",
                    "doing":"In progress","in progress":"In progress",
                    "done":"Done","hecho":"Done"
                }
                mapped = aliases.get(status_value.lower())
                if mapped:
                    opt = next((o for o in options if o["name"].lower() == mapped.lower()), None)

            if opt:
                set_project_single_select(project_id, item_id, status_field["id"], opt["id"])
                print(f"   ✅ Status = {opt['name']}")
            else:
                print(f"   ⚠ Opción de Status '{status_value}' no existe en el Project.")
        except Exception as e:
            print("   ⚠ No se pudo setear el Status:", e)

# ========= Main =========
def main():
    if len(sys.argv) < 2:
        print("Uso: python3 import_issues.py <archivo.csv>")
        sys.exit(1)
    csv_path = sys.argv[1]

    # 1) Resolver Project v2 (si se configuró)
    project_id = None
    if PROJECT_TITLE:
        try:
            project_id = get_project_id(OWNER, PROJECT_TITLE)
            if not project_id:
                print(f"⚠ Project v2 '{PROJECT_TITLE}' no encontrado. Se crearán issues sin añadir al Project.")
        except Exception as e:
            print("⚠ No pude resolver Project v2. Continúo sin Project:", e)

    # 2) Limpieza previa
    if CLEAR_EXISTING_ISSUES:
        try:
            close_all_open_issues()
        except Exception as e:
            print("⚠ No se pudo cerrar issues existentes:", e)

    if CLEAR_PROJECT_ITEMS and project_id:
        try:
            delete_all_project_items(project_id)
        except Exception as e:
            print("⚠ No se pudieron eliminar items del Project:", e)

    # 3) Importar CSV
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title      = row.get("title") or ""
            body       = row.get("body") or ""
            labels     = row.get("labels") or ""
            milestone  = row.get("milestone") or ""
            status     = row.get("status") or ""
            create_issue(title, body, labels, milestone, status, project_id)
            time.sleep(0.5)  # rate limit friendly

if __name__ == "__main__":
    main()
