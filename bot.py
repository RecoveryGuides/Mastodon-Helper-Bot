#!/usr/bin/env python3
"""
🤖 MASTODON VALUE-FOCUSED BOT - SIMPLE VERSION
- Static product data
- 2 posts per day (change MAX_POSTS_PER_DAY)
- No GitHub history - only local memory during run
"""

from mastodon import Mastodon
import json
import random
from datetime import datetime, date
import sys
import os  # DODANE - brakowało tego importu

print("=" * 60)
print("🤖 MASTODON BOT - SIMPLE VERSION")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# ==================== KONFIGURACJA ====================

MAX_POSTS_PER_DAY = 2  # Zmień na 1, 2 lub 3

# ==================== LISTA PRODUKTÓW ====================

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

# ==================== WARTOŚĆ + HASHTAGI ====================

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

# ==================== PROSTA LOGIKA ====================

def choose_product():
    """Wybierz produkt z pamięcią sesji"""
    try:
        # Spróbuj wczytać co już było w tej sesji
        with open("/tmp/mastodon_bot_today.json", "r") as f:
            used = json.load(f)
    except:
        used = {"date": str(date.today()), "used_ids": []}
    
    # Reset jeśli nowy dzień
    if used["date"] != str(date.today()):
        used = {"date": str(date.today()), "used_ids": []}
    
    # Dostępne produkty (te nieużywane dzisiaj)
    available = [p for p in PRODUCTS if p["id"] not in used["used_ids"]]
    
    # Jeśli wszystkie użyte, zacznij od nowa
    if not available:
        available = PRODUCTS
        used["used_ids"] = []
    
    # Wybierz losowo
    product = random.choice(available)
    
    # Zapisz że użyty
    used["used_ids"].append(product["id"])
    try:
        with open("/tmp/mastodon_bot_today.json", "w") as f:
            json.dump(used, f)
    except:
        pass  # Nie przejmuj się jeśli zapis się nie uda
    
    return product

def create_post(product):
    """Stwórz prosty post"""
    category = product["category"]
    value = VALUE_TEXTS.get(category, VALUE_TEXTS["budget"])
    
    post = f"{random.choice(MOTTOS)}\n\n"
    post += f"📘 {product['name']}\n"
    post += f"{value['emoji']} {value['text']}\n"
    post += f"✨ {value['benefit']}\n\n"
    post += f"{random.choice(CTAS)}\n"
    post += f"{product['url']}\n\n"
    post += f"{HASHTAGS.get(category, '#PersonalFinance #MoneyTips')}"
    
    # Obetnij jeśli za długie
    if len(post) > 500:
        post = post[:497] + "..."
    
    return post

def main():
    """Główna funkcja - PROSTA"""
    print(f"🎯 Bot konfiguracja: {MAX_POSTS_PER_DAY} post(y) dziennie")
    
    # 1. Wybierz produkt
    product = choose_product()
    print(f"🛒 Produkt: {product['name'][:60]}...")
    print(f"📁 Kategoria: {product['category']}")
    
    # 2. Stwórz post
    post = create_post(product)
    print(f"\n📝 Post ({len(post)} znaków):")
    print("-" * 40)
    print(post)
    print("-" * 40)
    
    # 3. Połącz z Mastodon
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
    
    # 4. Opublikuj
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
