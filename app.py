from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import requests
import time
from threading import Thread
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',  # Forçar async mode
    logger=True,  # Logs para depuração
    engineio_logger=True
)

# Configuração da API do BetBurger
url = "https://rest-api-lv.betburger.com/api/v1/arbs/pro_search?access_token=a3bcb1c670546b8b3d2d6cb8a92822ec&locale=en"

headers = {
    "accept": "application/json, text/plain, */*",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.betburger.com",
    "referer": "https://www.betburger.com/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

data = """auto_update=true&notification_sound=false&notification_popup=false&show_event_arbs=true&grouped=true&per_page=20&sort_by=percent&koef_format=decimal&mode=&event_id=&q=&is_live=true&event_arb_types[]=1&event_arb_types[]=2&event_arb_types[]=3&event_arb_types[]=4&event_arb_types[]=5&event_arb_types[]=6&event_arb_types[]=7&event_arb_types[]=8&event_arb_types[]=9&event_arb_types[]=10&search_filter[]=1706129&search_filter[]=1706130&search_filter[]=1706131&bk_ids[]=1&bk_ids[]=3&bk_ids[]=8&bk_ids[]=9&bk_ids[]=10&bk_ids[]=11&bk_ids[]=15&bk_ids[]=16&bk_ids[]=18&bk_ids[]=19"""

def fetch_and_emit_arbs():
    with app.app_context():  # Contexto de aplicação necessário
        while True:
            try:
                response = requests.post(url, headers=headers, data=data)
                parsed = response.json()
                arbs = parsed.get("arbs") or parsed.get("event_arbs") or parsed.get("bets") or []

                formatted_arbs = [
                    {
                        "data": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "evento": arb.get('name'),
                        "times": f"{arb.get('home')} x {arb.get('away')}",
                        "liga": arb.get('league'),
                        "lucro": f"{arb.get('percent')}%",
                        "odds": f"{arb.get('min_koef')} - {arb.get('max_koef')}"
                    }
                    for arb in arbs
                ]

                # Envia as surebets para o WebSocket
                socketio.emit('update_arbs', {"arbitrages": formatted_arbs})

            except Exception as e:
                print(f"Erro ao buscar surebets: {e}")

            time.sleep(10)  # Atualiza a cada 10 segundos


@app.route('/arbitrages', methods=['GET'])
def get_arbitrages():
    """Rota tradicional via HTTP para pegar as surebets"""
    try:
        response = requests.post(url, headers=headers, data=data)
        parsed = response.json()
        arbs = parsed.get("arbs") or parsed.get("event_arbs") or parsed.get("bets") or []

        formatted_arbs = [
            {
                "data": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "evento": arb.get('name'),
                "times": f"{arb.get('home')} x {arb.get('away')}",
                "liga": arb.get('league'),
                "lucro": f"{arb.get('percent')}%",
                "odds": f"{arb.get('min_koef')} - {arb.get('max_koef')}"
            }
            for arb in arbs
        ]

        return jsonify({"arbitrages": formatted_arbs})

    except Exception as e:
        return jsonify({"error": str(e)})


# Iniciar a thread corretamente
socketio.start_background_task(fetch_and_emit_arbs)

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=PORT, allow_unsafe_werkzeug=True)
