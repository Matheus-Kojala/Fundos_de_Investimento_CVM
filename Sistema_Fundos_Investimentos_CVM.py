import pandas as pd
import matplotlib.pyplot as plt

# Criando um menu de seleção do mês de análise:
def menu_ano():
    ano = """Seja bem-vindo ao seu app de análise de fundos!

    \tPara saber informações a respeito do melhor fundo para se investir os seus recursos,
    \tpreencha o campo abaixo com o ano a ser analisado, a partir de 2021.
    \t Ano:"""
    return input(ano)
    
def menu_mes():
    mes = """\tPreencha o campo abaixo com o mês a ser analisado.
    \t Mês:"""
    return input(mes)

def menu_acao():
    menu_acao = """ O que você deseja fazer:
                    1) Analisar o fundo com maior PL
                    2) Analisar o fundo com menor PL
                    Digite apenas o número da opção escolhida:"""
    return input(menu_acao)

# Função para retornar ao menu inicial
def retornar_menu():
    input("\nPressione Enter para retornar ao menu inicial...")
    main()

# Escolhendo o mês de análise:
def main():
    while True:
        ano = str(menu_ano())
        mes = str(menu_mes())
        link = f"https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes}.zip"
        print(link)
        acao(link)
        return retornar_menu()
        

# Função para realizar a análise do fundo
def acao(link_escolhido):
    acao_escolhida = menu_acao()


    if acao_escolhida == "1":
        informes_diarios = pd.read_csv(link_escolhido, sep=";")
        informes_diarios['DT_DIA'] = informes_diarios['DT_COMPTC'].str[-2:].astype(int)
        ultimo_dia = informes_diarios['DT_DIA'].max()
        comparativo = informes_diarios[informes_diarios['DT_DIA'] == ultimo_dia]
        comparativo = comparativo.sort_values(by='VL_PATRIM_LIQ', ascending=True)
        Fundo_com_maior_pl = comparativo.tail(1)
        Fundo_com_maior_pl.loc[:, 'VL_PATRIM_LIQ'] = Fundo_com_maior_pl['VL_PATRIM_LIQ'].apply(lambda x: '{:,.2f}'.format(x))
        CNPJ_Fundo_com_maior_pl = Fundo_com_maior_pl['CNPJ_FUNDO'].iloc[0]
        informes_diarios_filtered_condiction = informes_diarios['CNPJ_FUNDO'] == CNPJ_Fundo_com_maior_pl
        informes_diarios_filtered = informes_diarios[informes_diarios_filtered_condiction]
        informes_diarios_filtered['VL_QUOTA'] = informes_diarios['VL_QUOTA']
        print(f"""\tO fundo que obteve o maior PL no mês selecionado foi o fundo inscrito sobre o CNPJ de número: {Fundo_com_maior_pl['CNPJ_FUNDO'].values[0]},
        acumulando um valor total de: R${Fundo_com_maior_pl['VL_PATRIM_LIQ'].values[0]}!\t""")
        informes_diarios_filtered.plot(x='DT_DIA', y='VL_QUOTA', color='blue', linestyle='-', marker='o', markersize=3)
        plt.title('Evolução do Valor da Quota - Fundo com Maior PL')
        plt.xlabel('Dia')
        plt.ylabel('Valor da Quota (R$)')
        plt.grid(True)
        plt.show()
        retornar_menu()

    elif acao_escolhida == "2":
        informes_diarios = pd.read_csv(link_escolhido, sep=";", compression="zip")
        informes_diarios['DT_DIA'] = informes_diarios['DT_COMPTC'].str[-2:].astype(int)
        ultimo_dia = informes_diarios['DT_DIA'].max()
        comparativo = informes_diarios[informes_diarios['DT_DIA'] == ultimo_dia]
        comparativo = comparativo.sort_values(by='VL_PATRIM_LIQ', ascending=True)
        Fundo_com_menor_pl = comparativo.head(1)
        Fundo_com_menor_pl.loc[:, 'VL_PATRIM_LIQ'] = Fundo_com_menor_pl['VL_PATRIM_LIQ'].apply(lambda x: '{:,.2f}'.format(x))
        CNPJ_Fundo_com_menor_pl = Fundo_com_menor_pl['CNPJ_FUNDO'].iloc[0]
        informes_diarios_filtered_condiction = informes_diarios['CNPJ_FUNDO'] == CNPJ_Fundo_com_menor_pl
        informes_diarios_filtered = informes_diarios[informes_diarios_filtered_condiction]
        informes_diarios_filtered['VL_QUOTA'] = informes_diarios['VL_QUOTA']
        print(f"""\tO fundo que obteve o menor PL no mês selecionado foi o fundo inscrito sobre o CNPJ de número: {Fundo_com_menor_pl['CNPJ_FUNDO'].values[0]},
acumulando um valor patrimonial total de: R${Fundo_com_menor_pl['VL_PATRIM_LIQ'].values[0]}!\t """)
        informes_diarios_filtered.plot(x='DT_DIA', y='VL_QUOTA', color='blue', linestyle='-', marker='o', markersize=3)
        plt.title('Evolução do Valor da Quota - Fundo com Menor PL')
        plt.xlabel('Dia')
        plt.ylabel('Valor da Quota (R$)')
        plt.grid(True)
        plt.show()
        retornar_menu()

    else:
        print("Há algo de errado com essa operação! Tente novamente!")

main()