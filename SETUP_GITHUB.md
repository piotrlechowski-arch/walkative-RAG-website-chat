# Instrukcja utworzenia repozytorium GitHub

## Krok 1: Utwórz nowe repozytorium na GitHub

1. Przejdź do https://github.com/new
2. Wypełnij formularz:
   - **Repository name:** `walkative-rag`
   - **Description:** "RAG system for Walkative with FastAPI backend and frontend"
   - **Visibility:** Wybierz Public lub Private
   - **NIE zaznaczaj** "Initialize this repository with a README" (już mamy README)
3. Kliknij "Create repository"

## Krok 2: Połącz lokalne repozytorium z GitHub

Po utworzeniu repozytorium GitHub pokaże Ci instrukcje. Użyj tych komend:

```bash
cd /Users/Lechu1/walkative-rag

# Dodaj remote (zamień YOUR_USERNAME na swoją nazwę użytkownika GitHub)
git remote add origin https://github.com/YOUR_USERNAME/walkative-rag.git

# Zmień nazwę brancha na main (jeśli jeszcze nie)
git branch -M main

# Wyślij kod na GitHub
git push -u origin main
```

## Krok 3: Weryfikacja

Sprawdź czy wszystko działa:

```bash
git remote -v
git status
```

## Struktura projektu

Po dodaniu frontendu, struktura będzie wyglądać tak:

```
walkative-rag/
├── backend/          # Backend FastAPI
├── frontend/         # Frontend (do dodania)
├── .github/          # GitHub Actions workflows
├── README.md
└── ...
```

## Dodawanie frontendu

Gdy będziesz gotowy dodać frontend:

1. Skopiuj kod frontendu do folderu `frontend/`
2. Dodaj pliki:
   ```bash
   git add frontend/
   git commit -m "Add frontend"
   git push
   ```

## Współpraca

Aby inni mogli współpracować:

1. Dodaj ich jako collaborators w ustawieniach repozytorium GitHub
2. Albo użyj pull requests dla code review

