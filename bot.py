#!/usr/bin/env python3
"""
🤖 MASTODON VALUE-FOCUSED BOT
- Static product data (no scraping)
- 1 post dziennie na Twoim koncie
- Focus on value, not prices
"""

from mastodon import Mastodon
import os
import json
import random
from datetime import datetime, date
import sys

print("=" * 60)
print("🤖 MASTODON VALUE BOT")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# ==================== LISTA PRODUKTÓW (STATYCZNA) ====================

PRODUCTS = [
    {
        "id": "QaDjw",
        "name": "How to Talk to Creditors – Word-for-Word Scripts That Actually Work",
        "url": "https://payhip.com/b/QaDjw",
        "category": "debt",
        "description": "Professional scripts to handle creditor calls"
    },
    {
        "id": "fyxsZ",
        "name": "Financial First Aid – What to Do When Money Stress Hits",
        "url": "https://payhip.com/b/fyxsZ",
        "category": "stress",
        "description": "Emergency financial crisis management"
    },
    {
        "id": "J4fcL",
        "name": "Debt Recovery – A Simple, Realistic Plan for Getting Out of Debt",
        "url": "https://payhip.com/b/J4fcL",
        "category": "debt",
        "description": "Step-by-step debt elimination plan"
    },
    {
        "id": "ugrLq",
        "name": "FREE Checklist - Could Money Be Waiting for You?",
        "url": "https://payhip.com/b/ugrLq",
        "category": "free",
        "description": "Discover unclaimed money opportunities"
    },
    {
        "id": "9DWGt",
        "name": "UK Budget Calculator - See Where Your Money Really Goes",
        "url": "https://payhip.com/b/9DWGt",
        "category": "budget",
        "description": "Visual budget tracking for UK residents"
    },
    {
        "id": "BvbnP",
        "name": "GET YOUR MONEY BACK",
        "url": "https://payhip.com/b/BvbnP",
        "category": "money",
        "description": "Claim refunds and recover lost money"
    },
    {
        "id": "EDhYI",
        "name": "30$-50$ SURVIVAL FOOD SYSTEM",
        "url": "https://payhip.com/b/EDhYI",
        "category": "survival",
        "description": "Emergency food preparation on a budget"
    },
    {
        "id": "yBiu5",
        "name": "SILENCE THE CALLS",
        "url": "https://payhip.com/b/yBiu5",
        "category": "debt",
        "description": "Stop collection calls and harassment"
    },
    {
        "id": "kMjr3",
        "name": "FIND YOUR HIDDEN MONEY",
        "url": "https://payhip.com/b/kMjr3",
        "category": "money",
        "description": "Locate overlooked assets and money"
    },
    {
        "id": "RyToE",
        "name": "MediSave Method",
        "url": "https://payhip.com/b/RyToE",
        "category": "medical",
        "description": "Reduce medical bills and healthcare costs"
    },
    {
        "id": "WT8JI",
        "name": "Self Relief Guide FREE",
        "url": "https://payhip.com/b/WT8JI",
        "category": "free",
        "description": "Immediate financial stress relief techniques"
    },
    {
        "id": "0YSj7",
        "name": "Financial Crisis Survival Pack – Guides to Get Back on Track",
        "url": "https://payhip.com/b/0YSj7",
        "category": "survival",
        "description": "Complete crisis management toolkit"
    },
    {
        "id": "6RIpj",
        "name": "The 72 Hour Cash Lifeline",
        "url": "https://payhip.com/b/6RIpj",
        "category": "emergency",
        "description": "Emergency cash solutions in 72 hours"
    }
]

# ==================== STRATEGIE WARTOŚCI ====================

VALUE_STRATEGIES = {
    "free": {
        "emojis": ["🎁", "🎯", "🆓", "💝", "✨"],
        "phrases": [
            "100% FREE resource",
            "Complimentary guide",
            "Free gift for you",
            "No-cost solution",
            "Zero investment required"
        ],
        "benefits": [
            "Instant access - no waiting",
            "No strings attached",
            "Download and use today",
            "Immediate help available"
        ]
    },
    "budget": {
        "emojis": ["💰", "📊", "🧮", "💹", "📈"],
        "phrases": [
            "Budget mastery tool",
            "Financial clarity system",
            "Money tracking solution",
            "Spending insight guide"
        ],
        "benefits": [
            "See where every dollar goes",
            "Lifetime financial clarity",
            "Take control of your cash flow",
            "Master your finances"
        ]
    },
    "debt": {
        "emojis": ["🛡️", "⚡", "🔇", "✋", "⚖️"],
        "phrases": [
            "Creditor communication toolkit",
            "Debt resolution system",
            "Collection call defense",
            "Financial peace protocol"
        ],
        "benefits": [
            "Professional word-for-word scripts",
            "Regain peace of mind",
            "Stop harassment legally",
            "Take back control"
        ]
    },
    "stress": {
        "emojis": ["😌", "🧘", "💆", "🌊", "🌈"],
        "phrases": [
            "Financial stress relief system",
            "Money anxiety solution",
            "Mental peace toolkit",
            "Crisis calm down guide"
        ],
        "benefits": [
            "Reduce financial anxiety",
            "Find immediate relief",
            "Restore mental clarity",
            "Manage money stress"
        ]
    },
    "survival": {
        "emojis": ["🛠️", "🥫", "🏕️", "🔋", "🚨"],
        "phrases": [
            "Emergency preparedness system",
            "Crisis survival toolkit",
            "Financial safety net",
            "Urgent situation guide"
        ],
        "benefits": [
            "Be ready for anything",
            "Peace of mind in crisis",
            "Practical step-by-step plan",
            "Protect your family"
        ]
    },
    "medical": {
        "emojis": ["🏥", "💊", "❤️", "🩺", "💉"],
        "phrases": [
            "Medical bill defense system",
            "Healthcare cost solution",
            "Medical financial toolkit",
            "Patient advocacy guide"
        ],
        "benefits": [
            "Reduce medical expenses",
            "Navigate healthcare costs",
            "Save thousands on bills",
            "Expert guidance included"
        ]
    },
    "money": {
        "emojis": ["💵", "🏦", "💳", "🪙", "💸"],
        "phrases": [
            "Money recovery system",
            "Financial discovery tool",
            "Cash flow optimizer",
            "Money finding guide"
        ],
        "benefits": [
            "Find hidden money opportunities",
            "Maximize your income",
            "Unlock financial potential",
            "Discover overlooked resources"
        ]
    },
    "emergency": {
        "emojis": ["🚑", "⏰", "⚡", "🆘", "🔔"],
        "phrases": [
            "Emergency cash solution",
            "Urgent financial lifeline",
            "Quick crisis response",
            "Immediate help system"
        ],
        "benefits": [
            "Get cash fast when needed",
            "Emergency situation ready",
            "Quick access to solutions",
            "Immediate relief available"
        ]
    }
}

# ==================== MOTTA I CTA ====================

MOTTOS = [
    "Your financial breakthrough starts here.",
    "Take control of your money story today.",
    "Peace of mind is the best investment.",
    "Small steps lead to big financial wins.",
    "Your future self will thank you for this.",
    "Financial clarity is within your reach.",
    "Stop worrying, start solving.",
    "Smart tools for smart financial decisions.",
    "Your path to financial confidence starts now.",
    "Transform your relationship with money.",
    "Break free from financial stress.",
    "Build the financial future you deserve.",
    "Master your money, master your life.",
    "Financial freedom begins with a single step.",
    "Unlock your financial potential today."
]

CTAS = [
    "Start your journey →",
    "Get instant access →",
    "Claim your resource →",
    "Begin transforming today →",
    "Download now →",
    "Get your toolkit →",
    "Access the guide →",
    "Secure your copy →",
    "Learn the system →",
    "Get started →",
    "Discover more →",
    "Explore now →",
    "Check it out →",
    "See details →",
    "Learn how →"
]

# ==================== FUNKCJE POMOCNICZE ====================

def get_value_description(product):
    """Zwraca opis wartości zamiast ceny"""
    category = product["category"]
    strategy = VALUE_STRATEGIES.get(category, VALUE_STRATEGIES["budget"])
    
    emoji = random.choice(strategy["emojis"])
    phrase = random.choice(strategy["phrases"])
    benefit = random.choice(strategy["benefits"])
    
    return f"{emoji} {phrase}\n✨ {benefit}"

def should_post_today():
    """Sprawdza czy dzisiaj już był post"""
    try:
        with open("post_history.json", 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = {"last_post_date": None, "posted_products": []}
    
    today = date.today().isoformat()
    
    if history.get("last_post_date") == today:
        print(f"⏭️  Dzisiaj już był post o {history.get('last_post_time', 'nieznanej godzinie')}")
        return False, history
    
    return True, history

def generate_post(product):
    """Generuje post skupiony na wartości"""
    
    motto = random.choice(MOTTOS)
    cta = random.choice(CTAS)
    value_desc = get_value_description(product)
    
    # Hashtagi tematyczne
    hashtags_map = {
        "free": ["#FreeResource", "#FinancialHelp", "#MoneyTips", "#NoCost", "#FreeGuide"],
        "budget": ["#Budgeting", "#MoneyManagement", "#PersonalFinance", "#FinancialClarity", "#CashFlow"],
        "debt": ["#DebtFree", "#DebtHelp", "#FinancialFreedom", "#PeaceOfMind", "#CreditorTips"],
        "stress": ["#MoneyStress", "#FinancialWellness", "#MentalHealth", "#StressRelief"],
        "survival": ["#EmergencyPrep", "#SurvivalTips", "#FinancialSafety", "#CrisisManagement", "#Preparedness"],
        "medical": ["#MedicalBills", "#HealthcareCosts", "#MedicalDebt", "#PatientAdvocate", "#HealthFinance"],
        "money": ["#MoneyTips", "#FinancialDiscovery", "#CashFlow", "#MoneyManagement", "#FindMoney"],
        "emergency": ["#EmergencyCash", "#UrgentHelp", "#QuickMoney", "#FinancialEmergency"]
    }
    
    base_tags = hashtags_map.get(product["category"], ["#PersonalFinance", "#MoneyTips", "#FinancialHelp"])
    additional_tags = random.choice([
        ["#FinancialEducation", "#SmartMoney"],
        ["#MoneyMindset", "#WealthBuilding"],
        ["#FinanceTips", "#EconomicEmpowerment"],
        ["#FinancialWellness", "#MoneyManagement"],
        ["#DebtFreeJourney", "#FinancialGoals"]
    ])
    
    all_tags = list(set(base_tags + additional_tags))
    random.shuffle(all_tags)
    hashtags = " ".join(all_tags[:6])  # Max 6 hashtagów
    
    # Buduj post
    post_lines = []
    post_lines.append(f"{motto}")
    post_lines.append("")  # Pusta linia
    post_lines.append(f"📘 {product['name']}")
    post_lines.append(f"{value_desc}")
    post_lines.append("")  # Pusta linia
    post_lines.append(f"{cta}")
    post_lines.append(f"{product['url']}")
    post_lines.append("")  # Pusta linia
    post_lines.append(f"{hashtags}")
    
    post = "\n".join(post_lines)
    
    # Upewnij się że nie przekracza 500 znaków
    if len(post) > 500:
        # Skróć nazwę jeśli trzeba
        name = product['name']
        if len(name) > 80:
            product['name'] = name[:75] + "..."
            return generate_post(product)
        else:
            # Skróć hashtagi
            post = "\n".join(post_lines[:-1]) + "\n" + " ".join(all_tags[:4])
            if len(post) > 500:
                post = post[:497] + "..."
    
    return post

# ==================== GŁÓWNA LOGIKA ====================

def main():
    """Główna funkcja bota"""
    
    # 1. Sprawdź czy dzisiaj postować
    should_post, history = should_post_today()
    if not should_post:
        print("💤 Kończę pracę - dzisiaj już postowano")
        return
    
    print("✅ Rozpoczynam dzisiejszy post")
    
    # 2. Wybierz produkt (rotacja)
    available_products = [p for p in PRODUCTS 
                         if p["id"] not in history.get("posted_products", [])]
    
    if not available_products:
        print("🔄 Wszystkie produkty były reklamowane, resetuję rotację")
        history["posted_products"] = []
        available_products = PRODUCTS
    
    selected_product = random.choice(available_products)
    
    print(f"🛒 Wybrany produkt: {selected_product['name'][:50]}...")
    print(f"📊 Kategoria: {selected_product['category'].upper()}")
    
    # 3. Wygeneruj post skupiony na wartości
    print("\n📝 Tworzę post (skupiony na wartości)...")
    post_content = generate_post(selected_product)
    
    print(f"\n✍️  POST ({len(post_content)} znaków):")
    print("-" * 50)
    print(post_content)
    print("-" * 50)
    
    # 4. Połącz z Mastodon
    ACCESS_TOKEN = os.environ.get('MASTODON_ACCESS_TOKEN')
    BASE_URL = os.environ.get('MASTODON_BASE_URL', 'https://mastodon.social')
    
    if not ACCESS_TOKEN:
        print("\n❌ BRAK MASTODON_ACCESS_TOKEN!")
        print("Dodaj token w GitHub Secrets:")
        print("1. Settings → Secrets and variables → Actions")
        print("2. Kliknij 'New repository secret'")
        print("3. Nazwa: MASTODON_ACCESS_TOKEN")
        print("4. Wartość: Twój token z Mastodona")
        sys.exit(1)
    
    print(f"\n🔗 Łączę z Mastodon: {BASE_URL}")
    
    try:
        mastodon = Mastodon(
            access_token=ACCESS_TOKEN,
            api_base_url=BASE_URL,
            request_timeout=30
        )
        account = mastodon.account_verify_credentials()
        print(f"✅ Połączono jako: @{account['username']}")
        print(f"   👤 Followers: {account['followers_count']}")
        
    except Exception as e:
        print(f"❌ Błąd połączenia z Mastodon: {type(e).__name__}: {e}")
        print("\n💡 Sprawdź czy:")
        print("   • Token jest poprawny")
        print("   • URL instancji jest prawidłowy")
        print("   • Token ma uprawnienia 'write:statuses'")
        sys.exit(1)
    
    # 5. Opublikuj post
    print("\n🚀 Publikuję na Twojej tablicy Mastodona...")
    
    try:
        response = mastodon.status_post(
            status=post_content,
            visibility='public',
            language='en'
        )
        
        if response and 'url' in response:
            print(f"✅ SUKCES! OPUBLIKOWANO!")
            print(f"🔗 Link do posta: {response['url']}")
            print(f"📅 Data publikacji: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 6. Zaktualizuj historię
            history["last_post_date"] = date.today().isoformat()
            history["last_post_time"] = datetime.now().strftime('%H:%M')
            history["posted_products"].append(selected_product["id"])
            
            try:
                with open("post_history.json", "w") as f:
                    json.dump(history, f, indent=2)
                print(f"📊 Historia zaktualizowana: {len(history['posted_products'])}/{len(PRODUCTS)} produktów")
            except Exception as e:
                print(f"⚠️  Błąd zapisu historii: {e}")
            
        else:
            print("❌ Nie udało się opublikować (brak odpowiedzi)")
            
    except Exception as e:
        print(f"❌ Błąd publikacji na Mastodonie: {type(e).__name__}: {e}")
    
    # 7. Podsumowanie
    print("\n" + "=" * 60)
    print("🏁 BOT ZAKOŃCZONY DZIAŁANIE")
    print("=" * 60)
    print(f"📘 Produkt: {selected_product['name'][:60]}...")
    print(f"🎯 Strategia: {selected_product['category']} (value-focused)")
    print(f"📅 Data: {date.today().isoformat()}")
    print(f"⏰ Godzina: {datetime.now().strftime('%H:%M')}")
    print(f"🔄 Następny post: Jutro o podobnej porze")
    print("=" * 60)

if __name__ == "__main__":
    main()
