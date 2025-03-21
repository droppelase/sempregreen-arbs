import requests
import time
import sys

# URL da API do BetBurger
URL = "https://rest-api-lv.betburger.com/api/v1/arbs/pro_search"
TOKEN = "SEU_TOKEN_AQUI"  # Substitua pelo seu token real

# Tempo entre requisições (em segundos)
INTERVALO = 60  # 1 minuto

while True:
    try:
        print("🔍 Fazendo requisição para a API da BetBurger...", flush=True)

        # Parâmetros da requisição
        params = {
            "access_token": TOKEN,
            "auto_update": "true",
            "is_live": "true",  # Somente surebets ao vivo
            "per_page": 20,
            "sort_by": "percent",
            "koef_format": "decimal"
        }

        # Fazendo a requisição
        response = requests.post(URL, data=params)

        # Exibindo código de resposta
        print(f"🛰 Código da resposta: {response.status_code}", flush=True)

        if response.status_code == 200:
            data = response.json()

            # Exibir log da resposta JSON
            print("📦 Resposta JSON recebida", flush=True)

            # Verificar se há arbitragens (surebets)
            arbs = data.get("arbs", [])
            if arbs:
                print(f"✅ {len(arbs)} surebets encontradas!", flush=True)

                # Salvar logs em arquivo local
                with open("log_surebets.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"🔹 {time.strftime('%Y-%m-%d %H:%M:%S')} - {len(arbs)} surebets encontradas!\n")
                    for arb in arbs:
                        log_file.write(f"⚡ Jogo: {arb.get('name')}, Percentual: {arb.get('percent')}%\n")
                    log_file.write("-" * 50 + "\n")

            else:
                print("⚠️ Nenhuma surebet encontrada no momento.", flush=True)

        else:
            print(f"❌ Erro na requisição: {response.text}", flush=True)

        # Forçar exibição dos logs no Render
        sys.stdout.flush()

    except Exception as e:
        print(f"🚨 Erro inesperado: {e}", flush=True)

    # Aguardar antes de fazer a próxima requisição
    time.sleep(INTERVALO)
