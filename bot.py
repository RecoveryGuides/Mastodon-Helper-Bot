#!/usr/bin/env python3
"""
🤖 MASTODON BOT - ULTRA PROSTY
- Tylko publikowanie, zero zapisywania danych
- Losowy produkt z listy
- Działa na 100%
"""

from mastodon import Mastodon
import random
from datetime import datetime
import os

print("=" * 50)
print("🤖 MASTODON BOT - ULTRA PROSTY")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 50)

# ==================== KONFIGURACJA ====================
ACTIVE = True  # Ustaw na False aby wyłączyć

# ==================== SPRAWDŹ CZY PUBLIKOWAĆ ====================

def should_post_now():
    """Zawsze publikuj jeśli bot aktywny"""
    if not ACTIVE:
        print("🔴 BOT WYŁĄCZONY")
        return False
    
    now = datetime.now()
    current_hour = now.hour
    
    # Sprawdź czy w rozsądnych godzinach (6-22 UTC = 7-23 polski)
    if current_hour < 6 or current_hour > 22:
        print(f"⏰ {current_hour}:00 - noc, nie publikuję")
        return False
    
    # 90% szans na publikację
    if random.random() > 0.7:
        print("🎲 Losowo pomijam (30% szans)")
        return False
    
    print(f"✅ POSTUJĘ o {current_hour}:00!")
    return True

# ==================== PRODUKTY ====================

PRODUCTS = [
    {
        "name": "How to Talk to Creditors – Word-for-Word Scripts That Actually Work",
        "url": "https://payhip.com/b/QaDjw",
        "category": "debt"
    },
    {
        "name": "Financial First Aid – What to Do When Money Stress Hits",
        "url": "https://payhip.com/b/fyxsZ",
        "category": "stress"
    },
    {
        "name": "Debt Recovery – A Simple, Realistic Plan for Getting Out of Debt",
        "url": "https://payhip.com/b/J4fcL",
        "category": "debt"
    },
    {
        "name": "FREE Checklist - Could Money Be Waiting for You?",
        "url": "https://payhip.com/b/ugrLq",
        "category": "free"
    },
    {
        "name": "UK Budget Calculator - See Where Your Money Really Goes",
        "url": "https://payhip.com/b/9DWGt",
        "category": "budget"
    },
    {
        "name": "GET YOUR MONEY BACK",
        "url": "https://payhip.com/b/BvbnP",
        "category": "money"
    },
    {
        "name": "30$-50$ SURVIVAL FOOD SYSTEM",
        "url": "https://payhip.com/b/EDhYI",
        "category": "survival"
    },
    {
        "name": "SILENCE THE CALLS",
        "url": "https://payhip.com/b/yBiu5",
        "category": "debt"
    },
    {
        "name": "FIND YOUR HIDDEN MONEY",
        "url": "https://payhip.com/b/kMjr3",
        "category": "money"
    },
    {
        "name": "MediSave Method",
        "url": "https://payhip.com/b/RyToE",
        "category": "medical"
    },
    {
        "name": "Self Relief Guide FREE",
        "url": "https://payhip.com/b/WT8JI",
        "category": "free"
    },
    {
        "name": "Financial Crisis Survival Pack – Guides to Get Back on Track",
        "url": "https://payhip.com/b/0YSj7",
        "category": "survival"
    },
    {
        "name": "The 72 Hour Cash Lifeline",
        "url": "https://payhip.com/b/6RIpj",
        "category": "emergency"
    }
]

# ==================== TEKSTY ====================

MOTTOS = [
    "Take control of your finances today.",
    "Your financial freedom starts here.",
    "Smart solutions for money challenges.",
    "Build a better financial future.",
    "Peace of mind is priceless.",
    "Stop worrying about money.",
    "Get your finances back on track.",
    "Simple solutions for complex problems."
]

CTAS = [
    "Get it now →",
    "Start today →",
    "Learn more →",
    "Get access →",
    "Check it out →",
    "Download here →",
    "Grab your copy →",
    "See details →"
]

HASHTAGS = {
    "debt": "#DebtFree #DebtHelp #FinancialFreedom #MoneyHelp",
    "stress": "#MoneyStress #FinancialWellness #StressRelief #Anxiety",
    "free": "#FreeResource #FinancialHelp #MoneyTips #FreeGuide",
    "budget": "#Budgeting #MoneyManagement #PersonalFinance #SaveMoney",
    "money": "#MoneyTips #FindMoney #CashFlow #ExtraIncome",
    "survival": "#EmergencyPrep #SurvivalTips #Preparedness #Crisis",
    "medical": "#MedicalBills #HealthcareCosts #MedicalDebt #Health",
    "emergency": "#EmergencyCash #UrgentHelp #QuickMoney #FinancialEmergency"
}

# ==================== STWÓRZ POST ====================

def create_post():
    """Stwórz losowy post"""
    product = random.choice(PRODUCTS)
    category = product["category"]
    
    # Wybierz hashtagi dla kategorii
    tags = HASHTAGS.get(category, "#PersonalFinance #MoneyTips #FinancialHelp")
    
    # Stwórz post
    post = f"{random.choice(MOTTOS)}\n\n"
    post += f"📘 {product['name']}\n\n"
    post += f"{random.choice(CTAS)}\n"
    post += f"{product['url']}\n\n"
    post += f"{tags}"
    
    # Obetnij jeśli za długi
    if len(post) > 480:
        post = post[:475] + "..."
    
    return post, product

# ==================== GŁÓWNA FUNKCJA ====================

def main():
    """Główna funkcja"""
    print(f"\n⚙️  Status: {'✅ AKTYWNY' if ACTIVE else '🔴 WYŁĄCZONY'}")
    print(f"⏰ Godzina: {datetime.now().strftime('%H:%M')}")
    print("-" * 40)
    
    # 1. Sprawdź czy publikować
    if not should_post_now():
        print("\n💤 Kończę pracę")
        return
    
    # 2. Stwórz post
    post, product = create_post()
    print(f"\n🛒 Produkt: {product['name'][:50]}...")
    print(f"📁 Kategoria: {product['category']}")
    
    print(f"\n📝 Post ({len(post)} znaków):")
    print("-" * 40)
    print(post)
    print("-" * 40)
    
    # 3. Pobierz tokeny z environment
    token = os.environ.get('MASTODON_ACCESS_TOKEN')
    url = os.environ.get('MASTODON_BASE_URL', 'https://mastodon.social')
    
    if not token:
        print("❌ Brak MASTODON_ACCESS_TOKEN w sekretach!")
        return
    
    # 4. Połącz z Mastodon
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
    
    print("\n" + "=" * 50)
    print("🏁 BOT ZAKOŃCZONY")
    print("=" * 50)

if __name__ == "__main__":
    main()
