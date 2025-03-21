import requests
import json
import time
from datetime import datetime

url = "https://rest-api-lv.betburger.com/api/v1/arbs/pro_search?access_token=a3bcb1c670546b8b3d2d6cb8a92822ec&locale=en"

headers = {
    "accept": "application/json, text/plain, */*",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.betburger.com",
    "referer": "https://www.betburger.com/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

data = """auto_update=true&notification_sound=false&notification_popup=false&show_event_arbs=true&grouped=true&per_page=20&sort_by=percent&koef_format=decimal&mode=&event_id=&q=&is_live=true&event_arb_types[]=1&event_arb_types[]=2&event_arb_types[]=3&event_arb_types[]=4&event_arb_types[]=5&event_arb_types[]=6&event_arb_types[]=7&event_arb_types[]=8&event_arb_types[]=9&event_arb_types[]=10&search_filter[]=1706129&search_filter[]=1706130&search_filter[]=1706131&bk_ids[]=1&bk_ids[]=3&bk_ids[]=8&bk_ids[]=9&bk_ids[]=10&bk_ids[]=11&bk_ids[]=15&bk_ids[]=16&bk_ids[]=18&bk_ids[]=19"""

def format_arb(arb):
    return (
        "\n⏱ {}\n🏟 Evento: {}\n🆚 Times: {} x {}\n🌍 Liga: {}\n📈 Lucro: {}%\n🎯 Odds: {} ~ {}\n{}\n".format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            arb.get('name'),
            arb.get('home'),
            arb.get('away'),
            arb.get('league'),
            arb.get('percent'),
            arb.get('min_koef'),
            arb.get('max_koef'),
            "-" * 40
        )
    )

fetch_interval = 10
print("📡 Iniciando coleta contínua de arbitragens ao vivo...", flush=True)

while True:
    try:
        response = requests.post(url, headers=headers, data=data)
        parsed = response.json()
        arbs = parsed.get("arbs") or parsed.get("event_arbs") or parsed.get("bets") or []
        
        if arbs:
            print(f"✅ {len(arbs)} arbitragens recebidas", flush=True)
            for arb in arbs:
                print(format_arb(arb), flush=True)
        else:
            print("⚠️ Nenhuma arbitragem nesse ciclo", flush=True)
    except Exception as e:
        print(f"[ERRO] {e}", flush=True)
    
    time.sleep(fetch_interval)
