import streamlit as st  # Framework do budowy interfejsu użytkownika
import os  # Operacje na systemie plików
from dotenv import load_dotenv  # Ładowanie zmiennych środowiskowych z pliku .env
from openai import OpenAI  # Klient API OpenAI
import tempfile  # Tworzenie plików tymczasowych
from pathlib import Path  # Obsługa ścieżek plików
from utils import (  # Import funkcji pomocniczych z modułu utils
    wyodrebnij_audio_z_wideo,
    oblicz_koszt_transkrypcji,
    oblicz_koszt_gpt,
    oblicz_koszt_tts,
    generuj_plik_txt,
    generuj_plik_pdf,
    generuj_plik_docx,
    pobierz_rozmiar_pliku_mb,
    pobierz_dlugosc_audio,
    formatuj_czas_na_min_sec,
    zlicz_slowa,
    szacuj_tokeny_z_slow,
    pobierz_wideo_z_youtube,
    generuj_audio_z_tekstu
)

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Konfiguracja strony Streamlit
st.set_page_config(
    page_title="Transkrypcja i Podsumowanie Audio/Wideo",  # Tytuł zakładki przeglądarki
    page_icon="🎬",  # Ikona zakładki
    layout="wide"  # Szeroki układ strony
)

# Tytuł główny aplikacji
st.title("🎬 Transkrypcja i Podsumowanie Audio/Wideo")
st.markdown("Prześlij plik audio lub wideo, aby uzyskać transkrypcję i podsumowanie przy użyciu AI")

# Inicjalizacja zmiennych w sesji Streamlit (stan aplikacji)
if 'transkrypcja' not in st.session_state:  # Sprawdzenie czy zmienna transkrypcja istnieje
    st.session_state.transkrypcja = None  # Inicjalizacja zmiennej transkrypcja
if 'podsumowanie' not in st.session_state:  # Sprawdzenie czy zmienna podsumowanie istnieje
    st.session_state.podsumowanie = None  # Inicjalizacja zmiennej podsumowanie
if 'sciezka_audio' not in st.session_state:  # Sprawdzenie czy zmienna sciezka_audio istnieje
    st.session_state.sciezka_audio = None  # Inicjalizacja zmiennej sciezka_audio
if 'nazwa_pliku' not in st.session_state:  # Sprawdzenie czy zmienna nazwa_pliku istnieje
    st.session_state.nazwa_pliku = None  # Inicjalizacja zmiennej nazwa_pliku
if 'sciezka_temp' not in st.session_state:  # Sprawdzenie czy zmienna sciezka_temp istnieje
    st.session_state.sciezka_temp = None  # Inicjalizacja zmiennej sciezka_temp
if 'rozszerzenie' not in st.session_state:  # Sprawdzenie czy zmienna rozszerzenie istnieje
    st.session_state.rozszerzenie = None  # Inicjalizacja zmiennej rozszerzenie
if 'rozmiar_mb' not in st.session_state:  # Sprawdzenie czy zmienna rozmiar_mb istnieje
    st.session_state.rozmiar_mb = None  # Inicjalizacja zmiennej rozmiar_mb
if 'dlugosc_audio_minuty' not in st.session_state:  # Sprawdzenie czy zmienna dlugosc_audio_minuty istnieje
    st.session_state.dlugosc_audio_minuty = None  # Inicjalizacja zmiennej dlugosc_audio_minuty
if 'youtube_url' not in st.session_state:  # Sprawdzenie czy zmienna youtube_url istnieje
    st.session_state.youtube_url = None  # Inicjalizacja zmiennej youtube_url
if 'sciezka_audio_podsumowania' not in st.session_state:  # Sprawdzenie czy zmienna sciezka_audio_podsumowania istnieje
    st.session_state.sciezka_audio_podsumowania = None  # Inicjalizacja zmiennej sciezka_audio_podsumowania
if 'tryb_generowania' not in st.session_state:  # Sprawdzenie czy zmienna tryb_generowania istnieje
    st.session_state.tryb_generowania = None  # Inicjalizacja zmiennej tryb_generowania (tekstowe/audio)
if 'edytowana_transkrypcja' not in st.session_state:  # Sprawdzenie czy zmienna edytowana_transkrypcja istnieje
    st.session_state.edytowana_transkrypcja = None  # Inicjalizacja zmiennej edytowana_transkrypcja
if 'edycja_podsumowania_aktywna' not in st.session_state:  # Sprawdzenie czy zmienna edycja_podsumowania_aktywna istnieje
    st.session_state.edycja_podsumowania_aktywna = False  # Inicjalizacja zmiennej edycja_podsumowania_aktywna (False = tylko do odczytu)
if 'edycja_transkrypcji_aktywna' not in st.session_state:  # Sprawdzenie czy zmienna edycja_transkrypcji_aktywna istnieje
    st.session_state.edycja_transkrypcji_aktywna = False  # Inicjalizacja zmiennej edycja_transkrypcji_aktywna (False = tylko do odczytu)
if 'podsumowanie_przed_edycja' not in st.session_state:  # Sprawdzenie czy zmienna podsumowanie_przed_edycja istnieje
    st.session_state.podsumowanie_przed_edycja = None  # Inicjalizacja zmiennej podsumowanie_przed_edycja (do przechowania stanu przed edycją)
if 'transkrypcja_przed_edycja' not in st.session_state:  # Sprawdzenie czy zmienna transkrypcja_przed_edycja istnieje
    st.session_state.transkrypcja_przed_edycja = None  # Inicjalizacja zmiennej transkrypcja_przed_edycja (do przechowania stanu przed edycją)
if 'transkrypcja_zapisana' not in st.session_state:  # Sprawdzenie czy zmienna transkrypcja_zapisana istnieje
    st.session_state.transkrypcja_zapisana = False  # Inicjalizacja zmiennej transkrypcja_zapisana (czy transkrypcja została zapisana po edycji)
if 'edytowana_transkrypcja_temp' not in st.session_state:  # Sprawdzenie czy zmienna edytowana_transkrypcja_temp istnieje
    st.session_state.edytowana_transkrypcja_temp = None  # Inicjalizacja zmiennej tymczasowej dla edytowanej transkrypcji
if 'edytowane_podsumowanie_temp' not in st.session_state:  # Sprawdzenie czy zmienna edytowane_podsumowanie_temp istnieje
    st.session_state.edytowane_podsumowanie_temp = None  # Inicjalizacja zmiennej tymczasowej dla edytowanego podsumowania
if 'podsumowanie_wersja' not in st.session_state:  # Sprawdzenie czy zmienna podsumowanie_wersja istnieje
    st.session_state.podsumowanie_wersja = 0  # Inicjalizacja licznika wersji podsumowania (używany do wymuszenia odświeżenia widgetu)

# Sekcja obsługi klucza API OpenAI
st.sidebar.header("⚙️ Konfiguracja")  # Nagłówek w pasku bocznym

# Pobranie klucza API z pliku .env
klucz_api_z_env = os.getenv("OPENAI_API_KEY")  # Odczytanie klucza z zmiennej środowiskowej

# Sprawdzenie czy klucz API jest zapisany w .env
if klucz_api_z_env and klucz_api_z_env != "sk-twoj-klucz-api-tutaj":  # Sprawdzenie czy klucz jest prawidłowy
    klucz_api = klucz_api_z_env  # Użycie klucza z .env
    st.sidebar.success("✅ Klucz API załadowany z pliku .env")  # Komunikat o sukcesie
else:  # Jeśli klucz nie jest dostępny w .env
    klucz_api = st.sidebar.text_input(  # Pole tekstowe do wprowadzenia klucza
        "Klucz API OpenAI:",  # Etykieta pola
        type="password",  # Typ pola - hasło (ukryte znaki)
        help="Wprowadź swój klucz API OpenAI"  # Tekst pomocy
    )
    if not klucz_api:  # Sprawdzenie czy klucz został wprowadzony
        st.sidebar.warning("⚠️ Wprowadź klucz API OpenAI aby kontynuować")  # Ostrzeżenie
        st.stop()  # Zatrzymanie wykonywania aplikacji

# Inicjalizacja klienta OpenAI z kluczem API
try:  # Próba utworzenia klienta
    klient = OpenAI(api_key=klucz_api)  # Utworzenie obiektu klienta OpenAI
except Exception as e:  # Obsługa błędów
    st.error(f"❌ Błąd inicjalizacji klienta OpenAI: {str(e)}")  # Wyświetlenie błędu
    st.stop()  # Zatrzymanie aplikacji

# Sprawdzenie czy jakakolwiek edycja jest aktywna (używane do blokowania przycisków)
edycja_aktywna = st.session_state.edycja_podsumowania_aktywna or st.session_state.edycja_transkrypcji_aktywna  # Zmienna pomocnicza określająca czy jest aktywna jakakolwiek edycja

# Sekcja przesyłania plików w pasku bocznym
st.sidebar.header("📤 Prześlij plik")  # Nagłówek sekcji w sidebarze

# Widget do przesyłania plików w pasku bocznym
przeslany_plik = st.sidebar.file_uploader(  # Umieszczenie uploadera w sidebarze
    "Wybierz plik audio lub wideo",  # Etykieta
    type=['mp3', 'wav', 'mp4', 'avi', 'mov'],  # Dozwolone rozszerzenia plików
    help="Obsługiwane formaty: MP3, WAV, MP4, AVI, MOV",  # Tekst pomocy
    disabled=edycja_aktywna  # Widget wyłączony gdy edycja aktywna
)

# Sekcja pobierania z YouTube
st.sidebar.header("🎥 Pobierz z YouTube")  # Nagłówek sekcji YouTube
youtube_url = st.sidebar.text_input(  # Pole tekstowe na link YouTube
    "Link do filmu YouTube:",  # Etykieta
    placeholder="https://www.youtube.com/watch?v=...",  # Tekst zastępczy
    help="Wklej link do filmu z YouTube",  # Tekst pomocy
    disabled=edycja_aktywna  # Pole wyłączone gdy edycja aktywna
)

if st.sidebar.button("📥 Pobierz wideo z YouTube", key="download_youtube", disabled=edycja_aktywna):  # Przycisk pobierania (wyszarzony gdy edycja aktywna)
    if youtube_url:  # Sprawdzenie czy URL został podany
        with st.spinner("Pobieranie wideo z YouTube... To może potrwać kilka minut."):  # Wskaźnik postępu
            try:  # Próba pobrania wideo
                sciezka_pliku, tytul = pobierz_wideo_z_youtube(youtube_url)  # Pobranie wideo
                
                # Zapisanie danych do session_state
                st.session_state.sciezka_temp = sciezka_pliku  # Zapisanie ścieżki
                st.session_state.rozszerzenie = Path(sciezka_pliku).suffix.lower()  # Zapisanie rozszerzenia
                st.session_state.rozmiar_mb = pobierz_rozmiar_pliku_mb(sciezka_pliku)  # Zapisanie rozmiaru
                st.session_state.nazwa_pliku = tytul  # Zapisanie tytułu jako nazwy pliku
                st.session_state.dlugosc_audio_minuty = pobierz_dlugosc_audio(sciezka_pliku)  # Pobranie długości
                st.session_state.youtube_url = youtube_url  # Zapisanie URL
                
                st.sidebar.success("✅ Wideo pobrane pomyślnie!")  # Komunikat sukcesu
                st.rerun()  # Odświeżenie aplikacji aby pokazać wideo
            except Exception as e:  # Obsługa błędów
                st.sidebar.error(f"❌ Błąd podczas pobierania wideo: {str(e)}")  # Wyświetlenie błędu
    else:  # Jeśli URL nie został podany
        st.sidebar.warning("⚠️ Wprowadź link do filmu YouTube")  # Ostrzeżenie

# Sprawdzenie czy plik został przesłany
if przeslany_plik is not None:  # Jeśli plik został wybrany
    # Zapisanie przesłanego pliku tymczasowo
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(przeslany_plik.name).suffix) as plik_temp:  # Utworzenie pliku tymczasowego
        plik_temp.write(przeslany_plik.read())  # Zapisanie zawartości przesłanego pliku
        sciezka_temp = plik_temp.name  # Pobranie ścieżki pliku tymczasowego
    
    # Zapisanie danych pliku do session_state aby zachować je między odświeżeniami
    st.session_state.sciezka_temp = sciezka_temp  # Zapisanie ścieżki tymczasowej
    st.session_state.rozszerzenie = Path(przeslany_plik.name).suffix.lower()  # Zapisanie rozszerzenia
    st.session_state.rozmiar_mb = pobierz_rozmiar_pliku_mb(sciezka_temp)  # Zapisanie rozmiaru
    st.session_state.nazwa_pliku = Path(przeslany_plik.name).stem  # Zapisanie nazwy pliku
    st.session_state.dlugosc_audio_minuty = pobierz_dlugosc_audio(sciezka_temp)  # Pobranie długości audio/wideo

# Wyświetlanie interfejsu jeśli plik został kiedykolwiek przesłany
if st.session_state.sciezka_temp is not None:  # Sprawdzenie czy istnieje zapisana ścieżka
    sciezka_temp = st.session_state.sciezka_temp  # Pobranie ścieżki z session_state
    rozszerzenie = st.session_state.rozszerzenie  # Pobranie rozszerzenia z session_state
    rozmiar_mb = st.session_state.rozmiar_mb  # Pobranie rozmiaru z session_state
    
    # Wyświetlanie odtwarzacza w zależności od typu pliku
    st.subheader("🎥 Podgląd pliku")  # Nagłówek podsekcji
    
    col1, col2 = st.columns([2, 1])  # Utworzenie dwóch kolumn o proporcjach 2:1
    
    with col1:  # Zawartość pierwszej kolumny
        if rozszerzenie in ['.mp4', '.avi', '.mov']:  # Sprawdzenie czy plik jest wideo
            st.video(sciezka_temp)  # Wyświetlenie odtwarzacza wideo
        elif rozszerzenie in ['.mp3', '.wav']:  # Sprawdzenie czy plik jest audio
            st.audio(sciezka_temp)  # Wyświetlenie odtwarzacza audio
    
    with col2:  # Zawartość drugiej kolumny
        # Informacje o pliku
        st.info(f"📄 **Nazwa:** {st.session_state.nazwa_pliku}")  # Wyświetlenie nazwy pliku
        st.info(f"💾 **Rozmiar:** {rozmiar_mb:.2f} MB")  # Wyświetlenie rozmiaru
        if st.session_state.dlugosc_audio_minuty:  # Jeśli długość została odczytana
            dlugosc_sformatowana = formatuj_czas_na_min_sec(st.session_state.dlugosc_audio_minuty)  # Formatowanie długości na format "X min Y sec"
            st.info(f"⏱️ **Długość:** {dlugosc_sformatowana}")  # Wyświetlenie długości w formacie X min Y sec
    
    # ===== SEKCJA PODSUMOWANIA - OPCJA SZYBKA =====
    st.markdown("---")
    st.markdown("## 📋 Generowanie podsumowania")
    st.markdown("---")
    
    # Utworzenie dwóch kolumn dla pól wyboru
    col1, col2 = st.columns(2)  # Dwie kolumny o równej szerokości
    
    with col1:  # Pierwsza kolumna - wybór długości
        dlugosc = st.selectbox(  # Pole wyboru dla długości podsumowania
            "Długość:",  # Etykieta pola
            ["Krótkie", "Średnie", "Długie"],  # Opcje do wyboru
            index=1,  # Domyślnie wybrane "Średnie" (indeks 1)
            help="Wybierz długość podsumowania",  # Tekst pomocy
            key="dlugosc_select",  # Unikalny klucz
            disabled=edycja_aktywna  # Pole wyłączone gdy edycja aktywna
        )
        # Zapisanie wybranej wartości w session_state (aby była dostępna nawet gdy selectbox jest wyszarzony)
        if dlugosc is not None:  # Jeśli wartość istnieje
            st.session_state.wybrana_dlugosc = dlugosc  # Zapisanie w session_state
    
    with col2:  # Druga kolumna - wybór stylu
        styl = st.selectbox(  # Pole wyboru dla stylu podsumowania
            "Styl:",  # Etykieta pola
            ["Tekstowe", "W punktach"],  # Opcje do wyboru
            index=0,  # Domyślnie wybrane "Tekstowe" (indeks 0)
            help="Wybierz styl podsumowania",  # Tekst pomocy
            key="styl_select",  # Unikalny klucz
            disabled=edycja_aktywna  # Pole wyłączone gdy edycja aktywna
        )
        # Zapisanie wybranej wartości w session_state (aby była dostępna nawet gdy selectbox jest wyszarzony)
        if styl is not None:  # Jeśli wartość istnieje
            st.session_state.wybrany_styl = styl  # Zapisanie w session_state
    
    # Użycie wartości z session_state jeśli selectboxy są wyszarzone
    if edycja_aktywna:  # Jeśli edycja jest aktywna
        dlugosc = st.session_state.get('wybrana_dlugosc', 'Średnie')  # Pobranie wartości z session_state lub domyślna
        styl = st.session_state.get('wybrany_styl', 'Tekstowe')  # Pobranie wartości z session_state lub domyślna
    
    # Utworzenie dwóch kolumn dla przycisków opcji szybkiej
    col1, col2 = st.columns(2)  # Dwie kolumny o równej szerokości
    
    with col1:  # Pierwsza kolumna - opcja tekstowa
        if st.button("📝 Wygeneruj podsumowanie tekstowe", key="quick_text", use_container_width=True, disabled=edycja_aktywna):  # Przycisk opcji szybkiej tekstowej (wyszarzony gdy edycja aktywna)
            st.session_state.tryb_generowania = "tekstowe"  # Ustawienie trybu generowania
            
            with st.spinner("Przetwarzanie... To może potrwać kilka minut."):  # Wskaźnik postępu
                try:  # Próba przetwarzania
                    # Krok 1: Ekstrakcja audio z wideo (jeśli potrzebne)
                    if rozszerzenie in ['.mp4', '.avi', '.mov'] and not st.session_state.sciezka_audio:  # Jeśli wideo i brak audio
                        sciezka_audio = wyodrebnij_audio_z_wideo(sciezka_temp)  # Ekstrakcja audio
                        st.session_state.sciezka_audio = sciezka_audio  # Zapisanie ścieżki audio
                    
                    # Określenie ścieżki do transkrypcji
                    if rozszerzenie in ['.mp4', '.avi', '.mov']:  # Jeśli wideo
                        sciezka_do_transkrypcji = st.session_state.sciezka_audio  # Użycie wyodrębnionego audio
                    else:  # Jeśli audio
                        sciezka_do_transkrypcji = sciezka_temp  # Użycie oryginalnego pliku
                    
                    # Krok 2: Transkrypcja (jeśli jeszcze nie wykonana)
                    if not st.session_state.transkrypcja:  # Jeśli transkrypcja nie istnieje
                        with open(sciezka_do_transkrypcji, 'rb') as plik_audio:  # Otwarcie pliku audio
                            odpowiedz = klient.audio.transcriptions.create(  # Wywołanie API Whisper
                                model="whisper-1",  # Model do transkrypcji
                                file=(f"{st.session_state.nazwa_pliku}.mp3", plik_audio, "audio/mpeg"),  # Plik audio
                                language="pl"  # Język polski
                            )
                            st.session_state.transkrypcja = odpowiedz.text  # Zapisanie transkrypcji
                    
                    # Krok 3: Generowanie podsumowania
                    instrukcja_dlugosc = {  # Słownik z instrukcjami dla różnych długości
                        "Krótkie": "Stwórz krótkie podsumowanie (maksymalnie 3-4 zdania).",
                        "Średnie": "Stwórz średniej długości podsumowanie (5-8 zdań).",
                        "Długie": "Stwórz szczegółowe, rozbudowane podsumowanie."
                    }
                    
                    instrukcja_styl = {  # Słownik z instrukcjami dla różnych stylów
                        "Tekstowe": "Przedstaw podsumowanie w formie spójnego tekstu.",
                        "W punktach": "Przedstaw podsumowanie w formie numerowanej listy punktów. Użyj numeracji: 1. ... ; 2. ... ; 3. ... itd."
                    }
                    
                    prompt_systemowy = f"Jesteś asystentem AI specjalizującym się w tworzeniu zwięzłych i treściwych podsumowań. {instrukcja_dlugosc[dlugosc]} {instrukcja_styl[styl]} Stwórz podsumowanie poniższej transkrypcji w języku polskim."  # Pełna instrukcja
                    
                    odpowiedz_gpt = klient.chat.completions.create(  # Wywołanie API GPT
                        model="gpt-4o",  # Model GPT-4o
                        messages=[  # Lista wiadomości
                            {"role": "system", "content": prompt_systemowy},  # Wiadomość systemowa
                            {"role": "user", "content": f"Podsumuj następującą transkrypcję:\n\n{st.session_state.transkrypcja}"}  # Wiadomość użytkownika
                        ],
                        temperature=0.7  # Parametr kreatywności
                    )
                    
                    st.session_state.podsumowanie = odpowiedz_gpt.choices[0].message.content  # Zapisanie podsumowania
                    st.session_state.podsumowanie_wersja += 1  # Zwiększenie licznika wersji (wymusza odświeżenie widgetu)
                    
                    st.success("✅ Podsumowanie tekstowe wygenerowane pomyślnie!")  # Komunikat sukcesu
                    st.rerun()  # Odświeżenie aplikacji
                    
                except Exception as e:  # Obsługa błędów
                    st.error(f"❌ Błąd podczas generowania: {str(e)}")  # Wyświetlenie błędu
    
    with col2:  # Druga kolumna - opcja audio
        if st.button("🔊 Wygeneruj podsumowanie audio", key="quick_audio", use_container_width=True, disabled=edycja_aktywna):  # Przycisk opcji szybkiej audio (wyszarzony gdy edycja aktywna)
            st.session_state.tryb_generowania = "audio"  # Ustawienie trybu generowania
            
            with st.spinner("Przetwarzanie i generowanie audio... To może potrwać kilka minut."):  # Wskaźnik postępu
                try:  # Próba przetwarzania
                    # Krok 1: Ekstrakcja audio z wideo (jeśli potrzebne)
                    if rozszerzenie in ['.mp4', '.avi', '.mov'] and not st.session_state.sciezka_audio:  # Jeśli wideo i brak audio
                        sciezka_audio = wyodrebnij_audio_z_wideo(sciezka_temp)  # Ekstrakcja audio
                        st.session_state.sciezka_audio = sciezka_audio  # Zapisanie ścieżki audio
                    
                    # Określenie ścieżki do transkrypcji
                    if rozszerzenie in ['.mp4', '.avi', '.mov']:  # Jeśli wideo
                        sciezka_do_transkrypcji = st.session_state.sciezka_audio  # Użycie wyodrębnionego audio
                    else:  # Jeśli audio
                        sciezka_do_transkrypcji = sciezka_temp  # Użycie oryginalnego pliku
                    
                    # Krok 2: Transkrypcja (jeśli jeszcze nie wykonana)
                    if not st.session_state.transkrypcja:  # Jeśli transkrypcja nie istnieje
                        with open(sciezka_do_transkrypcji, 'rb') as plik_audio:  # Otwarcie pliku audio
                            odpowiedz = klient.audio.transcriptions.create(  # Wywołanie API Whisper
                                model="whisper-1",  # Model do transkrypcji
                                file=(f"{st.session_state.nazwa_pliku}.mp3", plik_audio, "audio/mpeg"),  # Plik audio
                                language="pl"  # Język polski
                            )
                            st.session_state.transkrypcja = odpowiedz.text  # Zapisanie transkrypcji
                    
                    # Krok 3: Generowanie podsumowania tekstowego
                    instrukcja_dlugosc = {  # Słownik z instrukcjami dla różnych długości
                        "Krótkie": "Stwórz krótkie podsumowanie (maksymalnie 3-4 zdania).",
                        "Średnie": "Stwórz średniej długości podsumowanie (5-8 zdań).",
                        "Długie": "Stwórz szczegółowe, rozbudowane podsumowanie."
                    }
                    
                    instrukcja_styl = {  # Słownik z instrukcjami dla różnych stylów
                        "Tekstowe": "Przedstaw podsumowanie w formie spójnego tekstu.",
                        "W punktach": "Przedstaw podsumowanie w formie numerowanej listy punktów. Użyj numeracji: 1. ... ; 2. ... ; 3. ... itd."
                    }
                    
                    prompt_systemowy = f"Jesteś asystentem AI specjalizującym się w tworzeniu zwięzłych i treściwych podsumowań. {instrukcja_dlugosc[dlugosc]} {instrukcja_styl[styl]} Stwórz podsumowanie poniższej transkrypcji w języku polskim."  # Pełna instrukcja
                    
                    odpowiedz_gpt = klient.chat.completions.create(  # Wywołanie API GPT
                        model="gpt-4o",  # Model GPT-4o
                        messages=[  # Lista wiadomości
                            {"role": "system", "content": prompt_systemowy},  # Wiadomość systemowa
                            {"role": "user", "content": f"Podsumuj następującą transkrypcję:\n\n{st.session_state.transkrypcja}"}  # Wiadomość użytkownika
                        ],
                        temperature=0.7  # Parametr kreatywności
                    )
                    
                    st.session_state.podsumowanie = odpowiedz_gpt.choices[0].message.content  # Zapisanie podsumowania
                    st.session_state.podsumowanie_wersja += 1  # Zwiększenie licznika wersji (wymusza odświeżenie widgetu)
                    
                    # Krok 4: Generowanie audio z podsumowania (TTS)
                    sciezka_audio_podsumowania = os.path.join(tempfile.gettempdir(), f"{st.session_state.nazwa_pliku}_podsumowanie.mp3")  # Ścieżka dla audio podsumowania
                    generuj_audio_z_tekstu(klient, st.session_state.podsumowanie, sciezka_audio_podsumowania, glos="onyx")  # Generowanie audio
                    st.session_state.sciezka_audio_podsumowania = sciezka_audio_podsumowania  # Zapisanie ścieżki audio podsumowania
                    
                    st.success("✅ Podsumowanie audio wygenerowane pomyślnie!")  # Komunikat sukcesu
                    st.rerun()  # Odświeżenie aplikacji
                    
                except Exception as e:  # Obsługa błędów
                    st.error(f"❌ Błąd podczas generowania: {str(e)}")  # Wyświetlenie błędu
    
    # Wyświetlenie podsumowania tekstowego jeśli istnieje
    if st.session_state.podsumowanie:  # Sprawdzenie czy podsumowanie zostało wygenerowane
        # Pole tekstowe podsumowania - edytowalne lub tylko do odczytu (renderowane PRZED przyciskami aby zachować wartość)
        if st.session_state.edycja_podsumowania_aktywna:  # Jeśli edycja jest aktywna
            edytowane_podsumowanie = st.text_area(  # Pole tekstowe edytowalne
                "Podsumowanie:",  # Etykieta
                value=st.session_state.podsumowanie,  # Treść podsumowania
                height=200,  # Wysokość pola
                key=f"summary_edit_area_v{st.session_state.podsumowanie_wersja}"  # Unikalny klucz z wersją
            )
            # Zapisanie zmian w zmiennej tymczasowej (aby były dostępne dla przycisku "Zapisz zmiany")
            st.session_state.edytowane_podsumowanie_temp = edytowane_podsumowanie  # Zapis w zmiennej tymczasowej
        else:  # Jeśli edycja nie jest aktywna (tylko do odczytu)
            st.text_area(  # Pole tekstowe tylko do odczytu
                "Podsumowanie:",  # Etykieta
                value=st.session_state.podsumowanie,  # Treść podsumowania
                height=200,  # Wysokość pola
                disabled=True,  # Pole wyłączone (tylko do odczytu)
                key=f"summary_readonly_area_v{st.session_state.podsumowanie_wersja}"  # Unikalny klucz z wersją
            )
        
        # Przyciski kontroli edycji podsumowania
        col_edit1, col_edit2, col_edit3 = st.columns([1, 1, 1])  # Trzy kolumny dla przycisków edycji
        
        with col_edit1:  # Pierwsza kolumna - przycisk Edycja
            if st.button("✏️ Edycja", key="edit_summary_btn", disabled=st.session_state.edycja_podsumowania_aktywna or st.session_state.edycja_transkrypcji_aktywna):  # Przycisk Edycja (wyszarzony gdy jakakolwiek edycja aktywna)
                st.session_state.edycja_podsumowania_aktywna = True  # Aktywacja trybu edycji podsumowania
                st.session_state.podsumowanie_przed_edycja = st.session_state.podsumowanie  # Zapisanie stanu przed edycją
                st.rerun()  # Odświeżenie aplikacji
        
        with col_edit2:  # Druga kolumna - przycisk Anuluj edycję
            if st.button("❌ Anuluj edycję", key="cancel_summary_edit_btn", disabled=not st.session_state.edycja_podsumowania_aktywna):  # Przycisk Anuluj (aktywny tylko gdy edycja podsumowania aktywna)
                st.session_state.podsumowanie = st.session_state.podsumowanie_przed_edycja  # Przywrócenie stanu przed edycją
                st.session_state.edycja_podsumowania_aktywna = False  # Wyłączenie trybu edycji
                st.session_state.podsumowanie_przed_edycja = None  # Wyczyszczenie kopii zapasowej
                st.session_state.edytowane_podsumowanie_temp = None  # Wyczyszczenie zmiennej tymczasowej
                st.rerun()  # Odświeżenie aplikacji
        
        with col_edit3:  # Trzecia kolumna - przycisk Zapisz zmiany
            if st.button("💾 Zapisz zmiany", key="save_summary_btn", disabled=not st.session_state.edycja_podsumowania_aktywna):  # Przycisk Zapisz (aktywny tylko gdy edycja podsumowania aktywna)
                # Zapisanie edytowanego podsumowania ze zmiennej tymczasowej do głównej zmiennej
                if st.session_state.edytowane_podsumowanie_temp is not None:  # Jeśli zmienna tymczasowa zawiera dane
                    st.session_state.podsumowanie = st.session_state.edytowane_podsumowanie_temp  # Zapisanie zmian
                
                # Jeśli tryb generowania to audio, regeneruj audio podsumowania z nowym tekstem
                if st.session_state.tryb_generowania == "audio":  # Jeśli wcześniej było wygenerowane audio
                    with st.spinner("Regenerowanie audio podsumowania z zaktualizowanym tekstem..."):  # Wskaźnik postępu
                        try:  # Próba regeneracji audio
                            sciezka_audio_podsumowania = os.path.join(tempfile.gettempdir(), f"{st.session_state.nazwa_pliku}_podsumowanie.mp3")  # Ścieżka dla audio
                            generuj_audio_z_tekstu(klient, st.session_state.podsumowanie, sciezka_audio_podsumowania, glos="onyx")  # Generowanie audio z nowego tekstu
                            st.session_state.sciezka_audio_podsumowania = sciezka_audio_podsumowania  # Zapisanie ścieżki audio
                        except Exception as e:  # Obsługa błędów
                            st.error(f"❌ Błąd podczas regeneracji audio: {str(e)}")  # Wyświetlenie błędu
                
                st.session_state.edycja_podsumowania_aktywna = False  # Wyłączenie trybu edycji
                st.session_state.podsumowanie_przed_edycja = None  # Wyczyszczenie kopii zapasowej
                st.session_state.edytowane_podsumowanie_temp = None  # Wyczyszczenie zmiennej tymczasowej
                st.success("✅ Zmiany w podsumowaniu zostały zapisane!" + (" Audio podsumowania zostało zaktualizowane." if st.session_state.tryb_generowania == "audio" else ""))  # Komunikat sukcesu
                st.rerun()  # Odświeżenie aplikacji
        
        # Przycisk Resetuj wszystko - szerszy, pod przyciskami edycji
        if st.button("🔄 Resetuj wszystko i zacznij od nowa", key="reset_all_btn", use_container_width=True, disabled=edycja_aktywna):  # Przycisk Resetuj wszystko (wyszarzony gdy edycja aktywna)
            # Resetowanie wszystkich zmiennych do stanu początkowego
            st.session_state.transkrypcja = None  # Wyczyszczenie transkrypcji
            st.session_state.podsumowanie = None  # Wyczyszczenie podsumowania
            st.session_state.sciezka_audio = None  # Wyczyszczenie ścieżki audio
            st.session_state.sciezka_audio_podsumowania = None  # Wyczyszczenie ścieżki audio podsumowania
            st.session_state.tryb_generowania = None  # Wyczyszczenie trybu generowania
            st.session_state.edytowana_transkrypcja = None  # Wyczyszczenie edytowanej transkrypcji
            st.session_state.edycja_podsumowania_aktywna = False  # Wyłączenie edycji podsumowania
            st.session_state.edycja_transkrypcji_aktywna = False  # Wyłączenie edycji transkrypcji
            st.session_state.podsumowanie_przed_edycja = None  # Wyczyszczenie kopii zapasowej podsumowania
            st.session_state.transkrypcja_przed_edycja = None  # Wyczyszczenie kopii zapasowej transkrypcji
            st.session_state.transkrypcja_zapisana = False  # Wyzerowanie flagi zapisu transkrypcji
            st.session_state.edytowana_transkrypcja_temp = None  # Wyczyszczenie zmiennej tymczasowej transkrypcji
            st.session_state.edytowane_podsumowanie_temp = None  # Wyczyszczenie zmiennej tymczasowej podsumowania
            st.success("✅ Aplikacja została zresetowana!")  # Komunikat sukcesu
            st.rerun()  # Odświeżenie aplikacji
    
    # Wyświetlenie odtwarzacza audio podsumowania jeśli istnieje
    if st.session_state.sciezka_audio_podsumowania:  # Sprawdzenie czy audio podsumowania zostało wygenerowane
        st.subheader("🔊 Podsumowanie w formie audio")  # Nagłówek podsekcji
        st.audio(st.session_state.sciezka_audio_podsumowania)  # Odtwarzacz audio podsumowania
    
    # ===== SEKCJA POBIERANIA WYNIKÓW =====
    # Wyświetlanie sekcji pobierania jeśli podsumowanie istnieje
    if st.session_state.podsumowanie:  # Sprawdzenie czy podsumowanie zostało wygenerowane
        st.markdown("---")
        st.markdown("## ⬇️ Pobierz wyniki")
        st.markdown("---")
        
        # Tworzenie kolumn dla przycisków pobierania
        if st.session_state.tryb_generowania == "audio" and st.session_state.sciezka_audio_podsumowania:  # Jeśli tryb audio
            col1, col2, col3, col4 = st.columns(4)  # Utworzenie czterech kolumn
        else:  # Jeśli tryb tekstowy
            col1, col2, col3 = st.columns(3)  # Utworzenie trzech kolumn
        
        with col1:  # Pierwsza kolumna - TXT
            tresc_txt = generuj_plik_txt(  # Generowanie zawartości pliku TXT
                st.session_state.nazwa_pliku,  # Nazwa pliku
                st.session_state.transkrypcja,  # Transkrypcja
                st.session_state.podsumowanie  # Podsumowanie
            )
            st.download_button(  # Przycisk pobierania TXT
                label="📄 Pobierz TXT",  # Etykieta
                data=tresc_txt,  # Dane
                file_name=f"{st.session_state.nazwa_pliku}_transkrypcja.txt",  # Nazwa pliku
                mime="text/plain"  # Typ MIME
            )
        
        with col2:  # Druga kolumna - PDF
            try:  # Próba generowania PDF
                bajty_pdf = generuj_plik_pdf(  # Generowanie pliku PDF
                    st.session_state.nazwa_pliku,  # Nazwa pliku
                    st.session_state.transkrypcja,  # Transkrypcja
                    st.session_state.podsumowanie  # Podsumowanie
                )
                st.download_button(  # Przycisk pobierania PDF
                    label="📕 Pobierz PDF",  # Etykieta
                    data=bajty_pdf,  # Dane
                    file_name=f"{st.session_state.nazwa_pliku}_transkrypcja.pdf",  # Nazwa pliku
                    mime="application/pdf"  # Typ MIME
                )
            except Exception as e:  # Obsługa błędów
                st.error(f"Błąd generowania PDF: {str(e)}")  # Wyświetlenie błędu
        
        with col3:  # Trzecia kolumna - DOCX
            try:  # Próba generowania DOCX
                bajty_docx = generuj_plik_docx(  # Generowanie pliku DOCX
                    st.session_state.nazwa_pliku,  # Nazwa pliku
                    st.session_state.transkrypcja,  # Transkrypcja
                    st.session_state.podsumowanie  # Podsumowanie
                )
                st.download_button(  # Przycisk pobierania DOCX
                    label="📘 Pobierz DOCX",  # Etykieta
                    data=bajty_docx,  # Dane
                    file_name=f"{st.session_state.nazwa_pliku}_transkrypcja.docx",  # Nazwa pliku
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"  # Typ MIME
                )
            except Exception as e:  # Obsługa błędów
                st.error(f"Błąd generowania DOCX: {str(e)}")  # Wyświetlenie błędu
        
        # Czwarta kolumna - Audio MP3 podsumowania (tylko jeśli tryb audio)
        if st.session_state.tryb_generowania == "audio" and st.session_state.sciezka_audio_podsumowania:  # Jeśli tryb audio i audio istnieje
            with col4:  # Czwarta kolumna
                with open(st.session_state.sciezka_audio_podsumowania, 'rb') as plik_audio_podsumowania:  # Otwarcie pliku audio podsumowania
                    st.download_button(  # Przycisk pobierania audio podsumowania
                        label="🔊 Pobierz Audio MP3",  # Etykieta
                        data=plik_audio_podsumowania,  # Dane
                        file_name=f"{st.session_state.nazwa_pliku}_podsumowanie.mp3",  # Nazwa pliku
                        mime="audio/mp3"  # Typ MIME
                    )
    
    # ===== SEKCJA STEP-BY-STEP =====
    st.markdown("---")
    st.markdown("## 🔧 Audio i Transkrypcja")
    st.markdown("---")
    
    # Inicjalizacja zmiennej ścieżki do transkrypcji
    sciezka_do_transkrypcji = None  # Domyślna wartość None
    
    # Sekcja konwersji audio dla plików wideo
    if rozszerzenie in ['.mp4', '.avi', '.mov']:  # Jeśli plik jest wideo
        st.markdown("### 🎵 Ekstrakcja Audio")
        
        if st.button("Wyodrębnij audio z wideo", key="extract_audio", disabled=edycja_aktywna):  # Przycisk do ekstrakcji (wyszarzony gdy edycja aktywna)
            with st.spinner("Wyodrębnianie audio..."):  # Wskaźnik postępu
                try:  # Próba ekstrakcji audio
                    sciezka_audio = wyodrebnij_audio_z_wideo(sciezka_temp)  # Wywołanie funkcji ekstrakcji
                    st.session_state.sciezka_audio = sciezka_audio  # Zapisanie ścieżki w sesji
                    st.success("✅ Audio zostało wyodrębnione pomyślnie!")  # Komunikat sukcesu
                except Exception as e:  # Obsługa błędów
                    st.error(f"❌ Błąd podczas wyodrębniania audio: {str(e)}")  # Wyświetlenie błędu
        
        # Wyświetlanie odtwarzacza i przycisku pobierania jeśli audio zostało wyodrębnione
        if st.session_state.sciezka_audio:  # Sprawdzenie czy audio zostało wyodrębnione
            # Odtwarzacz wyodrębnionego audio
            st.audio(st.session_state.sciezka_audio)  # Wyświetlenie odtwarzacza
            
            # Przycisk do pobrania pliku audio
            with open(st.session_state.sciezka_audio, 'rb') as plik_audio:  # Otwarcie pliku do odczytu binarnego
                st.download_button(  # Przycisk pobierania
                    label="⬇️ Pobierz plik MP3",  # Etykieta przycisku
                    data=plik_audio,  # Dane do pobrania
                    file_name=f"{st.session_state.nazwa_pliku}.mp3",  # Nazwa pliku do pobrania z session_state
                    mime="audio/mp3"  # Typ MIME
                )
        
        # Ustawienie ścieżki do transkrypcji
        sciezka_do_transkrypcji = st.session_state.sciezka_audio if st.session_state.sciezka_audio else sciezka_temp  # Wybór pliku do transkrypcji
    else:  # Jeśli plik jest audio
        sciezka_do_transkrypcji = sciezka_temp  # Użycie oryginalnego pliku
    
    # Sekcja transkrypcji
    st.markdown("### 📝 Transkrypcja")
    
    if st.button("Rozpocznij transkrypcję", key="transcribe", disabled=edycja_aktywna):  # Przycisk rozpoczęcia transkrypcji (wyszarzony gdy edycja aktywna)
        if sciezka_do_transkrypcji:  # Sprawdzenie czy ścieżka istnieje
            with st.spinner("Transkrypcja w toku... To może potrwać kilka minut."):  # Wskaźnik postępu
                try:  # Próba transkrypcji
                    # Otwarcie pliku audio do transkrypcji
                    with open(sciezka_do_transkrypcji, 'rb') as plik_audio:  # Otwarcie pliku
                        # Wywołanie API Whisper z poprawną nazwą pliku
                        odpowiedz = klient.audio.transcriptions.create(
                            model="whisper-1",  # Model do transkrypcji
                            file=(f"{st.session_state.nazwa_pliku}.mp3", plik_audio, "audio/mpeg"),  # Plik audio z nazwą z session_state
                            language="pl"  # Język (polski)
                        )
                        
                        # Zapisanie transkrypcji w sesji
                        st.session_state.transkrypcja = odpowiedz.text  # Zapisanie tekstu transkrypcji
                        st.session_state.transkrypcja_zapisana = True  # Ustawienie flagi zapisu (odblokowuje przyciski generowania)
                        
                        st.success("✅ Transkrypcja zakończona pomyślnie!")  # Komunikat sukcesu
                except Exception as e:  # Obsługa błędów
                    st.error(f"❌ Błąd podczas transkrypcji: {str(e)}")  # Wyświetlenie błędu
        else:  # Jeśli ścieżka nie istnieje
            st.warning("⚠️ Najpierw wyodrębnij audio z wideo")  # Ostrzeżenie
    
    # Wyświetlenie transkrypcji jeśli istnieje
    if st.session_state.transkrypcja:  # Sprawdzenie czy transkrypcja została wygenerowana
        # Pole tekstowe transkrypcji - edytowalne lub tylko do odczytu (renderowane PRZED przyciskami aby zachować wartość)
        if st.session_state.edycja_transkrypcji_aktywna:  # Jeśli edycja jest aktywna
            edytowana_transkrypcja = st.text_area(  # Pole tekstowe edytowalne
                "Transkrypcja:",  # Etykieta
                value=st.session_state.transkrypcja,  # Treść transkrypcji
                height=300,  # Wysokość pola
                key="transcription_edit_area"  # Unikalny klucz
            )
            # Zapisanie zmian w zmiennej tymczasowej (aby były dostępne dla przycisku "Zapisz zmiany")
            st.session_state.edytowana_transkrypcja_temp = edytowana_transkrypcja  # Zapis w zmiennej tymczasowej
        else:  # Jeśli edycja nie jest aktywna (tylko do odczytu)
            st.text_area(  # Pole tekstowe tylko do odczytu
                "Transkrypcja:",  # Etykieta
                value=st.session_state.transkrypcja,  # Treść transkrypcji
                height=300,  # Wysokość pola
                disabled=True,  # Pole wyłączone (tylko do odczytu)
                key="transcription_readonly_area"  # Unikalny klucz
            )
        
        # Przyciski kontroli edycji transkrypcji
        col_edit1, col_edit2, col_edit3 = st.columns([1, 1, 3])  # Trzy kolumny dla przycisków edycji
        
        with col_edit1:  # Pierwsza kolumna - przycisk Edycja
            if st.button("✏️ Edycja", key="edit_transcript_btn", disabled=st.session_state.edycja_transkrypcji_aktywna or st.session_state.edycja_podsumowania_aktywna):  # Przycisk Edycja (wyszarzony gdy jakakolwiek edycja aktywna)
                st.session_state.edycja_transkrypcji_aktywna = True  # Aktywacja trybu edycji transkrypcji
                st.session_state.transkrypcja_przed_edycja = st.session_state.transkrypcja  # Zapisanie stanu przed edycją
                st.session_state.transkrypcja_zapisana = False  # Wyzerowanie flagi zapisu (przyciski generowania będą wyszarzone dopóki nie zapisze zmian)
                st.rerun()  # Odświeżenie aplikacji
        
        with col_edit2:  # Druga kolumna - przycisk Anuluj edycję
            if st.button("❌ Anuluj edycję", key="cancel_transcript_edit_btn", disabled=not st.session_state.edycja_transkrypcji_aktywna):  # Przycisk Anuluj (aktywny tylko gdy edycja transkrypcji aktywna)
                st.session_state.transkrypcja = st.session_state.transkrypcja_przed_edycja  # Przywrócenie stanu przed edycją
                st.session_state.edycja_transkrypcji_aktywna = False  # Wyłączenie trybu edycji
                st.session_state.transkrypcja_przed_edycja = None  # Wyczyszczenie kopii zapasowej
                st.session_state.edytowana_transkrypcja_temp = None  # Wyczyszczenie zmiennej tymczasowej
                st.rerun()  # Odświeżenie aplikacji
        
        with col_edit3:  # Trzecia kolumna - przycisk Zapisz zmiany
            if st.button("💾 Zapisz zmiany", key="save_transcript_btn", disabled=not st.session_state.edycja_transkrypcji_aktywna):  # Przycisk Zapisz (aktywny tylko gdy edycja transkrypcji aktywna)
                # Zapisanie edytowanej transkrypcji ze zmiennej tymczasowej do głównej zmiennej
                if st.session_state.edytowana_transkrypcja_temp is not None:  # Jeśli zmienna tymczasowa zawiera dane
                    st.session_state.transkrypcja = st.session_state.edytowana_transkrypcja_temp  # Zapisanie zmian
                st.session_state.edycja_transkrypcji_aktywna = False  # Wyłączenie trybu edycji
                st.session_state.transkrypcja_przed_edycja = None  # Wyczyszczenie kopii zapasowej
                st.session_state.edytowana_transkrypcja_temp = None  # Wyczyszczenie zmiennej tymczasowej
                st.session_state.transkrypcja_zapisana = True  # Ustawienie flagi zapisu transkrypcji (odblokowuje przyciski generowania)
                st.success("✅ Zmiany w transkrypcji zostały zapisane!")  # Komunikat sukcesu
                st.rerun()  # Odświeżenie aplikacji
        
        # Przyciski do generowania podsumowania w opcji zaawansowanej
        col1, col2 = st.columns(2)  # Dwie kolumny o równej szerokości
        
        with col1:  # Pierwsza kolumna - opcja tekstowa
            # Przycisk domyślnie wyszarzony dopóki użytkownik nie zapisze edycji transkrypcji (flaga transkrypcja_zapisana musi być True)
            if st.button("📝 Wygeneruj podsumowanie tekstowe", key="advanced_text", use_container_width=True, disabled=(not st.session_state.transkrypcja_zapisana or edycja_aktywna)):  # Przycisk opcji zaawansowanej tekstowej (wyszarzony dopóki nie zapisano zmian lub edycja aktywna)
                st.session_state.tryb_generowania = "tekstowe"  # Ustawienie trybu generowania
                
                with st.spinner("Generowanie podsumowania..."):  # Wskaźnik postępu
                    try:  # Próba generowania podsumowania
                        # Przygotowanie promptu systemowego w zależności od wybranych opcji
                        instrukcja_dlugosc = {  # Słownik z instrukcjami dla różnych długości
                            "Krótkie": "Stwórz krótkie podsumowanie (maksymalnie 3-4 zdania).",  # Instrukcja dla krótkiego
                            "Średnie": "Stwórz średniej długości podsumowanie (5-8 zdań).",  # Instrukcja dla średniego
                            "Długie": "Stwórz szczegółowe, rozbudowane podsumowanie."  # Instrukcja dla długiego
                        }
                        
                        instrukcja_styl = {  # Słownik z instrukcjami dla różnych stylów
                            "Tekstowe": "Przedstaw podsumowanie w formie spójnego tekstu.",  # Instrukcja dla tekstowego
                            "W punktach": "Przedstaw podsumowanie w formie numerowanej listy punktów. Użyj numeracji: 1. ... ; 2. ... ; 3. ... itd."  # Instrukcja dla punktowego z numeracją
                        }
                        
                        # Złożenie pełnego promptu systemowego
                        prompt_systemowy = f"Jesteś asystentem AI specjalizującym się w tworzeniu zwięzłych i treściwych podsumowań. {instrukcja_dlugosc[dlugosc]} {instrukcja_styl[styl]} Stwórz podsumowanie poniższej transkrypcji w języku polskim."  # Pełna instrukcja systemowa
                        
                        # Wywołanie API GPT-4o
                        odpowiedz_gpt = klient.chat.completions.create(
                            model="gpt-4o",  # Model GPT-4o
                            messages=[  # Lista wiadomości
                                {
                                    "role": "system",  # Rola systemowa
                                    "content": prompt_systemowy  # Użycie przygotowanego promptu
                                },
                                {
                                    "role": "user",  # Rola użytkownika
                                    "content": f"Podsumuj następującą transkrypcję:\n\n{st.session_state.transkrypcja}"  # Treść do podsumowania
                                }
                            ],
                            temperature=0.7  # Parametr kreatywności
                        )
                        
                        # Zapisanie podsumowania w sesji
                        st.session_state.podsumowanie = odpowiedz_gpt.choices[0].message.content  # Zapisanie podsumowania
                        st.session_state.podsumowanie_wersja += 1  # Zwiększenie licznika wersji (wymusza odświeżenie widgetu)
                        
                        # Usunięcie audio podsumowania jeśli było wcześniej wygenerowane
                        st.session_state.sciezka_audio_podsumowania = None
                        
                        # Resetowanie flagi zapisu transkrypcji (kolejne edycje będą wymagały ponownego zapisu przed wygenerowaniem podsumowania)
                        st.session_state.transkrypcja_zapisana = False  # Wyłączenie flagi zapisu
                        
                        # Komunikat sukcesu z informacją o długości transkrypcji i podsumowania (do debugowania)
                        st.success(f"✅ Podsumowanie tekstowe wygenerowane pomyślnie! (Transkrypcja: {len(st.session_state.transkrypcja)} znaków, Podsumowanie: {len(st.session_state.podsumowanie)} znaków)")  # Komunikat sukcesu z info
                        st.rerun()  # Odświeżenie aplikacji
                    except Exception as e:  # Obsługa błędów
                        st.error(f"❌ Błąd podczas generowania podsumowania: {str(e)}")  # Wyświetlenie błędu
        
        with col2:  # Druga kolumna - opcja audio
            # Przycisk domyślnie wyszarzony dopóki użytkownik nie zapisze edycji transkrypcji (flaga transkrypcja_zapisana musi być True)
            if st.button("🔊 Wygeneruj podsumowanie audio", key="advanced_audio", use_container_width=True, disabled=(not st.session_state.transkrypcja_zapisana or edycja_aktywna)):  # Przycisk opcji zaawansowanej audio (wyszarzony dopóki nie zapisano zmian lub edycja aktywna)
                st.session_state.tryb_generowania = "audio"  # Ustawienie trybu generowania
                
                with st.spinner("Generowanie podsumowania i audio..."):  # Wskaźnik postępu
                    try:  # Próba generowania podsumowania
                        # Przygotowanie promptu systemowego w zależności od wybranych opcji
                        instrukcja_dlugosc = {  # Słownik z instrukcjami dla różnych długości
                            "Krótkie": "Stwórz krótkie podsumowanie (maksymalnie 3-4 zdania).",
                            "Średnie": "Stwórz średniej długości podsumowanie (5-8 zdań).",
                            "Długie": "Stwórz szczegółowe, rozbudowane podsumowanie."
                        }
                        
                        instrukcja_styl = {  # Słownik z instrukcjami dla różnych stylów
                            "Tekstowe": "Przedstaw podsumowanie w formie spójnego tekstu.",
                            "W punktach": "Przedstaw podsumowanie w formie numerowanej listy punktów. Użyj numeracji: 1. ... ; 2. ... ; 3. ... itd."
                        }
                        
                        # Złożenie pełnego promptu systemowego
                        prompt_systemowy = f"Jesteś asystentem AI specjalizującym się w tworzeniu zwięzłych i treściwych podsumowań. {instrukcja_dlugosc[dlugosc]} {instrukcja_styl[styl]} Stwórz podsumowanie poniższej transkrypcji w języku polskim."
                        
                        # Wywołanie API GPT-4o
                        odpowiedz_gpt = klient.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {
                                    "role": "system",
                                    "content": prompt_systemowy
                                },
                                {
                                    "role": "user",
                                    "content": f"Podsumuj następującą transkrypcję:\n\n{st.session_state.transkrypcja}"
                                }
                            ],
                            temperature=0.7
                        )
                        
                        # Zapisanie podsumowania w sesji
                        st.session_state.podsumowanie = odpowiedz_gpt.choices[0].message.content
                        st.session_state.podsumowanie_wersja += 1  # Zwiększenie licznika wersji (wymusza odświeżenie widgetu)
                        
                        # Generowanie audio z podsumowania (TTS)
                        sciezka_audio_podsumowania = os.path.join(tempfile.gettempdir(), f"{st.session_state.nazwa_pliku}_podsumowanie.mp3")
                        generuj_audio_z_tekstu(klient, st.session_state.podsumowanie, sciezka_audio_podsumowania, glos="onyx")
                        st.session_state.sciezka_audio_podsumowania = sciezka_audio_podsumowania
                        
                        # Resetowanie flagi zapisu transkrypcji (kolejne edycje będą wymagały ponownego zapisu przed wygenerowaniem podsumowania)
                        st.session_state.transkrypcja_zapisana = False  # Wyłączenie flagi zapisu
                        
                        # Komunikat sukcesu z informacją o długości transkrypcji i podsumowania (do debugowania)
                        st.success(f"✅ Podsumowanie audio wygenerowane pomyślnie! (Transkrypcja: {len(st.session_state.transkrypcja)} znaków, Podsumowanie: {len(st.session_state.podsumowanie)} znaków)")  # Komunikat sukcesu z info
                        st.rerun()  # Odświeżenie aplikacji
                    except Exception as e:  # Obsługa błędów
                        st.error(f"❌ Błąd podczas generowania podsumowania: {str(e)}")  # Wyświetlenie błędu
    
    # ===== SEKCJA KOSZTORYSU =====
    # Obliczenie i wyświetlenie kosztów jeśli podsumowanie istnieje
    if st.session_state.podsumowanie:  # Sprawdzenie czy podsumowanie zostało wygenerowane
        # Obliczenie kosztu transkrypcji na podstawie rzeczywistej długości audio
        if st.session_state.dlugosc_audio_minuty:  # Jeśli długość jest znana
            koszt_whisper = oblicz_koszt_transkrypcji(st.session_state.dlugosc_audio_minuty)  # Obliczenie kosztu Whisper
        else:  # Jeśli długość nie jest znana
            koszt_whisper = 0  # Koszt zerowy
        
        # Obliczenie kosztu GPT na podstawie rzeczywistej liczby słów
        liczba_slow_transkrypcji = zlicz_slowa(st.session_state.transkrypcja)  # Zliczenie słów w transkrypcji
        liczba_slow_podsumowania = zlicz_slowa(st.session_state.podsumowanie)  # Zliczenie słów w podsumowaniu
        
        # Szacowanie tokenów (transkrypcja jako input, podsumowanie jako output)
        tokeny_input = szacuj_tokeny_z_slow(liczba_slow_transkrypcji)  # Tokeny wejściowe
        tokeny_output = szacuj_tokeny_z_slow(liczba_slow_podsumowania)  # Tokeny wyjściowe
        
        # Obliczenie kosztu GPT
        koszt_gpt = oblicz_koszt_gpt(tokeny_input, tokeny_output)  # Obliczenie kosztu GPT
        
        # Obliczenie kosztu TTS jeśli tryb to audio
        koszt_tts = 0  # Domyślnie brak kosztu TTS
        if st.session_state.tryb_generowania == "audio" and st.session_state.sciezka_audio_podsumowania:  # Jeśli tryb audio i audio podsumowania istnieje
            liczba_znakow_podsumowania = len(st.session_state.podsumowanie)  # Zliczenie znaków w podsumowaniu
            koszt_tts = oblicz_koszt_tts(liczba_znakow_podsumowania)  # Obliczenie kosztu TTS
        
        # Wyświetlenie kosztów w sidebarze (zawsze gdy podsumowanie istnieje)
        st.sidebar.header("💰 Oszacowanie kosztów")  # Nagłówek sekcji w sidebarze
        dlugosc_dla_tooltipa = formatuj_czas_na_min_sec(st.session_state.dlugosc_audio_minuty)  # Formatowanie długości dla tooltipa na format "X min Y sec"
        st.sidebar.metric(  # Metryka kosztu Whisper
            "Whisper-1 (transkrypcja)",  # Etykieta
            f"${koszt_whisper:.4f}",  # Wartość
            help=f"Długość audio: {dlugosc_dla_tooltipa}"  # Tooltip z długością w formacie X min Y sec
        )
        st.sidebar.metric(  # Metryka kosztu GPT
            "GPT-4o (podsumowanie)",  # Etykieta
            f"${koszt_gpt:.4f}",  # Wartość
            help=f"Tokeny: ~{tokeny_input} in, ~{tokeny_output} out"  # Tooltip
        )
        
        # Wyświetlenie kosztu TTS jeśli tryb audio
        if st.session_state.tryb_generowania == "audio":  # Jeśli tryb audio
            st.sidebar.metric(  # Metryka kosztu TTS
                "TTS-1 (podsumowanie audio)",  # Etykieta
                f"${koszt_tts:.4f}",  # Wartość
                help=f"Znaki: {len(st.session_state.podsumowanie)}"  # Tooltip
            )
            koszt_laczny = koszt_whisper + koszt_gpt + koszt_tts  # Łączny koszt z TTS
        else:  # Jeśli tryb tekstowy
            koszt_laczny = koszt_whisper + koszt_gpt  # Łączny koszt bez TTS
        
        st.sidebar.metric(  # Metryka łącznego kosztu
            "Łączny koszt",  # Etykieta
            f"${koszt_laczny:.4f}"  # Wartość
        )
        st.sidebar.info("ℹ️ **Koszty obliczone na podstawie rzeczywistych danych:**")  # Nagłówek informacji
        st.sidebar.markdown("**Sposób obliczania kosztów:**")  # Nagłówek informacji
        st.sidebar.markdown("• **Whisper-1:** \\$0.006/min (długość audio)")  # Informacja o Whisper
        st.sidebar.markdown("• **GPT-4o:** \\$0.0025/1k tokenów (in), \\$0.01/1k tokenów (out)")  # Informacja o GPT
        if st.session_state.tryb_generowania == "audio":  # Jeśli tryb audio
            st.sidebar.markdown("• **TTS-1:** \\$0.015/1k znaków")  # Informacja o TTS

# Stopka aplikacji
st.markdown("---")  # Linia oddzielająca
st.markdown(  # Tekst stopki
    "💡 **Wskazówka:** Aplikacja wykorzystuje OpenAI Whisper-1 do transkrypcji, GPT-4o do podsumowania treści i TTS-1 do generowania mowy."
)
