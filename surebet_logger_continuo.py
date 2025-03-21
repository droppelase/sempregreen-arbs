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

data = "auto_update=true&notification_sound=false&notification_popup=false&show_event_arbs=true&grouped=true&per_page=20&sort_by=percent&koef_format=decimal&mode=&event_id=&q=&event_arb_types[]=1&event_arb_types[]=2&event_arb_types[]=3&event_arb_types[]=4&event_arb_types[]=5&event_arb_types[]=6&event_arb_types[]=7&event_arb_types[]=8&event_arb_types[]=9&event_arb_types[]=10&search_filter[]=1706129&search_filter[]=1706130&search_filter[]=1706131&is_live=true&bk_ids[]=1&bk_ids[]=3&bk_ids[]=8&bk_ids[]=9&bk_ids[]=10&bk_ids[]=11&bk_ids[]=15&bk_ids[]=16&bk_ids[]=18&bk_ids[]=19"

def format_arb(arb):
    return (
        "⏱ {}\n🏟 Evento: {}\n🆚 Times: {} x {}\n🌍 Liga: {}\n📈 Lucro: {}%\n🎯 Odds: {} ~ {}\n{}\n".format(
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

log_interval = 60
fetch_interval = 10
coletadas = []

print("📡 Iniciando coleta contínua de arbitragens ao vivo...")

while True:
    try:
        response = requests.post(url, headers=headers, data=data)
        parsed = response.json()
        arbs = parsed.get("arbs") or parsed.get("event_arbs") or parsed.get("bets") or []
        if arbs:
            print(f"✅ {{len(arbs)}} arbitragens recebidas")
            coletadas.extend(arbs)
        else:
            print("⚠️ Nenhuma arbitragem nesse ciclo")
    except Exception as e:
        print(f"[ERRO] {{e}}")

    if int(time.time()) % log_interval < fetch_interval:
        if coletadas:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"log_surebets_{{timestamp}}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for arb in coletadas:
                    f.write(format_arb(arb))
            print(f"📝 Log salvo: {{filename}} com {{len(coletadas)}} arbitragens")
            coletadas = []
        else:
            print("🕐 Nenhuma arbitragem para salvar neste ciclo.")
        time.sleep(fetch_interval + 1)
    else:
        time.sleep(fetch_interval)
