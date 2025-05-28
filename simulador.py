import streamlit as st
import pandas as pd
from copy import deepcopy

# --- Configurações Iniciais ---
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 250)
pd.set_option('display.colheader_justify', 'left')
st.set_page_config(layout="wide", page_title="FSA - Simulador Playoffs Lib/Sula")

# --- Funções do Backend ---
def calcular_sg(gp, gc):
    return gp - gc

def inicializar_dados_times_st():
    # IMPORTANTE: Substitua 'URL_ESCUDO_...' pelas URLs reais dos escudos dos times
    lib_data = { # PREENCHA COM SEUS DADOS COMPLETOS E URLs DE ESCUDO
        "A": [
            {'nome': 'Estudiantes', 'pontos': 12, 'jogos': 5, 'gp': 11, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Escudo_del_Club_Estudiantes_de_La_Plata.svg/824px-Escudo_del_Club_Estudiantes_de_La_Plata.svg.png'},
            {'nome': 'Botafogo', 'pontos': 12, 'jogos': 6, 'gp': 8, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/c/cb/Escudo_Botafogo.png'},
            {'nome': 'Universidad de Chile', 'pontos': 10, 'jogos': 6, 'gp': 8, 'gc': 8, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/5/50/C.F._Universidad_de_Chile_logo.png'},
            {'nome': 'Carabobo', 'pontos': 1, 'jogos': 6, 'gp': 2, 'gc': 13, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/8/88/Carabobo_F.C.png'},
        ],
        "B": [
            {'nome': 'River Plate', 'pontos': 12, 'jogos': 6, 'gp': 13, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Escudo_del_C_A_River_Plate.svg/1653px-Escudo_del_C_A_River_Plate.svg.png'},
            {'nome': 'Universitario', 'pontos': 8, 'jogos': 6, 'gp': 4, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Logo_oficial_de_Universitario.png/600px-Logo_oficial_de_Universitario.png'},
            {'nome': 'Independiente del Valle', 'pontos': 8, 'jogos': 6, 'gp': 8, 'gc': 11, 'escudo_url': 'https://logodetimes.com/times/independiente-del-valle/logo-independiente-del-valle-2048.png'},
            {'nome': 'Barcelona SC', 'pontos': 4, 'jogos': 6, 'gp': 4, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6a/Barcelona_Sporting_Club_Logo.png'},
        ],
        "C": [
            {'nome': 'Central Córdoba S.Estero', 'pontos': 11, 'jogos': 5, 'gp': 7, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Escudo_del_Club_Central_C%C3%B3rdoba_de_Santiago_del_Estero.svg/1200px-Escudo_del_Club_Central_C%C3%B3rdoba_de_Santiago_del_Estero.svg.png'},
            {'nome': 'Flamengo', 'pontos': 8, 'jogos': 5, 'gp': 5, 'gc': 3, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/9/93/Flamengo-RJ_%28BRA%29.png'},
            {'nome': 'LDU Quito', 'pontos': 8, 'jogos': 5, 'gp': 5, 'gc': 4, 'escudo_url': 'https://logodetimes.com/times/ldu-liga-de-quito/logo-ldu-liga-de-quito-1536.png'},
            {'nome': 'Deportivo Táchira', 'pontos': 0, 'jogos': 5, 'gp': 4, 'gc': 10, 'escudo_url': 'https://www.ogol.com.br/img/logos/equipas/2409_imgbank_1741861903.png'},
        ],
        "D": [
            {'nome': 'São Paulo', 'pontos': 14, 'jogos': 6, 'gp': 10, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/2054px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png'},
            {'nome': 'Libertad', 'pontos': 9, 'jogos': 6, 'gp': 6, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6b/Club_Libertad.png'},
            {'nome': 'Alianza Lima', 'pontos': 5, 'jogos': 6, 'gp': 7, 'gc': 11, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Escudo_Alianza_Lima.svg/1611px-Escudo_Alianza_Lima.svg.png'},
            {'nome': 'Talleres', 'pontos': 4, 'jogos': 6, 'gp': 5, 'gc': 8, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Escudo_Talleres_2015.svg/1200px-Escudo_Talleres_2015.svg.png'},
        ],
        "E": [
            {'nome': 'Racing Club', 'pontos': 10, 'jogos': 5, 'gp': 13, 'gc': 3, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Escudo_de_Racing_Club_%282014%29.svg/1686px-Escudo_de_Racing_Club_%282014%29.svg.png'},
            {'nome': 'Fortaleza', 'pontos': 8, 'jogos': 5, 'gp': 8, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Escudo_do_Fortaleza_EC.png'},
            {'nome': 'Atlético Bucaramanga', 'pontos': 2, 'jogos': 5, 'gp': 6, 'gc': 9, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/3/3b/CAtl%C3%A9ticoBucaramangaCD.png'},
            {'nome': 'Colo-Colo', 'pontos': 2, 'jogos': 5, 'gp': 4, 'gc': 15, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/e/e8/Colo-Colo_Futbol_Club.png'},
        ],
        "F": [
            {'nome': 'Atlético Nacional', 'pontos': 9, 'jogos': 5, 'gp': 7, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/d/d7/Atl%C3%A9tico_Nacional.png'},
            {'nome': 'Internacional', 'pontos': 8, 'jogos': 5, 'gp': 10, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Escudo_do_Sport_Club_Internacional.svg'},
            {'nome': 'Bahia', 'pontos': 7, 'jogos': 5, 'gp': 4, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/9/90/ECBahia.png'},
            {'nome': 'Nacional', 'pontos': 4, 'jogos': 5, 'gp': 4, 'gc': 10, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Escudo_del_Club_Nacional_de_Football.svg/1024px-Escudo_del_Club_Nacional_de_Football.svg.png'},
        ],
        "G": [
            {'nome': 'Palmeiras', 'pontos': 15, 'jogos': 5, 'gp': 11, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Palmeiras_logo.svg/2048px-Palmeiras_logo.svg.png'},
            {'nome': 'Cerro Porteño', 'pontos': 7, 'jogos': 5, 'gp': 7, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/5/5b/Escudo_del_Club_Cerro_Porte%C3%B1o.png'},
            {'nome': 'Sporting Cristal', 'pontos': 4, 'jogos': 5, 'gp': 6, 'gc': 10, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Escudo_del_Club_Sporting_Cristal.svg/1200px-Escudo_del_Club_Sporting_Cristal.svg.png'},
            {'nome': 'Bolívar', 'pontos': 3, 'jogos': 5, 'gp': 8, 'gc': 11, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Emblem_bolivar.png/538px-Emblem_bolivar.png'},
        ],
        "H": [
            {'nome': 'Vélez Sarsfield', 'pontos': 10, 'jogos': 5, 'gp': 11, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/2/21/Escudo_del_Club_Atl%C3%A9tico_V%C3%A9lez_Sarsfield.svg'},
            {'nome': 'Peñarol', 'pontos': 10, 'jogos': 5, 'gp': 9, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Escudo_de_Pe%C3%B1arol.svg/1200px-Escudo_de_Pe%C3%B1arol.svg.png'},
            {'nome': 'San Antonio Bulo Bulo', 'pontos': 6, 'jogos': 5, 'gp': 5, 'gc': 11, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/c/c8/CD_San_Antonio_Bulo_Bulo.png'},
            {'nome': 'Olimpia', 'pontos': 2, 'jogos': 5, 'gp': 6, 'gc': 11, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/4/4a/Logo_de_Olimpia_2022_PNG_HD.png'},
        ],
    }
    sula_data = { # PREENCHA COM SEUS DADOS COMPLETOS E URLs DE ESCUDO
        "A": [
            {'nome': 'Independiente', 'pontos': 9, 'jogos': 5, 'gp': 9, 'gc': 6, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Escudo_del_Club_Atl%C3%A9tico_Independiente.svg/1200px-Escudo_del_Club_Atl%C3%A9tico_Independiente.svg.png'},
            {'nome': 'Guaraní', 'pontos': 8, 'jogos': 5, 'gp': 9, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/7/7f/ClubGuaran%C3%AD.png'},
            {'nome': 'Nacional Potosí', 'pontos': 4, 'jogos': 5, 'gp': 8, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Club_Atletico_Nacional_Potosi.svg/671px-Club_Atletico_Nacional_Potosi.svg.png'},
            {'nome': 'Boston River', 'pontos': 1, 'jogos': 5, 'gp': 5, 'gc': 14, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Escudo_Boston_River_2019.png/1200px-Escudo_Boston_River_2019.png'},
        ],
        "B": [
            {'nome': 'Universidad Católica', 'pontos': 9, 'jogos': 5, 'gp': 11, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/d/db/UniversidadCat%C3%B3licaECU.png'},
            {'nome': 'Vitória', 'pontos': 6, 'jogos': 5, 'gp': 3, 'gc': 3, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/3/34/Esporte_Clube_Vit%C3%B3ria_logo.png'},
            {'nome': 'Defensa y Justicia', 'pontos': 4, 'jogos': 5, 'gp': 5, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/d/db/EscudoDefensayjustica.png'},
            {'nome': 'Cerro Largo', 'pontos': 1, 'jogos': 5, 'gp': 3, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Escudo_Cerro_Largo_F%C3%BAtbol_Club.png/640px-Escudo_Cerro_Largo_F%C3%BAtbol_Club.png'},
        ],
         "C": [
            {'nome': 'Huracán', 'pontos': 14, 'jogos': 6, 'gp': 11, 'gc': 2, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Emblema_oficial_del_Club_Atl%C3%A9tico_Hurac%C3%A1n.svg/1262px-Emblema_oficial_del_Club_Atl%C3%A9tico_Hurac%C3%A1n.svg.png'},
            {'nome': 'Corinthians', 'pontos': 8, 'jogos': 6, 'gp': 5, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/b/b4/Corinthians_simbolo.png'},
            {'nome': 'Racing (URU)', 'pontos': 1, 'jogos': 6, 'gp': 3, 'gc': 14, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Racing_Club_Escudo.png/250px-Racing_Club_Escudo.png'},
            {'nome': 'América de Cali(COL)', 'pontos': 8, 'jogos': 6, 'gp': 6, 'gc': 4, 'escudo_url': 'https://www.ogol.com.br/img/logos/equipas/2292_imgbank_1688117075.png'},
        ],
        "D": [
            {'nome': 'Godoy Cruz', 'pontos': 11, 'jogos': 5, 'gp': 8, 'gc': 3, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/8/89/Logo_of_CD_Godoy_Cruz_Antonio_Tomba.png'},
            {'nome': 'Grêmio', 'pontos': 9, 'jogos': 5, 'gp': 7, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Gremio_logo.svg/1718px-Gremio_logo.svg.png'},
            {'nome': 'Atlético Grau', 'pontos': 3, 'jogos': 5, 'gp': 3, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/8/89/Logo_of_CD_Godoy_Cruz_Antonio_Tomba.png'},
            {'nome': 'Sportivo Luqueño', 'pontos': 2, 'jogos': 5, 'gp': 4, 'gc': 8, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/c/ca/Club_Sportivo_Luqueno.png'},
        ],
        "E": [
            {'nome': 'Mushuc Runa', 'pontos': 13, 'jogos': 5, 'gp': 10, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/3/39/Mushuc_Runa_SC.png'},
            {'nome': 'Palestino', 'pontos': 9, 'jogos': 5, 'gp': 5, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/7/72/CDPalestino.png'},
            {'nome': 'Cruzeiro', 'pontos': 4, 'jogos': 5, 'gp': 2, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/b/bc/Logo_Cruzeiro_1996.png'},
            {'nome': 'Unión', 'pontos': 3, 'jogos': 5, 'gp': 5, 'gc': 8, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Escudo_del_Club_Atl%C3%A9tico_Uni%C3%B3n.svg/1200px-Escudo_del_Club_Atl%C3%A9tico_Uni%C3%B3n.svg.png'},
        ],
        "F": [
            {'nome': 'Once Caldas', 'pontos': 12, 'jogos': 5, 'gp': 8, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Once_Caldas_logo-svg.svg/1693px-Once_Caldas_logo-svg.svg.png'},
            {'nome': 'Fluminense', 'pontos': 10, 'jogos': 5, 'gp': 9, 'gc': 2, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/a/ad/Fluminense_FC_escudo.png'},
            {'nome': 'Gualberto Villarroel', 'pontos': 4, 'jogos': 5, 'gp': 5, 'gc': 11, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/f/f9/Escudo_GV_Club_Deportivo_San_Jos%C3%A9_PNG.png'},
            {'nome': 'Unión Española', 'pontos': 2, 'jogos': 5, 'gp': 2, 'gc': 7, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/9/93/Uni%C3%B3n_Espa%C3%B1ola_logo.png'},
        ],
        "G": [
            {'nome': 'Lanús', 'pontos': 12, 'jogos': 6, 'gp': 9, 'gc': 4, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Lanus_Atualiza.png/1024px-Lanus_Atualiza.png'},
            {'nome': 'Vasco', 'pontos': 8, 'jogos': 6, 'gp': 8, 'gc': 8, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/a/ac/CRVascodaGama.png'},
            {'nome': 'FBC Melgar', 'pontos': 7, 'jogos': 6, 'gp': 6, 'gc': 10, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/2/26/Foot_Ball_Club_Melgar.png'},
            {'nome': 'Academia Puerto Cabello', 'pontos': 5, 'jogos': 6, 'gp': 5, 'gc': 6, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/a/a7/Academia_Puerto_Cabello.png'},
        ],
        "H": [
            {'nome': 'Cienciano', 'pontos': 9, 'jogos': 5, 'gp': 11, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Escudo_Cienciano.png/960px-Escudo_Cienciano.png'},
            {'nome': 'Atlético Mineiro', 'pontos': 8, 'jogos': 5, 'gp': 10, 'gc': 5, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/commons/5/5f/Atletico_mineiro_galo.png'},
            {'nome': 'Caracas FC', 'pontos': 5, 'jogos': 5, 'gp': 7, 'gc': 10, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/f/f4/Caracas_FC.png'},
            {'nome': 'Deportes Iquique', 'pontos': 4, 'jogos': 5, 'gp': 6, 'gc': 14, 'escudo_url': 'https://upload.wikimedia.org/wikipedia/pt/f/f4/Caracas_FC.png'},
        ],
    }

    db = {"Libertadores": {}, "Sul-Americana": {}}
    for competicao_nome, data_competicao in [("Libertadores", lib_data), ("Sul-Americana", sula_data)]:
        for grupo, times in data_competicao.items():
            db[competicao_nome][grupo] = []
            for time_data in times:
                time_data_copy = deepcopy(time_data)
                if 'sg' not in time_data_copy: 
                    time_data_copy['sg'] = calcular_sg(time_data_copy['gp'], time_data_copy['gc'])
                if 'escudo_url' not in time_data_copy: 
                    time_data_copy['escudo_url'] = ""
                db[competicao_nome][grupo].append(time_data_copy)
            ordenar_grupo_st(db, competicao_nome, grupo)
    st.session_state.database_competicoes = db
    st.session_state.database_competicoes_original = deepcopy(db) # Salva a cópia original aqui

def inicializar_jogos_pendentes_st():
    jogos_completos = [ # PREENCHA COM SEUS DADOS COMPLETOS
        {'competicao': 'Libertadores', 'grupo': 'F', 'data': '28/05', 'casa': 'Nacional', 'visitante': 'Atlético Nacional', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Libertadores', 'grupo': 'F', 'data': '28/05', 'casa': 'Internacional', 'visitante': 'Bahia', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Libertadores', 'grupo': 'G', 'data': '28/05', 'casa': 'Bolívar', 'visitante': 'Cerro Porteño', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Libertadores', 'grupo': 'C', 'data': '28/05', 'casa': 'Flamengo', 'visitante': 'Deportivo Táchira', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Libertadores', 'grupo': 'G', 'data': '28/05', 'casa': 'Palmeiras', 'visitante': 'Sporting Cristal', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Libertadores', 'grupo': 'C', 'data': '28/05', 'casa': 'LDU Quito', 'visitante': 'Central Córdoba S.Estero', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Libertadores', 'grupo': 'H', 'data': '29/05', 'casa': 'Peñarol', 'visitante': 'Vélez Sarsfield', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Libertadores', 'grupo': 'H', 'data': '29/05', 'casa': 'Olimpia', 'visitante': 'San Antonio Bulo Bulo', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Libertadores', 'grupo': 'E', 'data': '29/05', 'casa': 'Colo-Colo', 'visitante': 'Atlético Bucaramanga', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Libertadores', 'grupo': 'E', 'data': '29/05', 'casa': 'Racing Club', 'visitante': 'Fortaleza', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'A', 'data': '28/05', 'casa': 'Guaraní', 'visitante': 'Boston River', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'A', 'data': '28/05', 'casa': 'Independiente', 'visitante': 'Nacional Potosí', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'E', 'data': '28/05', 'casa': 'Palestino', 'visitante': 'Mushuc Runa', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'B', 'data': '28/05', 'casa': 'Universidad Católica', 'visitante': 'Vitória', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'B', 'data': '28/05', 'casa': 'Defensa y Justicia', 'visitante': 'Cerro Largo', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'E', 'data': '28/05', 'casa': 'Cruzeiro', 'visitante': 'Unión', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'D', 'data': '29/05', 'casa': 'Grêmio', 'visitante': 'Sportivo Luqueño', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'D', 'data': '29/05', 'casa': 'Godoy Cruz', 'visitante': 'Atlético Grau', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'H', 'data': '29/05', 'casa': 'Caracas FC', 'visitante': 'Deportes Iquique', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'H', 'data': '29/05', 'casa': 'Atlético Mineiro', 'visitante': 'Cienciano', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'F', 'data': '29/05', 'casa': 'Unión Española', 'visitante': 'Gualberto Villarroel', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
        {'competicao': 'Sul-Americana', 'grupo': 'F', 'data': '29/05', 'casa': 'Fluminense', 'visitante': 'Once Caldas', 'simulado': False, 'gols_casa': 0, 'gols_visitante': 0},
    ]
    st.session_state.jogos_pendentes = deepcopy(jogos_completos)

def encontrar_time_st(db, competicao, grupo, nome_time_procurado):
    try:
        if competicao in db and grupo in db[competicao]:
            for index, time_obj in enumerate(db[competicao][grupo]):
                if time_obj['nome'] == nome_time_procurado:
                    return index, time_obj # Retorna o objeto diretamente
        return -1, None
    except KeyError:
        return -1, None

def atualizar_pontuacao_time(gols_feitos, gols_sofridos): # Removido _st e time_obj
    if gols_feitos > gols_sofridos:
        return 3
    elif gols_feitos == gols_sofridos:
        return 1
    return 0

def aplicar_resultado_jogo_st(db, competicao, grupo, nome_casa, nome_visitante, gols_casa, gols_visitante):
    # Esta função agora opera diretamente nos objetos dentro de 'db' que é st.session_state.database_competicoes
    idx_casa, time_casa_obj_ref = encontrar_time_st(db, competicao, grupo, nome_casa)
    idx_visitante, time_visitante_obj_ref = encontrar_time_st(db, competicao, grupo, nome_visitante)

    if time_casa_obj_ref and time_visitante_obj_ref:
        time_casa_obj_ref['jogos'] += 1
        time_casa_obj_ref['gp'] += gols_casa
        time_casa_obj_ref['gc'] += gols_visitante
        time_casa_obj_ref['sg'] = calcular_sg(time_casa_obj_ref['gp'], time_casa_obj_ref['gc'])
        time_casa_obj_ref['pontos'] += atualizar_pontuacao_time(gols_casa, gols_visitante)

        time_visitante_obj_ref['jogos'] += 1
        time_visitante_obj_ref['gp'] += gols_visitante
        time_visitante_obj_ref['gc'] += gols_casa
        time_visitante_obj_ref['sg'] = calcular_sg(time_visitante_obj_ref['gp'], time_visitante_obj_ref['gc'])
        time_visitante_obj_ref['pontos'] += atualizar_pontuacao_time(gols_visitante, gols_casa)
        
        ordenar_grupo_st(db, competicao, grupo) # 'db' aqui é st.session_state.database_competicoes
        return True
    return False

def ordenar_grupo_st(db, competicao, grupo_id):
    try:
        if competicao in db and grupo_id in db[competicao]:
            db[competicao][grupo_id].sort(
                key=lambda t: (t['pontos'], t['sg'], t['gp'], t['nome']),
                reverse=True
            )
    except KeyError:
        st.error(f"ERRO INTERNO (KeyError ao ordenar): Competição '{competicao}' ou Grupo '{grupo_id}' não encontrado.")

def extrair_qualificados_para_playoffs_st(db):
    terceiros_libertadores_lista = []
    if "Libertadores" in db:
        for grupo_id, times_do_grupo in db["Libertadores"].items():
            if times_do_grupo and len(times_do_grupo) >= 3:
                terceiros_libertadores_lista.append(deepcopy(times_do_grupo[2]))
    segundos_sulamericana_lista = []
    if "Sul-Americana" in db:
        for grupo_id, times_do_grupo in db["Sul-Americana"].items():
            if times_do_grupo and len(times_do_grupo) >= 2:
                segundos_sulamericana_lista.append(deepcopy(times_do_grupo[1]))
    terceiros_libertadores_lista.sort(key=lambda t: (t['pontos'], t['sg'], t['gp'], t['nome']), reverse=True)
    segundos_sulamericana_lista.sort(key=lambda t: (t['pontos'], t['sg'], t['gp'], t['nome']), reverse=False)
    return terceiros_libertadores_lista, segundos_sulamericana_lista

# --- Funções de Exibição --- (Mantidas como antes com HTML para escudos)
def display_group_standings_st(competicao_nome, grupo_id, times_do_grupo):
    if not times_do_grupo:
        st.write(" (Vazio)")
        return
    html_table = "<table style='width:100%; border-collapse: collapse; font-size: 0.9em;'>" # Reduzindo fonte
    html_table += "<tr><th style='text-align:left; padding: 2px;'>Pos.</th><th colspan=2 style='text-align:left; padding: 2px;'>Nome</th><th style='padding: 2px;'>P</th><th style='padding: 2px;'>J</th><th style='padding: 2px;'>GP</th><th style='padding: 2px;'>GC</th><th style='padding: 2px;'>SG</th></tr>"
    for i, time_obj in enumerate(times_do_grupo):
        escudo_html = f"<img src='{time_obj.get('escudo_url', '')}' style='width:18px; height:18px; margin-right:4px; vertical-align:middle;' onerror='this.style.display=\"none\"' />" if time_obj.get('escudo_url') else ""
        html_table += f"<tr><td style='padding: 2px;'>{i+1}</td><td style='padding: 0px 2px;'>{escudo_html}</td><td style='text-align:left; padding: 2px;'>{time_obj['nome']}</td><td style='padding: 2px;'>{time_obj['pontos']}</td><td style='padding: 2px;'>{time_obj['jogos']}</td><td style='padding: 2px;'>{time_obj['gp']}</td><td style='padding: 2px;'>{time_obj['gc']}</td><td style='padding: 2px;'>{time_obj['sg']}</td></tr>"
    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)

def display_all_standings_st(db, titulo_geral="Classificação Atual"):
    st.header(titulo_geral)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Libertadores")
        if "Libertadores" in db and db["Libertadores"]:
            for grupo_id_lib, times_lib in sorted(db["Libertadores"].items()):
                with st.expander(f"Grupo {grupo_id_lib}", expanded=False):
                    display_group_standings_st("Libertadores", grupo_id_lib, times_lib)
        else:
            st.write("Dados da Libertadores não disponíveis.")
    with col2:
        st.subheader("🏆 Sul-Americana")
        if "Sul-Americana" in db and db["Sul-Americana"]:
            for grupo_id_sula, times_sula in sorted(db["Sul-Americana"].items()):
                with st.expander(f"Grupo {grupo_id_sula}", expanded=False):
                    display_group_standings_st("Sul-Americana", grupo_id_sula, times_sula)
        else:
            st.write("Dados da Sul-Americana não disponíveis.")

def display_playoff_lists_st(lista_de_times, titulo_lista):
    st.subheader(titulo_lista)
    if not lista_de_times:
        st.write("Nenhum time nesta lista.")
        return
    html_table = "<table style='width:100%; border-collapse: collapse; font-size: 0.9em;'>"
    html_table += "<tr><th style='text-align:left; padding: 2px;'>Pos.</th><th colspan=2 style='text-align:left; padding: 2px;'>Nome</th><th style='padding: 2px;'>P</th><th style='padding: 2px;'>J</th><th style='padding: 2px;'>GP</th><th style='padding: 2px;'>GC</th><th style='padding: 2px;'>SG</th></tr>"
    for i, time_obj in enumerate(lista_de_times):
        escudo_html = f"<img src='{time_obj.get('escudo_url', '')}' style='width:18px; height:18px; margin-right:4px; vertical-align:middle;' onerror='this.style.display=\"none\"' />" if time_obj.get('escudo_url') else ""
        html_table += f"<tr><td style='padding: 2px;'>{i+1}</td><td style='padding: 0px 2px;'>{escudo_html}</td><td style='text-align:left; padding: 2px;'>{time_obj['nome']}</td><td style='padding: 2px;'>{time_obj['pontos']}</td><td style='padding: 2px;'>{time_obj['jogos']}</td><td style='padding: 2px;'>{time_obj['gp']}</td><td style='padding: 2px;'>{time_obj['gc']}</td><td style='padding: 2px;'>{time_obj['sg']}</td></tr>"
    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)

def display_playoff_matchups_st(lista_libertadores, lista_sulamericana):
    st.header("⚔️ Confrontos Definidos (Playoffs Sul-Americana)")
    num_confrontos = min(len(lista_libertadores), len(lista_sulamericana))
    if num_confrontos == 0:
        st.write("Não há times suficientes para gerar confrontos.")
        return
    matchups_data = []
    for i in range(num_confrontos):
        time_lib = lista_libertadores[i]
        time_sul = lista_sulamericana[i]
        escudo_lib_html = f"<img src='{time_lib.get('escudo_url', '')}' style='width:18px; height:18px; margin-right:4px; vertical-align:middle;' onerror='this.style.display=\"none\"' />" if time_lib.get('escudo_url') else ""
        escudo_sul_html = f"<img src='{time_sul.get('escudo_url', '')}' style='width:18px; height:18px; margin-right:4px; vertical-align:middle;' onerror='this.style.display=\"none\"' />" if time_sul.get('escudo_url') else ""
        matchups_data.append({
            'Chave': f"Playoff {chr(ord('A') + i)}",
            'Time Libertadores (3º)': f"{escudo_lib_html} {time_lib['nome']} (P:{time_lib['pontos']}, SG:{time_lib['sg']})",
            'vs': 'X',
            'Time Sul-Americana (2º)': f"{escudo_sul_html} {time_sul['nome']} (P:{time_sul['pontos']}, SG:{time_sul['sg']})"
        })
    html_confrontos = "<table style='width:100%; font-size: 0.95em;'>"
    html_confrontos += "<tr><th style='text-align:left; padding: 3px;'>Chave</th><th style='text-align:left; padding: 3px;'>Libertadores (3º)</th><th style='padding: 3px;'></th><th style='text-align:left; padding: 3px;'>Sul-Americana (2º)</th></tr>"
    for item in matchups_data:
        html_confrontos += f"<tr><td style='padding: 3px;'>{item['Chave']}</td><td style='padding: 3px;'>{item['Time Libertadores (3º)']}</td><td style='text-align:center; padding: 3px;'>{item['vs']}</td><td style='padding: 3px;'>{item['Time Sul-Americana (2º)']}</td></tr>"
    html_confrontos += "</table>"
    st.markdown(html_confrontos, unsafe_allow_html=True)

# --- Layout Principal ---
def main():
    st.title("FSA -Painel Simulador - Playoffs Libertadores / Sul-Americana")

    if 'database_competicoes_original' not in st.session_state: # Inicializa original na primeira vez
        inicializar_dados_times_st() # Isso define database_competicoes e database_competicoes_original
    if 'database_competicoes' not in st.session_state: # Garante que a cópia de trabalho exista
        st.session_state.database_competicoes = deepcopy(st.session_state.database_competicoes_original)
    if 'jogos_pendentes' not in st.session_state:
        inicializar_jogos_pendentes_st()

    if st.sidebar.button("🔄 Resetar Dados e Simulações", key="reset_button_main"):
        st.session_state.database_competicoes = deepcopy(st.session_state.database_competicoes_original)
        inicializar_jogos_pendentes_st()
        st.sidebar.success("Dados e simulações resetados!")
        st.rerun() # CORRIGIDO

    st.sidebar.header("Simular Jogos Pendentes")
    if 'jogos_pendentes' in st.session_state and st.session_state.jogos_pendentes:
        for idx, jogo_pendente_ref in enumerate(st.session_state.jogos_pendentes):
            if not jogo_pendente_ref['simulado']:
                with st.sidebar.expander(f"{jogo_pendente_ref['competicao']} Gr.{jogo_pendente_ref['grupo']}: {jogo_pendente_ref['casa']} vs {jogo_pendente_ref['visitante']}", expanded=False):
                    key_base = f"jogo_{idx}"
                    cols_score = st.columns(2)
                    gols_casa_input = cols_score[0].number_input(f"Gols {jogo_pendente_ref['casa']}", min_value=0, value=int(jogo_pendente_ref.get('gols_casa', 0)), step=1, key=f"{key_base}_casa_in")
                    gols_visitante_input = cols_score[1].number_input(f"Gols {jogo_pendente_ref['visitante']}", min_value=0, value=int(jogo_pendente_ref.get('gols_visitante', 0)), step=1, key=f"{key_base}_vis_in")
                    if st.button("Simular Jogo", key=f"{key_base}_btn_sim"):
                        st.session_state.jogos_pendentes[idx]['gols_casa'] = gols_casa_input
                        st.session_state.jogos_pendentes[idx]['gols_visitante'] = gols_visitante_input
                        success = aplicar_resultado_jogo_st(
                            st.session_state.database_competicoes, # Passa a referência da cópia de trabalho
                            st.session_state.jogos_pendentes[idx]['competicao'],
                            st.session_state.jogos_pendentes[idx]['grupo'],
                            st.session_state.jogos_pendentes[idx]['casa'],
                            st.session_state.jogos_pendentes[idx]['visitante'],
                            gols_casa_input,
                            gols_visitante_input
                        )
                        if success:
                            st.session_state.jogos_pendentes[idx]['simulado'] = True
                            st.success(f"Resultado: {st.session_state.jogos_pendentes[idx]['casa']} {gols_casa_input} x {gols_visitante_input} {st.session_state.jogos_pendentes[idx]['visitante']}")
                            st.rerun() # CORRIGIDO
                        else:
                            st.error("Erro ao aplicar resultado. Verifique os nomes dos times.")
            else:
                with st.sidebar.expander(f"✅ {jogo_pendente_ref['competicao']} Gr.{jogo_pendente_ref['grupo']}: {jogo_pendente_ref['casa']} {jogo_pendente_ref.get('gols_casa',0)} x {jogo_pendente_ref.get('gols_visitante',0)} {jogo_pendente_ref['visitante']}", expanded=False):
                    st.caption("Simulado.")
    else:
        st.sidebar.warning("Jogos pendentes não carregados.")

    if 'database_competicoes' in st.session_state and st.session_state.database_competicoes:
        display_all_standings_st(st.session_state.database_competicoes, "Classificação dos Grupos")
        st.markdown("---")
        terceiros_lib, segundos_sula = extrair_qualificados_para_playoffs_st(st.session_state.database_competicoes)
        col_listas1, col_listas2 = st.columns(2)
        with col_listas1:
            display_playoff_lists_st(terceiros_lib, "Melhores 3ºs da Libertadores")
        with col_listas2:
            display_playoff_lists_st(segundos_sula, "2ºs da Sul-Americana")
        st.markdown("---")
        display_playoff_matchups_st(terceiros_lib, segundos_sula)
    else:
        st.warning("Base de dados não carregada.")

if __name__ == "__main__":
    main()
