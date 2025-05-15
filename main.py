import datetime
import pandas as pd

planilha = {
    "Semana": [],
    "Pagante": []
}
pagantes = ["Enzo", "Pedrão", "André", "Samuel", "Belai", "Pedrão", "Alex", "Antônio", "Comunitária"]
inicio = datetime.datetime(2025,4,4)
semana_inicio = int(inicio.strftime("%V"))
ciclos = int(input("Digite a quantidade de ciclos que deseja verificar: ")) * len(pagantes)

for i in range(ciclos):
    data = datetime.datetime.now() + datetime.timedelta(i * 7)
    pagante = pagantes[(int(data.strftime("%V")) + 1 - semana_inicio) % len(pagantes)]
    dia = f"{data.strftime('%d')}/{data.strftime('%m')}"

    planilha["Semana"].append(dia)
    planilha["Pagante"].append(pagante)

df = pd.DataFrame(planilha)
print(df)
df.to_excel("coquinha.xlsx", sheet_name="escala", index = False)