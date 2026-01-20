# 🎬 Aplikacja do Transkrypcji i Podsumowania Audio/Wideo

Aplikacja webowa w Streamlit do transkrypcji i podsumowywania plików audio i wideo przy użyciu OpenAI Whisper, GPT-4o i TTS-1.

## 📋 Funkcjonalności

### Podstawowe funkcje
- ✅ Przesyłanie plików audio (MP3, WAV) i wideo (MP4, AVI, MOV)
- ✅ Pobieranie filmów z YouTube
- ✅ Odtwarzacz wideo/audio z podglądem
- ✅ Ekstrakcja audio z plików wideo do formatu MP3
- ✅ Transkrypcja audio przy użyciu OpenAI Whisper-1
- ✅ Generowanie podsumowania przy użyciu GPT-4o
- ✅ Generowanie podsumowania w formie audio (text-to-speech) z użyciem TTS-1
- ✅ Wybór długości (krótkie/średnie/długie) i stylu (tekstowe/w punktach) podsumowania
- ✅ Oszacowanie kosztów użycia API OpenAI (Whisper-1, GPT-4o, TTS-1)
- ✅ Eksport wyników do formatów TXT, PDF, DOCX, MP3
- ✅ Pełna obsługa błędów i komunikaty w języku polskim

### Dwie ścieżki generowania
- **📋 Generowanie podsumowania (Opcja szybka):** Automatyczne przejście przez wszystkie kroki
- **🔧 Audio i Transkrypcja (Opcja zaawansowana):** Krok po kroku z pełną kontrolą

### Zaawansowane funkcje edycji
- ✅ **Edycja transkrypcji** - możliwość poprawienia tekstu przed generowaniem podsumowania
- ✅ **Edycja podsumowania** - możliwość modyfikacji wygenerowanego podsumowania
- ✅ **Anulowanie zmian** - powrót do poprzedniej wersji
- ✅ **Automatyczna regeneracja audio** - po edycji podsumowania w trybie audio
- ✅ **Blokady podczas edycji** - zabezpieczenie przed przypadkowym wyjściem z trybu edycji
- ✅ **Reset aplikacji** - przycisk "Resetuj wszystko i zacznij od nowa"

### Intuicyjny interfejs użytkownika
- ✅ **Czytelny podział na sekcje** - wyraźne nagłówki z emoji i liniami poziomymi
- ✅ **Wskaźniki postępu** - informacja o trwających operacjach
- ✅ **Walidacja stanów** - niemożność wykonania operacji w niewłaściwej kolejności

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

#### Opcja A: 📋 Generowanie podsumowania (Szybka - zalecana)
5a. W sekcji "📋 Generowanie podsumowania" wybierz:
   - **Długość:** Krótkie / Średnie / Długie
   - **Styl:** Tekstowe / W punktach
6a. Kliknij jeden z przycisków:
   - **📝 Wygeneruj podsumowanie tekstowe** - automatycznie wykonuje wszystkie kroki
   - **🔊 Wygeneruj podsumowanie audio** - dodatkowo generuje mowę (TTS)
7a. **Edytuj podsumowanie** (opcjonalnie):
   - Kliknij **✏️ Edycja** aby włączyć tryb edycji
   - Wprowadź zmiany w polu tekstowym
   - Kliknij **💾 Zapisz zmiany** (audio zostanie automatycznie zregenerowane)
   - Lub kliknij **❌ Anuluj edycję** aby odrzucić zmiany
8a. Pobierz wyniki w wybranym formacie (TXT, PDF, DOCX, MP3)
9a. **🔄 Resetuj wszystko i zacznij od nowa** - przycisk do wyczyszczenia wyników podsumowania i transkrypcji, powrót do stanu po wczytaniu audio/video

#### Opcja B: 🔧 Audio i Transkrypcja (Zaawansowana - krok po kroku)
5b. W sekcji "🔧 Audio i Transkrypcja":
   - **Dla plików wideo:** Wyodrębnij audio do MP3 (sekcja "🎵 Ekstrakcja Audio")
   - **📝 Rozpocznij transkrypcję** i poczekaj na zakończenie
   - **Edytuj transkrypcję** (opcjonalnie):
     - Kliknij **✏️ Edycja** aby włączyć tryb edycji
     - Popraw tekst transkrypcji
     - Kliknij **💾 Zapisz zmiany** (obowiązkowe przed generowaniem podsumowania)
     - Lub kliknij **❌ Anuluj edycję** aby odrzucić zmiany
   - **Wygeneruj podsumowanie** z wybranymi parametrami (tekstowe lub audio)
6b. Pobierz wyniki w wybranym formacie

### ⬇️ Pobieranie wyników

Po wygenerowaniu podsumowania w sekcji "⬇️ Pobierz wyniki" możesz pobrać:
- **📄 TXT** - plik tekstowy z transkrypcją i podsumowaniem
- **📕 PDF** - sformatowany dokument PDF (ograniczone wsparcie polskich znaków)
- **📘 DOCX** - dokument Word (pełne wsparcie polskich znaków)
- **🔊 MP3** - *(tylko dla opcji audio)* plik audio z podsumowaniem w formie mowy

## 💰 Koszty

Aplikacja wyświetla **rzeczywiste koszty** po wygenerowaniu podsumowania w pasku bocznym:

- **Whisper-1**: $0.006 za minutę audio
- **GPT-4o**: $0.0025 za 1000 tokenów wejściowych, $0.01 za 1000 tokenów wyjściowych
- **TTS-1**: $0.015 za 1000 znaków *(tylko dla opcji audio)*

Koszty są obliczane na podstawie:
- Rzeczywistej długości audio w minutach (dla Whisper-1)
- Rzeczywistej liczby tokenów w transkrypcji i podsumowaniu (dla GPT-4o)
- Rzeczywistej liczby znaków w podsumowaniu (dla TTS-1)

**Przykładowy koszt:**
- 10-minutowe wideo: ~$0.06 (Whisper) + ~$0.01-0.05 (GPT) + ~$0.01 (TTS jeśli wybrano) = **$0.08-0.12 łącznie**

**Przykładowy koszt:**
- 10-minutowe wideo: ~$0.06 (Whisper) + ~$0.01-0.05 (GPT) + ~$0.01 (TTS jeśli wybrano) = **$0.08-0.12 łącznie**

## 📁 Struktura projektu

```
podsumowanie_audio_video_v9/
│
├── app.py                  # Główny plik aplikacji Streamlit (800+ linii)
├── utils.py                # Funkcje pomocnicze (ekstrakcja audio, TTS, eksport, YouTube)
├── requirements.txt        # Zależności projektu
├── .env.example           # Szablon pliku konfiguracyjnego
├── .env                   # Plik konfiguracyjny (tworzony przez użytkownika, nie w repo)
├── .gitignore             # Wykluczenia z repozytorium Git
├── README.md              # Dokumentacja projektu (ten plik)
├── INSTRUKCJA.md          # Szybki start i szczegółowa instrukcja (nie w repo)
└── prompt.txt             # Historia wymagań projektu (nie w repo)
```

### Pliki wykluczane z repozytorium (.gitignore)
- `.env` - klucz API
- `INSTRUKCJA.md` - instrukcja wewnętrzna
- `prompt.txt` - historia wymagań
- `__pycache__/` - cache Pythona
- Pliki tymczasowe (*.tmp, *_audio.mp3, temp_*.mp4, etc.)

## 🔧 Technologie

- **Streamlit** - framework do budowy interfejsu użytkownika
- **OpenAI API** - Whisper-1 do transkrypcji, GPT-4o do podsumowania, TTS-1 do generowania mowy
- **MoviePy** - ekstrakcja audio z wideo
- **yt-dlp** - pobieranie filmów z YouTube
- **FPDF** - generowanie plików PDF
- **python-docx** - generowanie plików DOCX
- **python-dotenv** - zarządzanie zmiennymi środowiskowymi

## ⚠️ Ważne uwagi

### Przetwarzanie
- ⏱️ Pliki wideo są konwertowane do MP3 przed transkrypcją
- ⏱️ Transkrypcja i podsumowanie mogą potrwać kilka minut w zależności od długości pliku
- ⏱️ Generowanie audio (TTS) dodaje dodatkowy czas przetwarzania (ok. 10-30 sekund)

### Edycja
- 🔒 **Podczas edycji (transkrypcji lub podsumowania) aplikacja blokuje:**
  - Przesyłanie nowych plików
  - Pobieranie z YouTube
  - Wszystkie przyciski przetwarzania
  - Przycisk resetowania
- 💾 **Musisz zapisać lub anulować zmiany** przed kontynuowaniem pracy
- 🔄 Przy edycji podsumowania w trybie audio - audio zostanie automatycznie zregenerowane po zapisaniu

### Formaty eksportu
- ✅ **DOCX i TXT** - pełne wsparcie polskich znaków (zalecane)
- ⚠️ **PDF** - ograniczone wsparcie Unicode, polskie znaki mogą być zastąpione

### Koszty i bezpieczeństwo
- 💰 Koszty są obliczane na podstawie rzeczywistych danych
- 🔐 **Nigdy nie udostępniaj publicznie pliku `.env` z kluczem API**
- 🔐 Plik `.env` jest automatycznie wykluczony z repozytorium Git

### Techniczne
- 🎙️ Aplikacja używa głosu "onyx" dla TTS (można zmienić w kodzie: linia z `generuj_audio_z_tekstu`)
- 📁 Pliki tymczasowe są automatycznie usuwane przez system operacyjny

## 🎙️ Dostępne głosy TTS

Aplikacja domyślnie używa głosu **"onyx"**. OpenAI TTS-1 oferuje następujące głosy:
- **alloy** - neutralny
- **echo** - męski
- **fable** - brytyjski męski
- **onyx** - głęboki męski *(domyślny w aplikacji)*
- **nova** - kobiecy
- **shimmer** - kobiecy

Aby zmienić głos, edytuj plik [app.py](app.py) i [utils.py](utils.py) - znajdź wywołania funkcji `generuj_audio_z_tekstu` i zmień parametr `glos="onyx"` na wybrany głos.

## 📝 Licencja

MIT

## 👨‍💻 Autor

Lukasz_Es / Lukasz6855
