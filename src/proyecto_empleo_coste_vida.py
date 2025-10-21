import os
import numpy as np
import pandas as pd


#Rutas

ruta_raw = "data/raw"
ruta_out = "data/processed"
os.makedirs(ruta_raw, exist_ok=True)
os.makedirs(ruta_out, exist_ok=True)

f_ofertas = os.path.join(ruta_raw, "linkedin_job_postings.csv")
f_skills  = os.path.join(ruta_raw, "job_skills.csv")
f_coste   = os.path.join(ruta_raw, "Cost_of_Living_Index_by_Country_2024.csv")
f_salida  = os.path.join(ruta_out, "empleo_coste_vida_2024.csv")

print("Rutas OK")
print(f"- Ofertas: {f_ofertas}")
print(f"- Skills : {f_skills}")
print(f"- Coste  : {f_coste}")


#Lectura básica

ofertas_raw = pd.read_csv(f_ofertas, low_memory=False, on_bad_lines="skip")
skills_raw  = pd.read_csv(f_skills,  low_memory=False, on_bad_lines="skip")
coste_raw   = pd.read_csv(f_coste,   low_memory=False)

print("Dimensiones:")
print("  Ofertas:", ofertas_raw.shape)
print("  Skills :", skills_raw.shape)
print("  Coste  :", coste_raw.shape)


#Selección y renombre simple (si un nombre no existe, se ignora)

col_of_enlace = "job_link" if "job_link" in ofertas_raw.columns else None
col_of_titulo = "job_title" if "job_title" in ofertas_raw.columns else None
col_of_empresa = "company" if "company" in ofertas_raw.columns else None
col_of_ubic = "job_location" if "job_location" in ofertas_raw.columns else None
col_of_fecha = "date_posted" if "date_posted" in ofertas_raw.columns else None

usar = [c for c in [col_of_enlace,col_of_titulo,col_of_empresa,col_of_ubic,col_of_fecha] if c is not None]
ofertas = ofertas_raw[usar].copy()

ren = {}
if col_of_enlace: ren[col_of_enlace]="enlace"
if col_of_titulo: ren[col_of_titulo]="titulo_oferta"
if col_of_empresa:ren[col_of_empresa]="empresa"
if col_of_ubic: ren[col_of_ubic] ="ubicacion"
if col_of_fecha: ren[col_of_fecha] ="fecha_publicacion"
ofertas.rename(columns=ren, inplace=True)


#País

# Regla 1: si la ubicación tiene coma, el último trozo
# Regla 2: si ese trozo es un código de estado de USA (CA, NY, TX...), entonces "UNITED STATES"
# Regla 3: si contiene palabras país claras (USA, CANADA, UNITED KINGDOM, AUSTRALIA)
# Regla 4: si parece "área/metro" - UNITED STATES
# Regla 5: si contiene dígitos (tipo 2024-01) o es vacío - NaN

usa_codigos = set(["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA",
                   "MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
                   "TX","UT","VT","VA","WA","WV","WI","WY","DC","PR"])

def extraer_pais_simple(ubic):
    if pd.isna(ubic):
        return np.nan
    t = str(ubic).strip()
    if t == "" or any(ch.isdigit() for ch in t):
        return np.nan
    u = t.upper()
    if "UNITED STATES" in u or "USA" in u or "U.S." in u: return "UNITED STATES"
    if "CANADA" in u: return "CANADA"
    if "UNITED KINGDOM" in u or " ENGLAND" in u or "SCOTLAND" in u or "WALES" in u or "NORTHERN IRELAND" in u or " UK" in u:
        return "UNITED KINGDOM"
    if "AUSTRALIA" in u: return "AUSTRALIA"
    if ("AREA" in u or "METRO" in u):
        return "UNITED STATES"

    #Último fragmento tras coma
    ult = u.split(",")[-1].strip() if "," in u else u
    if ult in usa_codigos:   
        return "UNITED STATES"
    if any(ch.isdigit() for ch in ult) or ult == "":
        return np.nan
    return ult  

if "ubicacion" in ofertas.columns:
    ofertas["ubicacion"] = ofertas["ubicacion"].astype(str).str.strip()
    ofertas["pais_norm"] = ofertas["ubicacion"].apply(extraer_pais_simple)
else:
    ofertas["pais_norm"] = np.nan

#Formas en español más comunes
ofertas["pais_norm"] = ofertas["pais_norm"].replace({
    "ESPAÑA":"SPAIN",
    "ESTADOS UNIDOS":"UNITED STATES",
    "REINO UNIDO":"UNITED KINGDOM",
    "MÉXICO":"MEXICO"
})

#Nombre legible
ofertas["pais"] = ofertas["pais_norm"].apply(lambda x: str(x).title() if isinstance(x,str) and x.strip()!="" else np.nan)


#Fecha y mes

if "fecha_publicacion" in ofertas.columns:
    ofertas["fecha_publicacion"] = pd.to_datetime(ofertas["fecha_publicacion"], errors="coerce")
    ofertas["mes_publicacion"] = ofertas["fecha_publicacion"].dt.strftime("%Y-%m")
else:
    ofertas["mes_publicacion"] = np.nan


#Duplicados y remoto

if "enlace" in ofertas.columns:
    ofertas = ofertas.drop_duplicates(subset=["enlace"])

def marcar_remoto_simple(texto1, texto2):
    txt = (str(texto1) + " " + str(texto2)).lower()
    if "remote" in txt or "remoto" in txt or "hybrid" in txt or "híbrido" in txt:
        return 1
    return 0

if "ubicacion" not in ofertas.columns:
    ofertas["ubicacion"] = ""
if "titulo_oferta" not in ofertas.columns:
    ofertas["titulo_oferta"] = ""

ofertas["es_remoto"] = ofertas.apply(lambda f: marcar_remoto_simple(f["ubicacion"], f["titulo_oferta"]), axis=1)


#Skills

col_sk_enlace = "job_link"  if "job_link"  in skills_raw.columns else None
col_sk_texto  = "job_skills" if "job_skills" in skills_raw.columns else None

skills = skills_raw[[col_sk_enlace]].copy()
skills.rename(columns={col_sk_enlace:"enlace"}, inplace=True)

def a_lista(txt):
    if pd.isna(txt): return []
    return [p.strip().lower() for p in str(txt).split(",") if p.strip()!=""]

if col_sk_texto is not None:
    skills["lista_skills"] = skills_raw[col_sk_texto].apply(a_lista)
else:
    skills["lista_skills"] = [[] for _ in range(len(skills))]

skills_clave = ["python","sql","power bi","tableau","excel","azure","aws","google cloud","java","javascript"]

for sk in skills_clave:
    col = "skill_" + sk.replace(" ","_")
    skills[col] = skills["lista_skills"].apply(lambda l: 1 if sk in l else 0)

skills["num_skills"] = skills["lista_skills"].apply(len)


#Unión ofertas + skills y área simple

df = ofertas.merge(skills.drop(columns=["lista_skills"]), on="enlace", how="left")

def area_simple(f):
    if f.get("skill_python",0)==1 or f.get("skill_sql",0)==1 or f.get("skill_power_bi",0)==1 or f.get("skill_tableau",0)==1:
        return "datos_ia"
    if f.get("skill_java",0)==1 or f.get("skill_javascript",0)==1:
        return "desarrollo"
    if f.get("skill_azure",0)==1 or f.get("skill_aws",0)==1 or f.get("skill_google_cloud",0)==1:
        return "cloud_devops"
    return "otros"

df["area_simple"] = df.apply(area_simple, axis=1)


#Coste de vida (por país)

coste = coste_raw.copy()
if "Country" in coste.columns: coste.rename(columns={"Country":"pais"}, inplace=True)

#Renombres básicos
for c in list(coste.columns):
    cl = c.lower()
    if "cost of living index" in cl: coste.rename(columns={c:"indice_coste_vida"}, inplace=True)
    if "rent index" in cl: coste.rename(columns={c:"indice_alquiler"}, inplace=True)
    if "groceries" in cl: coste.rename(columns={c:"indice_super"}, inplace=True)
    if "restaurant" in cl: coste.rename(columns={c:"indice_restaurantes"}, inplace=True)
    if "local purchasing" in cl: coste.rename(columns={c:"indice_poder_adquisitivo"}, inplace=True)

coste["pais_norm"] = coste["pais"].astype(str).str.upper().str.strip()
df["pais_norm"] = df["pais_norm"].astype(str).str.upper().str.strip()

df = df.merge(
    coste[["pais_norm","indice_coste_vida","indice_alquiler","indice_super","indice_restaurantes","indice_poder_adquisitivo"]],
    on="pais_norm",
    how="left"
)

#Quitar filas sin país válido (para no ver basura tipo '2024-01')
df = df[~df["pais"].isna()].copy()


#EDA

print("\n--- EDA rápido ---")
print("Filas y columnas:", df.shape)
print("Top países:")
print(df["pais"].value_counts().head(10))
print("Remoto (0/1):")
print(df["es_remoto"].value_counts(dropna=False))


#Guardar

df.to_csv(f_salida, index=False)
print("\nCSV final guardado en:", f_salida)
print("Listo para Power BI (simple y limpio).")





















