from flask_restful import Resource, request, abort

import csv, json, requests

def analise_mensal(date, csv):
    indicadores = []
    persons = []
    total_indicador = {}
    qtd_indicador = 0

    for r in csv:
        dict_persons = {}
        for key, value in r.items():
            if not key in ['id', 'media']:
                try:
                    value = float(value)
                    if not key in indicadores:
                        total_indicador[key] = 0
                        indicadores.append(key)
                    
                    if key in indicadores:
                        if key == indicadores[0]:
                            qtd_indicador += 1
                        
                        total_indicador[key] += float(value)
                except:
                    pass
                
                dict_persons[key] = value

        media = [n for n in dict_persons.values() if type(n) == float]

        dict_persons['media'] = round(sum(media)/len(media), 1)
        dict_persons['date'] = date
        persons.append(dict_persons)
                

    indicador = []
    media_indicador = 0
    bv = 0
    for k, v in total_indicador.items():
        media = round(v/qtd_indicador, 1)
        media_indicador += media
        bv = media_indicador/len(total_indicador)
        indicador.append({
            'name': k,
            'media': media,
        })

    retorno = {
        'date': date,
        'persons': persons,
        'indicators': indicador,
        'media_indicators':  bv,
    }

    return retorno


def analise_media_anual(params, url):
    ano, mes = params['date'].split('-')

    medias = []
    media_indicators = 0
    for i in range(int(mes), 0, -1):
        date = f'{ano}-{i}'
        params['date'] = date
        url = f"{url}/persons"
        try:
            r = requests.get(url, params=params)
            persons = r.json()
        except:
            abort(404, message="Erro ao buscar no banco de dados.")
        
        if persons:
            analise_search = analise_mensal(date, persons)
            
            media_indicators = analise_search.get('media_indicators', 0)

            medias.append({'month': i, 'media': media_indicators})

    return medias


def analise_anual(date, csv):
    pass