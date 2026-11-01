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
    div.block-container {
        padding-top: 1.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Inizializzazione sicura dello session_state per il registro delle sessioni
if 'session_history' not in st.session_state:
    st.session_state['session_history'] = []

# Funzione centralizzata per loggare le sessioni in modo sicuro
def log_session(session_type, input_text, output_text):
    """Aggiunge l'interazione allo storico e forza l'aggiornamento."""
    new_entry = {
        "type": session_type,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input": str(input_text),
        "output": str(output_text)
    }
    st.session_state['session_history'].append(new_entry)

# 4. Recupero sicuro della chiave dai Secrets di Streamlit (Cloud o locale)
secret_key = ""
try:
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        secret_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# 5. Barra Laterale (Sidebar) per la configurazione dell'API Key e Storico Sessioni
with st.sidebar:
    st.header("⚙️ Configurazione IA")

    if secret_key:
        st.success("🔒 Chiave rilevata nei Secrets!")
    else:
        st.info("💡 Inserisci la chiave manualmente.")

    api_key_input = st.text_input(
        "Inserisci Gemini API Key:",
        value=secret_key,
        type="password",
        key="gemini_political_key",
        help="Caricata automaticamente da secrets.toml / Streamlit Cloud o inseribile manualmente."
    )

    st.markdown("---")
    active_api_key = api_key_input if api_key_input else secret_key

    if active_api_key:
        st.success("🟢 API Key attiva.")
    else:
        st.error("🔴 API Key mancante.")

    st.markdown("---")
    st.header("🗂️ Storico Sessioni")

    # Debug rapido per verificare il numero esatto di elementi salvati nello stato
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
    else:
        st.caption("Genera almeno un contenuto nei moduli per abilitare il download dello storico.")

    st.markdown("---")
    st.markdown("### 📌 Informazioni")
    st.markdown("Suite strategica per la comunicazione politica basata su Google Gemini 3.8 Flash.")

# 6. Funzione centralizzata di chiamata alle API di Gemini
def call_gemini(prompt, system_instruction=""):
    """Funzione centralizzata per interrogare Gemini 3.8 Flash."""
    current_key = api_key_input if api_key_input else secret_key

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

# 7. Header Principale
st.title("🏛️ AI Political Marketing Suite")
st.markdown("Strumenti avanzati di comunicazione strategica, analisi dell'elettorato e preparazione del candidato.")

# 8. Organizzazione in Tab dei 4 Moduli
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
        topic = st.text_input("Tema principale del messaggio:", placeholder="Es. Transizione ecologica e incentivi per le PMI", key="speech_topic")
        target_audience = st.selectbox("Elettorato Target:", ["Giovani / Studenti", "Imprenditori / Partite IVA", "Famiglie", "Pensionati", "Elettorato Indeciso / Generale"], key="speech_target")
    with col2:
        content_type = st.selectbox("Formato del Contenuto:", ["Post per Instagram / Facebook", "Comunicato Stampa", "Discorso di Piazza (2 minuti)", "Punto programmatico sintetico"], key="speech_type")
        tone = st.selectbox("Tono di Voce:", ["Ispirazionale & Visionario", "Pragmatico & Concreto", "Battagliero & Determinato", "Empatico & Rassicurante"], key="speech_tone")

    if st.button("🚀 Genera Messaggio", key="btn_speech", use_container_width=True):
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
                # Salvataggio immediato nello stato
                log_session(f"Speechwriter ({content_type})", topic, result)
                st.success("✅ Interazione salvata nello storico!")

# --- TAB 2: SIMULATORE DI DIBATTITI ---
with tab2:
    st.header("⚔️ Simulatore di Dibattiti e Q&A Trainer")
    st.markdown("Mettiti alla prova: l'IA interpreterà un giornalista aggressivo o un avversario politico che ti mette in difficoltà sui punti deboli.")

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        candidate_stance = st.text_input("La tua posizione sul tema caldo:", placeholder="Es. Favorevole alla costruzione del termovalorizzatore", key="deb_stance")
    with col_q2:
        interviewer_style = st.selectbox("Profilo dell'Intervistatore:", ["Giornalista d'inchiesta ostile", "Avversario politico polemico", "Cittadino scettico e pragmatico"], key="deb_style")

    if st.button("🎤 Mettimi alla prova (Genera Domanda Scomoda)", key="btn_deb_gen", use_container_width=True):
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

        user_reply = st.text_area("La tua risposta (come candidato):", placeholder="Scrivi qui la tua replica...", key="deb_reply")
        if st.button("⚖️ Valuta la mia risposta", key="btn_deb_eval"):
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
                    st.success("✅ Interazione salvata nello storico!")

# --- TAB 3: SENTIMENT ELETTORALE ---
with tab3:
    st.header("📊 Analisi del Sentiment e Temi dell'Elettorato")
    st.markdown("Incolla un blocco di commenti raccolti sui social o opinioni dei cittadini per estrarre le priorità e il sentiment.")

    sample_comments = """Non se ne può più delle buche in città, nessuno fa niente!\nIl nuovo piano trasporti mi sembra un'ottima idea per i giovani.\nTasse troppo alte, le imprese locali stanno morte.\nFinalmente un candidato che parla chiaro di sicurezza e lavoro."""

    comments_input = st.text_area("Inserisci i commenti dei cittadini (uno per riga):", value=sample_comments, height=150, key="sent_input")

    if st.button("📈 Analizza Commenti e Priorità", key="btn_sent", use_container_width=True):
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
                st.success("✅ Interazione salvata nello storico!")

# --- TAB 4: CREATORE DI SLOGAN ---
with tab4:
    st.header("🎯 Generatore di Slogan ed Efficacia della Campagna")
    st.markdown("Sintetizza i valori del tuo programma in slogan brevi, incisivi e memorabili per manifesti e social.")

    core_values = st.text_input("Valori o obiettivi chiave della campagna:", placeholder="Es. Futuro, lavoro locale, ambiente, rinnovamento", key="slogan_values")
    slogan_style = st.selectbox("Stile dello Slogan:", ["Emozionale & Identitario", "Breve & Memorabile (stile tormentone)", "Pragmatico & Risolutivo", "Provocatorio & di Rottura"], key="slogan_style")

    if st.button("✨ Genera Slogan", key="btn_slogan", use_container_width=True):
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
                st.success("✅ Interazione salvata nello storico!")
