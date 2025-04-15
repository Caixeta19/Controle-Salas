import csv
from django.http import HttpResponse

def exportar_csv(info, relatorio):
    colunas = info.model._meta.fields
    nomes_colunas = [colunas.name for colunas in colunas]

    resposta = HttpResponse(content_type="text/csv")

    if relatorio == "salas":
        resposta["Content-Disposition"] = "attachment; filename=salas.csv"

    elif relatorio == "usuarios":
        resposta["Content-Disposition"] = "attachment; filename=usuarios.csv"

    elif relatorio == "agendamentos":
        resposta["Content-Disposition"] = "attachment; filename=agendamentos.csv"

    cr_csv = csv.writer(resposta, delimiter=";")

    cr_csv.writerow(nomes_colunas)

    for linha in info.values_list():
        cr_csv.writerow(linha)

    return resposta