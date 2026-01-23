#!/usr/bin/env python3
"""
🤖 MASTODON BOT - URUCHAMIANIE CO 2 GODZINY
- Bot działa co 2h, ale może postować rzadziej
- Łatwe odwołanie/wyłączenie
- Prosta konfiguracja
"""

from mastodon import Mastodon
import json
import random
from datetime import datetime, date
import sys
import os

print("=" * 60)
print("🤖 MASTODON BOT - CO 2 GODZINY")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# ==================== KONFIGURACJA BOTA ====================
# ZMIENIAJ TYLKO TU ↓↓↓

CONFIG = {
    "active": True,                    # Ustaw False aby wyłączyć bota
    "max_posts_per_day": 8,           # Maks postów dziennie
    "post_frequency_hours": 2,        # Co ile godzin może postować (jeśli limit > 1)
    "post_chance_percent": 100,        # Szansa na post w danym uruchomieniu
    "exact_hours": None,              # None = dowolna godzina, lub np. [9, 15, 21]
    "timezone_offset": 1              # Przesunięcie czasu (UTC+0), zmień na 1 dla Polski zimą
}

# ==================== SPRAWDŹ CZY BOT AKTYWNY ====================

def check_bot_active():
    """Sprawdź czy bot jest włączony"""
    if not CONFIG["active"]:
        print("🔴 BOT WYŁĄCZONY - zmień CONFIG['active'] na True")
        return False
    return True

# ==================== SPRAWDŹ CZY TERAZ PUBLIKOWAĆ ====================

def should_post_now():
    """Sprawdź czy teraz jest odpowiedni czas na publikację"""
    
    # 1. Sprawdź czy bot aktywny
    if not check_bot_active():
        return False
    
    now = datetime.now()
    current_hour = (now.hour + CONFIG["timezone_offset"]) % 24
    
    print(f"⏰ Godzina lokalna: {current_hour:02d}:{now.minute:02d}")
    
    # 2. Sprawdź czy dozwolona dokładna godzina
    if CONFIG["exact_hours"] is not None:
        if current_hour not in CONFIG["exact_hours"]:
            print(f"⏭️ {current_hour}:00 - nie w dozwolonych godzinach")
            print(f"   Dozwolone: {CONFIG['exact_hours']}")
            return False
    
    # 3. Losowa szansa
    chance = random.randint(1, 100)
    if chance > CONFIG["post_chance_percent"]:
        print(f"🎲 Losowo pomijam (szansa: {chance}% > {CONFIG['post_chance_percent']}%)")
        return False
    
    # 4. Sprawdź dzienny limit
    if not check_daily_limit():
        return False
    
    # 5. Sprawdź częstotliwość (jeśli >1 post dziennie)
    if CONFIG["max_posts_per_day"] > 1:
        if not check_frequency():
            return False
    
    print(f"✅ DECYZJA: POSTUJĘ!")
    return True

def check_daily_limit():
    """Sprawdź dzienny limit postów"""
    LIMIT_FILE = "/tmp/mastodon_daily_limit.json"
    
    if os.path.exists(LIMIT_FILE):
        try:
            with open(LIMIT_FILE, "r") as f:
                limit_data = json.load(f)
        except:
            limit_data = {"date": None, "posts_today": 0}
    else:
        limit_data = {"date": None, "posts_today": 0}
    
    today = str(date.today())
    
    # Reset jeśli nowy dzień
    if limit_data.get("date") != today:
        print(f"🆕 NOWY DZIEŃ: {today} - resetuję licznik")
        limit_data = {"date": today, "posts_today": 0}
    
    # Sprawdź limit
    if limit_data["posts_today"] >= CONFIG["max_posts_per_day"]:
        print(f"⏭️ Dzisiejszy limit: {limit_data['posts_today']}/{CONFIG['max_posts_per_day']}")
        return False
    
    # Zwiększ licznik i zapisz
    limit_data["posts_today"] += 1
    try:
        with open(LIMIT_FILE, "w") as f:
            json.dump(limit_data, f, indent=2)
        print(f"📊 Licznik: {limit_data['posts_today']}/{CONFIG['max_posts_per_day']}")
    except:
        print("⚠️  Nie udało się zapisać licznika")
    
    return True

def check_frequency():
    """Sprawdź czy nie za wcześnie od ostatniego postu"""
    FREQ_FILE = "/tmp/mastodon_last_post.json"
    
    now = datetime.now()
    
    if os.path.exists(FREQ_FILE):
        try:
            with open(FREQ_FILE, "r") as f:
                last_post = json.load(f)
            last_time = datetime.fromisoformat(last_post["timestamp"])
            
            # Oblicz różnicę w godzinach
            hours_diff = (now - last_time).total_seconds() / 3600
            
            if hours_diff < CONFIG["post_frequency_hours"]:
                print(f"⏭️ Za wcześnie od ostatniego postu: {hours_diff:.1f}h < {CONFIG['post_frequency_hours']}h")
                return False
        except:
            pass
    
    # Zapisz czas obecnego postu
    try:
        with open(FREQ_FILE, "w") as f:
            json.dump({"timestamp": now.isoformat()}, f, indent=2)
    except:
        pass
    
    return True

# ==================== PRODUKTY (BEZ ZMIAN) ====================

PRODUCTS = [
    {
        "id": "QaDjw",
        "name": "How to Talk to Creditors – Word-for-Word Scripts That Actually Work",
        "url": "https://payhip.com/b/QaDjw",
        "category": "debt"
    },
    {
        "id": "fyxsZ",
        "name": "Financial First Aid – What to Do When Money Stress Hits",
        "url": "https://payhip.com/b/fyxsZ",
        "category": "stress"
    },
    {
        "id": "J4fcL",
        "name": "Debt Recovery – A Simple, Realistic Plan for Getting Out of Debt",
        "url": "https://payhip.com/b/J4fcL",
        "category": "debt"
    },
    {
        "id": "ugrLq",
        "name": "FREE Checklist - Could Money Be Waiting for You?",
        "url": "https://payhip.com/b/ugrLq",
        "category": "free"
    },
    {
        "id": "9DWGt",
        "name": "UK Budget Calculator - See Where Your Money Really Goes",
        "url": "https://payhip.com/b/9DWGt",
        "category": "budget"
    },
    {
        "id": "BvbnP",
        "name": "GET YOUR MONEY BACK",
        "url": "https://payhip.com/b/BvbnP",
        "category": "money"
    },
    {
        "id": "EDhYI",
        "name": "30$-50$ SURVIVAL FOOD SYSTEM",
        "url": "https://payhip.com/b/EDhYI",
        "category": "survival"
    },
    {
        "id": "yBiu5",
        "name": "SILENCE THE CALLS",
        "url": "https://payhip.com/b/yBiu5",
        "category": "debt"
    },
    {
        "id": "kMjr3",
        "name": "FIND YOUR HIDDEN MONEY",
        "url": "https://payhip.com/b/kMjr3",
        "category": "money"
    },
    {
        "id": "RyToE",
        "name": "MediSave Method",
        "url": "https://payhip.com/b/RyToE",
        "category": "medical"
    },
    {
        "id": "WT8JI",
        "name": "Self Relief Guide FREE",
        "url": "https://payhip.com/b/WT8JI",
        "category": "free"
    },
    {
        "id": "0YSj7",
        "name": "Financial Crisis Survival Pack – Guides to Get Back on Track",
        "url": "https://payhip.com/b/0YSj7",
        "category": "survival"
    },
    {
        "id": "6RIpj",
        "name": "The 72 Hour Cash Lifeline",
        "url": "https://payhip.com/b/6RIpj",
        "category": "emergency"
    }
]

VALUE_TEXTS = {
    "free": {"emoji": "🎁", "text": "100% FREE resource", "benefit": "Instant access"},
    "budget": {"emoji": "💰", "text": "Budget mastery tool", "benefit": "Financial clarity"},
    "debt": {"emoji": "🛡️", "text": "Debt solution", "benefit": "Peace of mind"},
    "stress": {"emoji": "😌", "text": "Stress relief guide", "benefit": "Immediate calm"},
    "survival": {"emoji": "🛠️", "text": "Emergency toolkit", "benefit": "Be prepared"},
    "medical": {"emoji": "🏥", "text": "Medical cost solution", "benefit": "Save thousands"},
    "money": {"emoji": "💵", "text": "Money recovery system", "benefit": "Find hidden cash"},
    "emergency": {"emoji": "🚨", "text": "Urgent cash solution", "benefit": "Fast relief"}
}

MOTTOS = [
    "Take control of your finances today.",
    "Your financial freedom starts here.",
    "Smart solutions for money challenges.",
    "Build a better financial future.",
    "Peace of mind is priceless."
]

CTAS = [
    "Get it now →",
    "Start today →",
    "Learn more →",
    "Get access →",
    "Check it out →"
]

HASHTAGS = {
    "free": "#FreeResource #FinancialHelp #MoneyTips",
    "budget": "#Budgeting #MoneyManagement #PersonalFinance",
    "debt": "#DebtFree #DebtHelp #FinancialFreedom",
    "stress": "#MoneyStress #FinancialWellness #StressRelief",
    "survival": "#EmergencyPrep #SurvivalTips #Preparedness",
    "medical": "#MedicalBills #HealthcareCosts #MedicalDebt",
    "money": "#MoneyTips #FindMoney #CashFlow",
    "emergency": "#EmergencyCash #UrgentHelp #QuickMoney"
}

# ==================== WYBIERZ PRODUKT ====================

def choose_product():
    """Wybierz produkt"""
    try:
        with open("/tmp/mastodon_used_today.json", "r") as f:
            used = json.load(f)
    except:
        used = {"date": str(date.today()), "used_ids": []}
    
    if used["date"] != str(date.today()):
        used = {"date": str(date.today()), "used_ids": []}
    
    available = [p for p in PRODUCTS if p["id"] not in used["used_ids"]]
    
    if not available:
        available = PRODUCTS
        used["used_ids"] = []
    
    product = random.choice(available)
    
    used["used_ids"].append(product["id"])
    try:
        with open("/tmp/mastodon_used_today.json", "w") as f:
            json.dump(used, f)
    except:
        pass
    
    return product

def create_post(product):
    """Stwórz post"""
    category = product["category"]
    value = VALUE_TEXTS.get(category, VALUE_TEXTS["budget"])
    
    post = f"{random.choice(MOTTOS)}\n\n"
    post += f"📘 {product['name']}\n"
    post += f"{value['emoji']} {value['text']}\n"
    post += f"✨ {value['benefit']}\n\n"
    post += f"{random.choice(CTAS)}\n"
    post += f"{product['url']}\n\n"
    post += f"{HASHTAGS.get(category, '#PersonalFinance #MoneyTips')}"
    
    if len(post) > 500:
        post = post[:497] + "..."
    
    return post

# ==================== GŁÓWNA FUNKCJA ====================

def main():
    """Główna funkcja"""
    print(f"\n⚙️  KONFIGURACJA:")
    print(f"   • Aktywny: {'✅ TAK' if CONFIG['active'] else '🔴 NIE'}")
    print(f"   • Max postów/dzień: {CONFIG['max_posts_per_day']}")
    print(f"   • Co ile godzin: {CONFIG['post_frequency_hours']}h")
    print(f"   • Szansa: {CONFIG['post_chance_percent']}%")
    print(f"   • Godziny: {CONFIG['exact_hours'] or 'dowolne'}")
    print("-" * 40)
    
    # 1. Sprawdź czy publikować
    if not should_post_now():
        print("\n💤 Kończę pracę - nie postuję")
        return
    
    # 2. Wybierz produkt
    product = choose_product()
    print(f"🛒 Produkt: {product['name'][:60]}...")
    print(f"📁 Kategoria: {product['category']}")
    
    # 3. Stwórz post
    post = create_post(product)
    print(f"\n📝 Post ({len(post)} znaków):")
    print("-" * 40)
    print(post)
    print("-" * 40)
    
    # 4. Połącz z Mastodon
    token = os.environ.get('MASTODON_ACCESS_TOKEN')
    url = os.environ.get('MASTODON_BASE_URL', 'https://mastodon.social')
    
    if not token:
        print("❌ Brak tokena Mastodon!")
        return
    
    try:
        mastodon = Mastodon(access_token=token, api_base_url=url)
        user = mastodon.account_verify_credentials()
        print(f"✅ Zalogowany jako: @{user['username']}")
    except Exception as e:
        print(f"❌ Błąd logowania: {e}")
        return
    
    # 5. Opublikuj
    print("\n🚀 Publikuję...")
    try:
        result = mastodon.status_post(
            status=post,
            visibility='public',
            language='en'
        )
        print(f"✅ OPUBLIKOWANO!")
        print(f"🔗 Link: {result['url']}")
        print(f"⏰ Czas: {datetime.now().strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"❌ Błąd publikacji: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 BOT ZAKOŃCZONY")
    print("=" * 60)

if __name__ == "__main__":
    main()
