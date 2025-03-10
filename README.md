# FoodFinder

FoodFinder je webová aplikace pro sdílení a vyhledávání receptů, postavená na frameworku Flask a hostovaná na platformě Vercel. Aplikace umožňuje uživatelům přidávat, spravovat a vyhledávat recepty, spravovat svůj uživatelský profil a interagovat s ostatními uživateli prostřednictvím oblíbených receptů.

## Funkcionalita

### Autentizace a správa účtu

- Registrace uživatele s validací hesla a generováním profilového obrázku.
- Přihlášení pomocí e-mailu/hesla nebo Google OAuth.
- Možnost úpravy uživatelského profilu (změna jména, e-mailu, hesla).
- Možnost smazání účtu.

### Práce s recepty

- Přidávání nových receptů s obrázky, ingrediencemi, postupem a kategorií.
- Ukládání obrázků receptů na Vercel Blob Storage.
- Vyhledávání receptů podle názvu, ingrediencí nebo kategorie (pomocí fuzzy matching).
- Filtrování doporučených receptů na základě času dne.
- Zobrazení detailu receptu s podrobným popisem a souvisejícími recepty.
- Označování receptů jako oblíbené.

### Hlavní stránky

- **Homepage:** zobrazuje doporučené a nejnovější recepty.
- **Vyhledávání:** umožňuje vyhledávat recepty podle názvu a ingrediencí.
- **Detail receptu:** obsahuje informace o receptu, obrázky a související recepty.
- **Profil uživatele:** zobrazuje nahrané a oblíbené recepty uživatele.

## Použité technologie

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Frontend:** Bootstrap 5, Jinja2
- **Databáze:** SQLite (možnost rozšíření na PostgreSQL)
- **Hostování:** Vercel (serverless deployment)
- **Úložiště obrázků:** Vercel Blob Storage

## Instalace a spuštění

1. Naklonujte repozitář:
   ```bash
   git clone <repo_url>
   cd FoodFinder
   ```
2. Vytvořte a aktivujte virtuální prostředí:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
3. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```
4. Spusťte aplikaci lokálně:

   ```bash
   flask run
   ```

   Aplikace poběží na `http://localhost:5000`.

5. Nasazení na Vercel:
   ```bash
   npm i -g vercel
   vercel
   ```
   Aplikace bude dostupná na hostovaném URL od Vercel.

## Autoři

- Pavel Podrazký
- Ondřej Štecher
- Marek Šimon
- Jan Král
