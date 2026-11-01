import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai
import datetime

# 1. Configurazione della pagina
st.set_page_config(
    page_title="AI Political Marketing Suite",
    page_icon="🏛️",
    layout="wide"
)

# 2. CSS personalizzato per la piena compatibilità Mobile / Tablet / Desktop (Responsive Design)
st.markdown("""
    <style>
    /* Ottimizzazione generale dei contenitori per schermi piccoli */
    @media (max-width: 768px) {
        .stColumns {
            display: flex;
            flex-direction: column !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 1rem;
        }
    }

    /* Riduzione dei margini superiori su mobile per ottimizzare lo spazio */
    div.block-container {
        padding-top: 1.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Adattamento dei pulsanti a tutta larghezza sui piccoli schermi */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }

    /* Miglioramento della leggibilità delle schede Tab su mobile */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Inizializzazione dello session_state per il registro delle sessioni
if 'session_history' not in st.session_state:
    st.session_state['session_history'] = []

# 3. Lettura sicura della chiave dai secrets di Streamlit (Cloud o locale)
default_api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        default_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# 4. Barra Laterale (Sidebar) per la configurazione dell'API Key e Storico Sessioni
with st.sidebar:
    st.header("⚙️ Configurazione IA")

    # Controllo di debug visivo per i secrets
    if default_api_key:
        st.success("🔒 Chiave rilevata nei Secrets di Streamlit!")
    else:
        st.info("💡 Nessun secret rilevato. Inserisci la chiave manualmente o configurala su Streamlit Cloud.")

    api_key = st.text_input(
        "Inserisci Gemini API Key:",
        value=default_api_key,
        type="password",
        key="gemini_political_key",
        help="Caricata automaticamente da secrets.toml / Streamlit Cloud o inseribile manualmente."
    )

    st.markdown("---")
    if api_key:
        st.success("🟢 API Key attiva: Pronto per la campagna.")
    else:
        st.error("🔴 Inserisci o configura una chiave API valida per attivare gli strumenti IA.")

    st.markdown("---")
    st.header("🗂️ Storico Sessioni")
    active_count = len(st.session_state['session_history'])
    st.metric("Interazioni Salvate", active_count)

    if active_count > 0:
        md_export = "# 🏛️ Registro Sessioni - AI Political Marketing Suite\n\n"
        for idx, item in enumerate(st.session_state['session_history'], 1):
            md_export += f"## Sessione #{idx} - {item['type']}\n"
            md_export += f"**Timestamp:** {item['timestamp']}\n\n"
            md_export += f"**Input / Tema:** {item['input']}\n\n"
            md_export += f"**Output Generato:**\n{item['output']}\n\n---\n\n"

        st.download_button(
            label="📥 Scarica Storico (.md)",
            data=md_export,
            file_name=f"report_sessioni_politiche_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

        if st.button("🗑️ Pulisci Storico", use_container_width=True):
            st.session_state['session_history'] = []
            st.rerun()

    st.markdown("---")
    st.markdown("### 📌 Informazioni")
    st.markdown("Suite strategica per la comunicazione politica, l'analisi dell'elettorato e la preparazione ai dibattiti basata su Google Gemini 3.8 Flash.")

# 5. Funzioni di chiamata alle API di Gemini e di log
def call_gemini(prompt, system_instruction=""):
    """Funzione centralizzata per interrogare Gemini 3.8 Flash."""
    # Usa la chiave attiva (dalla sidebar o dai secrets)
    current_key = api_key or default_api_key

    if not current_key:
        return "⚠️ Errore: Inserisci la tua Gemini API Key (o configurala nei secrets) per generare i contenuti."

    try:
        client = genai.Client(api_key=current_key)

        config = {}
        if system_instruction:
            config['system_instruction'] = system_instruction

        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config=config if config else None
        )
        return response.text
    except Exception as e:
        return f"⚠️ Errore durante la chiamata a Google Gemini: {str(e)}"

def log_session(session_type, input_text, output_text):
    """Registra l'interazione nello session_state."""
    st.session_state['session_history'].append({
        "type": session_type,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input": input_text,
        "output": output_text
    })

# 6. Header Principale
st.title("🏛️ AI Political Marketing Suite")
st.markdown("Strumenti avanzati di comunicazione strategica, analisi dell'elettorato e preparazione del candidato.")

# 7. Organizzazione in Tab dei 4 Moduli
tab1, tab2, tab3, tab4 = st.tabs([
    "🎙️ Speechwriter",
    "⚔️ Dibattiti",
    "📊 Sentiment",
    "🎯 Slogan"
])

# --- TAB 1: SPEECHWRITER & SOCIAL POST ---
with tab1:
    st.header("🎙️ Generatore di Discorsi e Post Social")
    st.markdown("Crea messaggi mirati calibrati sul target di elettori e sul tono di voce desiderato.")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Tema principale del messaggio:", placeholder="Es. Transizione ecologica e incentivi per le PMI")
        target_audience = st.selectbox("Elettorato Target:", ["Giovani / Studenti", "Imprenditori / Partite IVA", "Famiglie", "Pensionati", "Elettorato Indeciso / Generale"])
    with col2:
        content_type = st.selectbox("Formato del Contenuto:", ["Post per Instagram / Facebook", "Comunicato Stampa", "Discorso di Piazza (2 minuti)", "Punto programmatico sintetico"])
        tone = st.selectbox("Tono di Voce:", ["Ispirazionale & Visionario", "Pragmatico & Concreto", "Battagliero & Determinato", "Empatico & Rassicurante"])

    if st.button("🚀 Genera Messaggio", use_container_width=True):
        if not topic:
            st.warning("Inserisci un tema principale.")
        else:
            system_prompt = "Sei un senior political speechwriter ed esperto di comunicazione strategica ed elettorale."
            user_prompt = f"""
            Scrivi un {content_type} sul tema: '{topic}'.
            Il messaggio è rivolto a: {target_audience}.
            Il tono da utilizzare deve essere: {tone}.
            Rendilo persuasivo, chiaro e strutturato in modo professionale per la campagna elettorale.
            """
            with st.spinner("Generazione del messaggio in corso..."):
                result = call_gemini(user_prompt, system_prompt)
                st.subheader("Risultato Generato:")
                st.markdown(result)
                log_session(f"Speechwriter ({content_type})", topic, result)

# --- TAB 2: SIMULATORE DI DIBATTITI ---
with tab2:
    st.header("⚔️ Simulatore di Dibattiti e Q&A Trainer")
    st.markdown("Mettiti alla prova: l'IA interpreterà un giornalista aggressivo o un avversario politico che ti mette in difficoltà sui punti deboli.")

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        candidate_stance = st.text_input("La tua posizione sul tema caldo:", placeholder="Es. Favorevole alla costruzione del termovalorizzatore")
    with col_q2:
        interviewer_style = st.selectbox("Profilo dell'Intervistatore:", ["Giornalista d'inchiesta ostile", "Avversario politico polemico", "Cittadino scettico e pragmatico"])

    if st.button("🎤 Mettimi alla prova (Genera Domanda Scomoda)", use_container_width=True):
        system_prompt = f"Sei un {interviewer_style} durante un dibattito televisivo di primissima serata."
        user_prompt = f"""
        Il candidato sostiene questa posizione: '{candidate_stance}'.
        Fagli una domanda diretta, pungente e difficile, che metta in luce le possibili criticità o contraddizioni di questa scelta, costringendolo a giustificarsi.
        """
        with st.spinner("L'intervistatore sta preparando la domanda..."):
            question = call_gemini(user_prompt, system_prompt)
            st.session_state['current_question'] = question

    if 'current_question' in st.session_state:
        st.markdown("---")
        st.error(f"**Domanda dell'Intervistatore:** {st.session_state['current_question']}")

        user_reply = st.text_area("La tua risposta (come candidato):", placeholder="Scrivi qui la tua replica...")
        if st.button("⚖️ Valuta la mia risposta"):
            if not user_reply:
                st.warning("Scrivi prima la tua risposta.")
            else:
                eval_prompt = f"""
                Valuta la risposta del candidato alla domanda scomoda.
                Domanda: {st.session_state['current_question']}
                Risposta del candidato: {user_reply}

                Fai un'analisi costruttiva:
                1. Efficacia persuasiva (da 1 a 10)
                2. Punti di forza della risposta
                3. Eventuali rischi o falle retoriche sfruttate dagli avversari
                4. Suggerimento su come migliorarla.
                """
                with st.spinner("Analisi della performance in corso..."):
                    feedback = call_gemini(eval_prompt, "Sei un coach di comunicazione politica ed ex spin doctor.")
                    st.success("### 📋 Valutazione dello Spin Doctor")
                    st.markdown(feedback)
                    log_session("Simulatore Dibattito", st.session_state['current_question'], feedback)

# --- TAB 3: SENTIMENT ELETTORALE ---
with tab3:
    st.header("📊 Analisi del Sentiment e Temi dell'Elettorato")
    st.markdown("Incolla un blocco di commenti raccolti sui social o opinioni dei cittadini per estrarre le priorità e il sentiment.")

    sample_comments = """Non se ne può più delle buche in città, nessuno fa niente!\nIl nuovo piano trasporti mi sembra un'ottima idea per i giovani.\nTasse troppo alte, le imprese locali stanno morendo.\nFinalmente un candidato che parla chiaro di sicurezza e lavoro."""

    comments_input = st.text_area("Inserisci i commenti dei cittadini (uno per riga):", value=sample_comments, height=150)

    if st.button("📈 Analizza Commenti e Priorità", use_container_width=True):
        if not comments_input:
            st.warning("Inserisci dei testi da analizzare.")
        else:
            system_prompt = "Sei un data analyst esperto in sondaggi politici e social listening."
            prompt = f"""
            Analizza i seguenti commenti dei cittadini:
            {comments_input}

            Estrai:
            1. I 3 temi o problemi più sentiti dall'elettorato.
            2. La percentuale stimata di Sentiment (Positivo, Neutro, Negativo).
            3. Un consiglio strategico su quale tema dovrebbe puntare il candidato per conquistare questi elettori.
            """
            with st.spinner("Analisi dei dati in corso..."):
                analysis_result = call_gemini(prompt, system_prompt)
                st.markdown(analysis_result)
                log_session("Analisi Sentiment", "Analisi batch commenti", analysis_result)

# --- TAB 4: CREATORE DI SLOGAN ---
with tab4:
    st.header("🎯 Generatore di Slogan ed Efficacia della Campagna")
    st.markdown("Sintetizza i valori del tuo programma in slogan brevi, incisivi e memorabili per manifesti e social.")

    core_values = st.text_input("Valori o obiettivi chiave della campagna:", placeholder="Es. Futuro, lavoro locale, ambiente, rinnovamento")
    slogan_style = st.selectbox("Stile dello Slogan:", ["Emozionale & Identitario", "Breve & Memorabile (stile tormentone)", "Pragmatico & Risolutivo", "Provocatorio & di Rottura"])

    if st.button("✨ Genera Slogan", use_container_width=True):
        if not core_values:
            st.warning("Inserisci i valori chiave.")
        else:
            system_prompt = "Sei un direttore creativo e copywriter di campagne politiche vincenti."
            prompt = f"""
            Genera 5 proposte di slogan politico basate su questi concetti: '{core_values}'.
            Lo stile deve essere: {slogan_style}.
            Per ogni slogan, spiega brevemente il perché funziona e su quale leva psicologica dell'elettore fa leva.
            """
            with st.spinner("Creazione slogan in corso..."):
                slogans = call_gemini(prompt, system_prompt)
                st.markdown(slogans)
                log_session("Generatore Slogan", core_values, slogans)
