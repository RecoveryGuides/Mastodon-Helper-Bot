# 🤖 Mastodon Bot - Automatyczne posty o produktach

Bot publikujący **1 post dziennie** na Twoim koncie Mastodon, reklamujący produkty z Payhip.

## 🚀 Szybka instalacja

### 1. Przygotuj token Mastodon
1. Zaloguj się na swoje konto Mastodon
2. Przejdź do **Preferences → Development**
3. Kliknij **"New Application"**
4. Wpisz:
   - **Application name:** `GitHub Bot`
   - **Scopes:** zaznacz `read:accounts` i `write:statuses`
5. Kliknij **"Submit"**
6. Skopiuj **"Your access token"**

### 2. Skonfiguruj repozytorium GitHub
1. **Stwórz nowe repozytorium** na GitHub
2. **Wgraj wszystkie pliki** z tego folderu:
   - `bot.py` (główny kod)
   - `.github/workflows/mastodon.yml` (automatyzacja)
   - `requirements.txt` (zależności)
   - `README.md` (ta instrukcja)

### 3. Dodaj sekrety do GitHub
1. W repozytorium → **Settings** (Ustawienia)
2. **Secrets and variables → Actions**
3. Kliknij **"New repository secret"**
4. Dodaj **2 sekrety**:

**Secret 1:**
- **Name:** `MASTODON_ACCESS_TOKEN`
- **Value:** *wklej skopiowany token z Mastodona*

**Secret 2:**
- **Name:** `MASTODON_BASE_URL`
- **Value:** `https://mastodon.social` *(lub adres Twojej instancji)*

### 4. Działanie bota
✅ **Gotowe!** Bot będzie automatycznie:
- Pobierać dane z Twoich produktów Payhip
- Publikować **1 post dziennie** o 9:00 czasu polskiego
- Rotować wszystkie produkty
- Podkreślać **wartość**, nie ceny
- Działać **24/7** dzięki GitHub Actions

## ⚙️ Dostosowanie

### Zmiana godziny postowania
Edytuj plik `.github/workflows/mastodon.yml`:
```yaml
schedule:
  - cron: '0 8 * * *'  # 8:00 UTC = 9:00 polskiego (zimowy)
