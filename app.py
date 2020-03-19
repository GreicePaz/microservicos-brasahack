from flask import Flask
from flask_restful import Resource, Api, request, abort
from lib import util, microservice

import requests, json, datetime

app = Flask(__name__)
app.config.from_pyfile("local.cfg")

api = Api(app)
        
class ImportCsvIndices(Resource):
    def post(self):
        try:
            csv_file = request.files['file']
            date = request.form['date']
        except Exception as e:
            abort(404, message=f"Parâmetros insuficientes")

        csv_json = util.csv_to_json(csv_file)

        params = microservice.analise_mensal(date, csv_json)

        # url = f"{app.config['URL_JSON_SERVER']}"

        # try:
        #     r = requests.get(url, params=retorno)
        #     response = r.json()
        # except:
        #     abort(404, message="Erro ao salvar os dados no banco.")

        return params, 200

class Configuration(Resource):
    def post(self):
        try:
            date = request.form['date']
            csv_file = request.files['file']
        except:
            abort(404, message="Parâmetros insuficientes")
        
        csv_json = util.csv_to_json(csv_file)


class Historic(Resource):
    def get(self):
        try:
            params = request.args
        except Exception as e:
            abort(404, message=str(e))
        
        if params:
            ano, mes = params['date'].split('-')
            
            search = params
            url = f"{app.config['URL_JSON_SERVER']}/persons"
            try:
                r = requests.get(url, params=search)
                persons = r.json()
            except:
                abort(404, message="Erro ao buscar no banco de dados.")

            analise_search = microservice.analise_mensal(f'{ano}-{mes}', persons)

            indicators = analise_search.get('indicators')
            
            data = util.dict_to_new_dict(params)
            
            media_months = microservice.analise_media_anual(data, app.config['URL_JSON_SERVER'])
            
        else:
            hoje = datetime.date.today().strftime('%Y-%m')
            ano, mes = hoje.split('-')

            search = {'date': f'{ano}-{mes}'}
            url = f"{app.config['URL_JSON_SERVER']}/persons"
            try:
                r = requests.get(url, params=search)
                persons = r.json()
            except:
                abort(404, message="Erro ao buscar no banco de dados.")

            analise_search = microservice.analise_mensal(f'{ano}-{mes}', persons)

            indicators = analise_search.get('indicators')

            search = {'date_like': ano}
            url = f"{app.config['URL_JSON_SERVER']}/media_months"
            try:
                r = requests.get(url, params=search)
                media_months = r.json()
            except:
                abort(404, message="Erro ao buscar no banco de dados.")

        response = {
            "historic": [
                {
                    "date": f'{ano}-{mes}',
                    "mediaMonths": media_months,
                    "persons": persons,
                    "indicators": indicators,
                    "weight": [0.1, 0.2, 0.3, 0.2, 0.05, 0.15],
                }
            ]
        }

        return response


api.add_resource(Historic, 'v1/historic')
api.add_resource(Configuration, '/v1/csv/configuration')
api.add_resource(ImportCsvIndices, '/v1/csv/indicators')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])