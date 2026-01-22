#!/usr/bin/env python3
"""
🤖 MASTODON VALUE-FOCUSED BOT (NO IMAGES)
- Podkreśla wartość, nie ceny
- Automatycznie pobiera dane z Payhip
- 1 post dziennie na Twoim koncie
- Bez obrazków (wersja czysto tekstowa)
"""

from mastodon import Mastodon
import os
import json
import random
from datetime import datetime, date
import sys
import requests
import time
from bs4 import BeautifulSoup

print("=" * 60)
print("🤖 MASTODON VALUE BOT (TEXT ONLY)")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# ==================== KONFIGURACJA ====================

CACHE_DIR = "product_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# ==================== LISTA PRODUKTÓW ====================

PRODUCT_URLS = [
    "https://payhip.com/b/QaDjw",      # How to Talk to Creditors
    "https://payhip.com/b/fyxsZ",      # Financial First Aid
    "https://payhip.com/b/J4fcL",      # Debt Recovery
    "https://payhip.com/b/ugrLq",      # FREE Checklist
    "https://payhip.com/b/9DWGt",      # UK Budget Calculator
    "https://payhip.com/b/BvbnP",      # GET YOUR MONEY BACK
    "https://payhip.com/b/EDhYI",      # 30$-50$ SURVIVAL FOOD SYSTEM
    "https://payhip.com/b/yBiu5",      # SILENCE THE CALLS
    "https://payhip.com/b/kMjr3",      # FIND YOUR HIDDEN MONEY
    "https://payhip.com/b/RyToE",      # MediSave Method
    "https://payhip.com/b/WT8JI",      # Self Relief Guide FREE
    "https://payhip.com/b/0YSj7",      # Financial Crisis Survival Pack
    "https://payhip.com/b/6RIpj",      # the 72 hour cash lifeline
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
            "Zero investment required",
            "Absolutely FREE download"
        ],
        "benefits": [
            "Instant access - no waiting",
            "No strings attached",
            "Download and use today",
            "Immediate help available",
            "Get started right away"
        ]
    },
    "budget": {
        "emojis": ["💰", "📊", "🧮", "💹", "📈"],
        "phrases": [
            "Budget mastery tool",
            "Financial clarity system",
            "Money tracking solution",
            "Spending insight guide",
            "Cash flow optimizer",
            "Financial roadmap"
        ],
        "benefits": [
            "See where every dollar goes",
            "Lifetime financial clarity",
            "Take control of your cash flow",
            "Master your finances",
            "Achieve money goals faster"
        ]
    },
    "debt": {
        "emojis": ["🛡️", "⚡", "🔇", "✋", "⚖️"],
        "phrases": [
            "Creditor communication toolkit",
            "Debt resolution system",
            "Collection call defense",
            "Financial peace protocol",
            "Debt negotiation guide",
            "Creditor management system"
        ],
        "benefits": [
            "Professional word-for-word scripts",
            "Regain peace of mind",
            "Stop harassment legally",
            "Take back control",
            "Reduce stress immediately"
        ]
    },
    "survival": {
        "emojis": ["🛠️", "🥫", "🏕️", "🔋", "🚨"],
        "phrases": [
            "Emergency preparedness system",
            "Crisis survival toolkit",
            "Financial safety net",
            "Urgent situation guide",
            "Emergency response plan",
            "Crisis management system"
        ],
        "benefits": [
            "Be ready for anything",
            "Peace of mind in crisis",
            "Practical step-by-step plan",
            "Lifetime preparedness",
            "Protect your family"
        ]
    },
    "premium": {
        "emojis": ["🏆", "💎", "👑", "⭐", "🎖️"],
        "phrases": [
            "Comprehensive premium system",
            "Ultimate solution toolkit",
            "Complete mastery guide",
            "Professional-grade resource",
            "All-in-one solution pack",
            "Premium financial system"
        ],
        "benefits": [
            "All-in-one solution",
            "Lifetime access & updates",
            "Professional results",
            "Transformative system",
            "Complete coverage"
        ]
    },
    "medical": {
        "emojis": ["🏥", "💊", "❤️", "🩺", "💉"],
        "phrases": [
            "Medical bill defense system",
            "Healthcare cost solution",
            "Medical financial toolkit",
            "Patient advocacy guide",
            "Medical expense reducer",
            "Healthcare savings plan"
        ],
        "benefits": [
            "Reduce medical expenses",
            "Navigate healthcare costs",
            "Save thousands on bills",
            "Expert guidance included",
            "Maximize insurance benefits"
        ]
    },
    "money": {
        "emojis": ["💵", "🏦", "💳", "🪙", "💸"],
        "phrases": [
            "Money recovery system",
            "Financial discovery tool",
            "Cash flow optimizer",
            "Money finding guide",
            "Financial detective kit"
        ],
        "benefits": [
            "Find hidden money opportunities",
            "Maximize your income",
            "Unlock financial potential",
            "Discover overlooked resources"
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

def fetch_product_data(url, force_refresh=False):
    """Pobiera dane produktu z Payhip"""
    cache_key = url.split('/')[-1]
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    # Sprawdź cache (ważny 24h)
    if not force_refresh and os.path.exists(cache_file):
        cache_age = time.time() - os.path.getmtime(cache_file)
        if cache_age < 86400:  # 24 godziny
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                print(f"📦 Używam cache dla {cache_key}")
                return cached
            except:
                pass  # Jeśli błąd cache, pobierz na nowo
    
    print(f"🌐 Pobieram dane z: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tytuł
        title_elem = soup.find('h1', class_='product-title') or soup.find('h1') or soup.find('title')
        title = title_elem.get_text(strip=True) if title_elem else "Financial Resource"
        
        # Określ kategorię na podstawie tytułu
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['free', 'checklist', 'guide']):
            category = "free"
        elif any(word in title_lower for word in ['budget', 'calculator']):
            category = "budget"
        elif any(word in title_lower for word in ['debt', 'creditor', 'collection', 'silence', 'recovery']):
            category = "debt"
        elif any(word in title_lower for word in ['survival', 'food', 'emergency', 'crisis', 'lifeline', 'pack']):
            category = "survival"
        elif any(word in title_lower for word in ['medical', 'medisave']):
            category = "medical"
        elif any(word in title_lower for word in ['money', 'cash', 'financial', 'get your money']):
            category = "money"
        elif any(word in title_lower for word in ['system', 'premium', 'complete']):
            category = "premium"
        else:
            category = "budget"
        
        product_data = {
            "name": title,
            "url": url,
            "category": category,
            "fetched_at": datetime.now().isoformat(),
            "product_id": cache_key
        }
        
        # Zapisz do cache
        with open(cache_file, 'w') as f:
            json.dump(product_data, f, indent=2)
        
        print(f"✅ Pobrano: {title[:50]}...")
        return product_data
        
    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout przy pobieraniu {url}")
    except requests.exceptions.RequestException as e:
        print(f"🌐 Błąd sieci: {e}")
    except Exception as e:
        print(f"⚠️  Inny błąd: {type(e).__name__}: {e}")
    
    # Fallback na cache nawet jeśli stary
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Ostateczny fallback
    return {
        "name": "Financial Resource",
        "url": url,
        "category": "budget",
        "fetched_at": datetime.now().isoformat(),
        "product_id": cache_key
    }

def get_value_description(product_data):
    """Zwraca opis wartości zamiast ceny"""
    category = product_data["category"]
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

def generate_post(product_data):
    """Generuje post skupiony na wartości"""
    
    motto = random.choice(MOTTOS)
    cta = random.choice(CTAS)
    value_desc = get_value_description(product_data)
    
    # Hashtagi tematyczne
    hashtags_map = {
        "free": ["#FreeResource", "#FinancialHelp", "#MoneyTips", "#NoCost", "#FreeGuide"],
        "budget": ["#Budgeting", "#MoneyManagement", "#PersonalFinance", "#FinancialClarity", "#CashFlow"],
        "debt": ["#DebtFree", "#DebtHelp", "#FinancialFreedom", "#PeaceOfMind", "#CreditorTips"],
        "survival": ["#EmergencyPrep", "#SurvivalTips", "#FinancialSafety", "#CrisisManagement", "#Preparedness"],
        "medical": ["#MedicalBills", "#HealthcareCosts", "#MedicalDebt", "#PatientAdvocate", "#HealthFinance"],
        "money": ["#MoneyTips", "#FinancialDiscovery", "#CashFlow", "#MoneyManagement", "#FindMoney"],
        "premium": ["#FinancialTools", "#MoneySystems", "#PremiumResources", "#CompleteSolutions", "#AllInOne"]
    }
    
    base_tags = hashtags_map.get(product_data["category"], ["#PersonalFinance", "#MoneyTips", "#FinancialHelp"])
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
    post_lines.append(f"📘 {product_data['name']}")
    post_lines.append(f"{value_desc}")
    post_lines.append("")  # Pusta linia
    post_lines.append(f"{cta}")
    post_lines.append(f"{product_data['url']}")
    post_lines.append("")  # Pusta linia
    post_lines.append(f"{hashtags}")
    
    post = "\n".join(post_lines)
    
    # Upewnij się że nie przekracza 500 znaków
    if len(post) > 500:
        # Skróć nazwę jeśli trzeba
        name = product_data['name']
        if len(name) > 80:
            product_data['name'] = name[:75] + "..."
            return generate_post(product_data)
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
    available_ids = [url.split('/')[-1] for url in PRODUCT_URLS 
                     if url.split('/')[-1] not in history.get("posted_products", [])]
    
    if not available_ids:
        print("🔄 Wszystkie produkty były reklamowane, resetuję rotację")
        history["posted_products"] = []
        available_ids = [url.split('/')[-1] for url in PRODUCT_URLS]
    
    selected_id = random.choice(available_ids)
    selected_url = f"https://payhip.com/b/{selected_id}"
    
    print(f"🛒 Wybrany produkt ID: {selected_id}")
    print(f"🔗 URL: {selected_url}")
    
    # 3. Pobierz dane produktu
    print("\n🔍 Pobieram informacje o produkcie...")
    product_data = fetch_product_data(selected_url)
    
    print(f"📊 Kategoria: {product_data['category'].upper()}")
    print(f"🏷️  Nazwa: {product_data['name']}")
    
    # 4. Wygeneruj post skupiony na wartości
    print("\n📝 Tworzę post (skupiony na wartości)...")
    post_content = generate_post(product_data)
    
    print(f"\n✍️  POST ({len(post_content)} znaków):")
    print("-" * 50)
    print(post_content)
    print("-" * 50)
    
    # 5. Połącz z Mastodon
    ACCESS_TOKEN = os.environ.get('MASTODON_ACCESS_TOKEN')
    BASE_URL = os.environ.get('MASTODON_BASE_URL', 'https://mastodon.social')
    
    if not ACCESS_TOKEN:
        print("\n❌ BRAK MASTODON_ACCESS_TOKEN!")
        print("Dodaj token w GitHub Secrets:")
        print("1. Wejdź do Settings → Secrets and variables → Actions")
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
    
    # 6. Opublikuj post
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
            
            # 7. Zaktualizuj historię
            history["last_post_date"] = date.today().isoformat()
            history["last_post_time"] = datetime.now().strftime('%H:%M')
            history["posted_products"].append(selected_id)
            
            try:
                with open("post_history.json", "w") as f:
                    json.dump(history, f, indent=2)
                print(f"📊 Historia zaktualizowana: {len(history['posted_products'])}/{len(PRODUCT_URLS)} produktów")
            except Exception as e:
                print(f"⚠️  Błąd zapisu historii: {e}")
            
        else:
            print("❌ Nie udało się opublikować (brak odpowiedzi)")
            
    except Exception as e:
        print(f"❌ Błąd publikacji na Mastodonie: {type(e).__name__}: {e}")
    
    # 8. Podsumowanie
    print("\n" + "=" * 60)
    print("🏁 BOT ZAKOŃCZONY DZIAŁANIE")
    print("=" * 60)
    print(f"📘 Produkt: {product_data['name'][:60]}...")
    print(f"🎯 Strategia: {product_data['category']} (value-focused)")
    print(f"📅 Data: {date.today().isoformat()}")
    print(f"⏰ Godzina: {datetime.now().strftime('%H:%M')}")
    print(f"🔄 Następny post: Jutro o podobnej porze")
    print("=" * 60)

if __name__ == "__main__":
    main()
