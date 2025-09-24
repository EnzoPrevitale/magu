import datetime
import random
import pandas as pd
import os
from django.conf import settings
import re

export_dir = os.path.join(settings.BASE_DIR, "exports")
os.makedirs(export_dir, exist_ok=True)

INICIO = datetime.datetime(2025, 8, 15)
SEMANA_INICIO = int(INICIO.strftime("%V"))

def verificar_ciclos(quantidade: int, pagantes: list):
    planilha = {
        "Ciclo": [],
        "Semana": [],
        "Pagante": []
    }
    for i in range(quantidade*len(pagantes)):
        data = datetime.datetime.now() + datetime.timedelta(i * 7)
        data += datetime.timedelta(5 - int(data.strftime('%w')))

        pagante = pagantes[(int(data.strftime("%V")) - SEMANA_INICIO) % len(pagantes)]
        dia = f"{data.strftime('%d')}/{data.strftime('%m')}"
        ciclos = (data - INICIO).days // (7 * len(pagantes)) + 1

        planilha["Ciclo"].append(ciclos)
        planilha["Semana"].append(dia)
        planilha["Pagante"].append(pagante)

    df = pd.DataFrame(planilha)

    arquivo = os.path.join(export_dir, "coquinha.xlsx")
    df.to_excel(arquivo, sheet_name="escala", index=False)

    return df.to_dict()

def obter_dados_conclave(pagantes: list):
    proximas_datas = verificar_ciclos(1, pagantes)
    data_conclave = proximas_datas[proximas_datas["Pagante"] == "Conclave"]["Semana"].values[0]
    if data_conclave.split("/")[1] == '01' and datetime.datetime.now().strftime("%m") == '12':
        ano = int(datetime.datetime.now().strftime("%Y")) + 1
    else:
        ano = int(datetime.datetime.now().strftime("%Y"))
    dia_conclave = datetime.datetime(ano, int(data_conclave.split("/")[1]), int(data_conclave.split("/")[0]))

    dias_para_conclave = (dia_conclave - datetime.datetime.now()).days + 1
    return {
        "dia_conclave": dia_conclave,
        "dias_para_conclave": dias_para_conclave
    }

def obter_por_nome(pagantes: list, nome: str):
    datas = pd.read_excel(f"{export_dir}/coquinha.xlsx")
    mask = datas["Pagante"].fillna("").astype(str).apply(
    lambda x: re.sub(r"\s+", "", x, flags=re.UNICODE).casefold() == "enzo"
    )

    datas_nome = datas[mask]

    print(datas_nome)

    arquivo = os.path.join(export_dir, f"coquinha{nome}.xlsx")
    datas_nome.to_excel(arquivo, sheet_name="escala", index=False)

    proxima_semana = (datas_nome[datas_nome['Ciclo'] == min(list(datas_nome['Ciclo']))])["Semana"].values[0]
    proximo_ciclo = (datas_nome[datas_nome['Ciclo'] == min(list(datas_nome['Ciclo']))])["Ciclo"].values[0]

    return {
        "proximaSemana": proxima_semana,
        "proximoCiclo": proximo_ciclo,
        "dados": datas_nome.to_dict()
    }
