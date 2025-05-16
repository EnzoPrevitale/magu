import datetime
import pandas as pd


def verificar_ciclos(quantidade):
    planilha = {
        "Ciclo": [],
        "Semana": [],
        "Pagante": []
    }

    for i in range(quantidade):
        data = datetime.datetime.now() + datetime.timedelta(i * 7)
        data += datetime.timedelta(5 - int(data.strftime('%w')))

        pagante = PAGANTES[(int(data.strftime("%V")) - SEMANA_INICIO) % len(PAGANTES)]
        dia = f"{data.strftime('%d')}/{data.strftime('%m')}"
        ciclo = (data - INICIO).days // (7 * len(PAGANTES)) + 1

        planilha["Ciclo"].append(ciclo)
        planilha["Semana"].append(dia)
        planilha["Pagante"].append(pagante)

    df = pd.DataFrame(planilha)
    df.to_excel("coquinha.xlsx", sheet_name="escala", index=False)

    return df


INICIO = datetime.datetime(2025, 4, 4)
SEMANA_INICIO = int(INICIO.strftime("%V"))

PAGANTES = ("Papa Doutor XIX", "Papa Botton III", "Papa Joelho VII", "Papa Magu XXI", "Papa Casada XI", "Papa Fernandão XVI", "Papa Todas XV", "Conclave")

print("[1] - Verificar próximas datas | [2] - Verificar por nome")

while True:
    while True:
        opcao = int(input("Escolha: "))
        if 2 >= opcao >= 1:
            break

    if opcao == 1:
        print(verificar_ciclos(int(input("Digite a quantidade de ciclos que deseja verificar: ")) * len(PAGANTES)))
    elif opcao == 2:
        for num in range(len(PAGANTES)):
            print(f"[{num + 1}] - {PAGANTES[num]}")

        nome = PAGANTES[int(input("Escolha: ")) - 1]
        datas = verificar_ciclos(3 * len(PAGANTES))
        datas_nome = datas[datas["Pagante"] == nome]

        print(datas_nome)
        datas_nome.to_excel(f"coquinha_{nome}.xlsx", sheet_name="escala", index=False)

        proxima_semana = (datas_nome[datas_nome['Ciclo'] == min(list(datas_nome['Ciclo']))])["Semana"].values[0]
        proximo_ciclo = (datas_nome[datas_nome['Ciclo'] == min(list(datas_nome['Ciclo']))])["Ciclo"].values[0]
        valor_total_estimado = f"{((proximo_ciclo - 1) * 14):.2f}".replace('.', ',')

        print(f"\n"
              f"Informações de {nome}: \n"
              f"Próxima semana: {proxima_semana}\n"
              f"Cocas pagas: {proximo_ciclo - 1}\n"
              f"Valor total estimado: R${valor_total_estimado}"
              )
        break

