# Szybki start - Instrukcje uruchomienia

## Krok 1: Instalacja zależności
```powershell
pip install -r requirements.txt
```

## Krok 2: Konfiguracja klucza API

### Opcja A: Użyj pliku .env (zalecane)
1. Skopiuj plik `.env.example` do `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Otwórz plik `.env` w edytorze i wpisz swój klucz API:
   ```
   OPENAI_API_KEY=sk-twoj-prawdziwy-klucz-openai
   ```

### Opcja B: Wprowadź klucz w aplikacji
Jeśli nie utworzysz pliku `.env`, aplikacja poprosi Cię o wprowadzenie klucza API w interfejsie.

## Krok 3: Uruchomienie aplikacji
```powershell
streamlit run app.py
```

Aplikacja otworzy się automatycznie w przeglądarce pod adresem: http://localhost:8501

## Testowanie aplikacji

1. Prześlij plik audio (MP3, WAV) lub wideo (MP4, AVI, MOV)
2. Jeśli przesłałeś wideo, kliknij "Wyodrębnij audio z wideo"
3. Kliknij "Rozpocznij transkrypcję"
4. Po zakończeniu transkrypcji, kliknij "Wygeneruj podsumowanie"
5. Pobierz wyniki w wybranym formacie (TXT, PDF, DOCX)

## Rozwiązywanie problemów

### Błąd importu moviepy
```powershell
pip install moviepy --upgrade
```

### Błąd z codecami audio
Upewnij się, że masz zainstalowany ffmpeg:
```powershell
# Windows (przy użyciu Chocolatey)
choco install ffmpeg

# Lub pobierz ręcznie ze strony: https://ffmpeg.org/download.html
```

### Błędy z polskimi znakami w PDF
To normalne zachowanie - FPDF ma ograniczone wsparcie dla Unicode. 
Użyj formatu DOCX lub TXT dla pełnego wsparcia polskich znaków.

## Wskazówki

- Transkrypcja może potrwać kilka minut dla dłuższych plików
- Sprawdź szacowane koszty przed rozpoczęciem operacji
- Zachowaj klucz API w bezpiecznym miejscu
- Nie udostępniaj pliku `.env` publicznie
