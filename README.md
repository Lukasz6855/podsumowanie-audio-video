# 🎬 Aplikacja do Transkrypcji i Podsumowania Audio/Wideo

Aplikacja webowa w Streamlit do transkrypcji i podsumowywania plików audio i wideo przy użyciu OpenAI Whisper, GPT-4o i TTS-1.

## 📋 Funkcjonalności

- ✅ Przesyłanie plików audio (MP3, WAV) i wideo (MP4, AVI, MOV)
- ✅ Pobieranie filmów z YouTube
- ✅ Odtwarzacz wideo/audio z podglądem
- ✅ Ekstrakcja audio z plików wideo do formatu MP3
- ✅ Transkrypcja audio przy użyciu OpenAI Whisper-1
- ✅ Generowanie podsumowania przy użyciu GPT-4o
- ✅ **NOWOŚĆ:** Generowanie podsumowania w formie audio (text-to-speech) z użyciem TTS-1
- ✅ **Dwie ścieżki generowania:**
  - **Opcja szybka:** Automatyczne przejście przez wszystkie kroki (ekstrakcja → transkrypcja → podsumowanie)
  - **Opcja zaawansowana:** Krok po kroku z pełną kontrolą nad procesem
- ✅ Wybór długości (krótkie/średnie/długie) i stylu (tekstowe/w punktach) podsumowania
- ✅ Oszacowanie kosztów użycia API OpenAI (Whisper-1, GPT-4o, TTS-1)
- ✅ Eksport wyników do formatów TXT, PDF, DOCX
- ✅ **NOWOŚĆ:** Pobieranie podsumowania audio jako plik MP3
- ✅ Wskaźniki postępu dla długotrwałych operacji
- ✅ Obsługa klucza API z pliku .env lub wprowadzenie ręczne
- ✅ Pełna obsługa błędów i komunikaty w języku polskim

## 🛠️ Wymagania

- Python 3.8 lub nowszy
- Klucz API OpenAI
- Pakiety wymienione w `requirements.txt`

## 📦 Instalacja

1. **Sklonuj lub pobierz repozytorium**

2. **Utwórz wirtualne środowisko (opcjonalne, ale zalecane)**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Zainstaluj zależności**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Skonfiguruj klucz API OpenAI**
   
   Opcja A: Utwórz plik `.env` na podstawie `.env.example`:
   ```powershell
   Copy-Item .env.example .env
   ```
   Następnie edytuj plik `.env` i wpisz swój klucz API:
   ```
   OPENAI_API_KEY=twoj-prawdziwy-klucz-api
   ```
   
   Opcja B: Wprowadź klucz API bezpośrednio w interfejsie aplikacji po uruchomieniu

## 🚀 Uruchomienie

```powershell
streamlit run app.py
```

Aplikacja otworzy się automatycznie w przeglądarce pod adresem `http://localhost:8501`

## 📖 Instrukcja użytkowania

### Podstawowy przepływ pracy

1. **Wprowadź klucz API OpenAI** (w pasku bocznym, jeśli nie jest w pliku .env)
2. **Prześlij plik** audio/wideo lub **wprowadź link do YouTube** (w pasku bocznym)
3. **Obejrzyj podgląd** wideo lub audio w sekcji głównej
4. **Wybierz tryb generowania:**

#### Opcja A: Szybka (zalecana)
5a. W sekcji "Podsumowanie" wybierz:
   - **Długość:** Krótkie / Średnie / Długie
   - **Styl:** Tekstowe / W punktach
6a. Kliknij jeden z przycisków:
   - **"Wygeneruj podsumowanie tekstowe"** - automatycznie wykonuje wszystkie kroki i generuje podsumowanie tekstowe
   - **"Wygeneruj podsumowanie audio"** - dodatkowo zamienia podsumowanie na mowę (text-to-speech)
7a. Poczekaj na zakończenie procesu
8a. Pobierz wyniki w wybranym formacie

#### Opcja B: Zaawansowana (krok po kroku)
5b. W sekcji "Opcja zaawansowana (krok po kroku)":
   - **Dla plików wideo:** Wyodrębnij audio do MP3
   - **Rozpocznij transkrypcję** i poczekaj na zakończenie
   - **Wygeneruj podsumowanie** z wybranymi parametrami
6b. Pobierz wyniki w wybranym formacie

### Pobieranie wyników

Po wygenerowaniu podsumowania możesz pobrać:
- **TXT** - plik tekstowy z transkrypcją i podsumowaniem
- **PDF** - sformatowany dokument PDF
- **DOCX** - dokument Word
- **MP3** - *(tylko dla opcji "Wygeneruj podsumowanie audio")* plik audio z podsumowaniem w formie mowy

## 💰 Koszty

Aplikacja wyświetla rzeczywiste koszty po wygenerowaniu podsumowania w pasku bocznym:

- **Whisper-1**: $0.006 za minutę audio
- **GPT-4o**: $0.0025 za 1000 tokenów wejściowych, $0.01 za 1000 tokenów wyjściowych
- **TTS-1**: $0.015 za 1000 znaków *(tylko dla opcji audio)*

Koszty są obliczane na podstawie:
- Rzeczywistej długości audio (dla Whisper-1)
- Rzeczywistej liczby słów w transkrypcji i podsumowaniu (dla GPT-4o)
- Liczby znaków w podsumowaniu (dla TTS-1)

## 📁 Struktura projektu

```
podsumowanie_audio_video_v5/
│
├── app.py                  # Główny plik aplikacji Streamlit
├── utils.py                # Funkcje pomocnicze (w tym TTS)
├── requirements.txt        # Zależności projektu
├── .env.example           # Szablon pliku konfiguracyjnego
├── .env                   # Plik konfiguracyjny (tworzony przez użytkownika)
├── prompt.txt             # Historia wymagań projektu
└── README.md              # Dokumentacja projektu
```

## 🔧 Technologie

- **Streamlit** - framework do budowy interfejsu użytkownika
- **OpenAI API** - Whisper-1 do transkrypcji, GPT-4o do podsumowania, TTS-1 do generowania mowy
- **MoviePy** - ekstrakcja audio z wideo
- **yt-dlp** - pobieranie filmów z YouTube
- **FPDF** - generowanie plików PDF
- **python-docx** - generowanie plików DOCX
- **python-dotenv** - zarządzanie zmiennymi środowiskowymi

## ⚠️ Uwagi

- Pliki wideo są konwertowane do MP3 przed transkrypcją
- Transkrypcja i podsumowanie mogą potrwać kilka minut w zależności od długości pliku
- Generowanie audio (TTS) dodaje dodatkowy czas przetwarzania
- Polskie znaki w PDF mogą być częściowo zastąpione najbliższymi odpowiednikami ASCII
- Koszty są obliczane na podstawie rzeczywistych danych i są wyświetlane po zakończeniu operacji
- Dla funkcji TTS użyto głosu "fable" - jednego z 6 dostępnych głosów OpenAI

## 🎙️ Dostępne głosy TTS

Aplikacja domyślnie używa głosu **"fable"**. OpenAI TTS-1 oferuje następujące głosy:
- alloy
- echo
- fable *(domyślny)*
- onyx
- nova
- shimmer

## 📝 Licencja

Projekt edukacyjny - swobodne użytkowanie.

## 👨‍💻 Autor

Aplikacja stworzona w ramach kursu "Od Zera do AI" - Moduł 8
