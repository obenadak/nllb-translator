import gradio as gr
from transformers import pipeline
import gc
import torch

# --- MODEL VE DİL TANIMLAMALARI ---
MODEL_NAME = "facebook/nllb-200-distilled-600M"
LANGUAGES_NLLB = {
    "Türkçe": "tur_Latn",
    "English": "eng_Latn",
    "Español": "spa_Latn",
}
UI_LANGUAGES = sorted(list(LANGUAGES_NLLB.keys()))
translator_pipeline = None

# --- ANA FONKSİYONLAR ---

def initialize_translator():
    """Uygulama yüklendiğinde çeviri modelini bir kereliğine yükler."""
    global translator_pipeline
    if translator_pipeline is None:
        try:
            yield "<p>⏳ Çeviri motoru (NLLB-200) hazırlanıyor...</p>", gr.Button(interactive=False)
            # Performans için GPU varsa onu kullan, yoksa CPU kullan
            device = 0 if torch.cuda.is_available() else -1
            translator_pipeline = pipeline(
                'translation', 
                model=MODEL_NAME, 
                device=device
            )
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            yield "<p style='color:#4ade80;'>✅ Çeviri motoru hazır.</p>", gr.Button(interactive=True)
        except Exception as e:
            yield f"<p style='color:#f87171;'>❌ HATA: Model yüklenemedi: {e}</p>", gr.Button(interactive=False)
    else:
        yield "<p style='color:#4ade80;'>✅ Çeviri zaten hazır.</p>", gr.Button(interactive=True)

def translate_text(text, source_lang_ui, target_lang_ui):
    """Verilen metni kaynak dilden hedef dile çevirir."""
    global translator_pipeline
    if translator_pipeline is None:
        gr.Error("Çeviri motoru hazır değil.")
        return ""
    if not text.strip():
        return ""
    if source_lang_ui == target_lang_ui:
        return text
    source_lang_code = LANGUAGES_NLLB[source_lang_ui]
    target_lang_code = LANGUAGES_NLLB[target_lang_ui]
    try:
        result = translator_pipeline(text, src_lang=source_lang_code, tgt_lang=target_lang_code)
        return result[0]['translation_text']
    except Exception as e:
        gr.Error(f"Çeviri sırasında bir hata oluştu: {e}")
        return ""

def swap_languages_and_text(src_lang, tgt_lang, src_text, tgt_text):
    """Dilleri ve metin kutularının içeriğini değiştirir."""
    return tgt_lang, src_lang, tgt_text, src_text

def clear_all():
    """Metin kutularını temizler."""
    return "", ""

# --- ARAYÜZ TASARIMI ---

css = """
#main-container { max-width: 950px; margin: auto; padding: 1.5rem 1rem; }
#main-title { text-align: center; font-weight: 600; font-size: 2rem; margin-bottom: 0.5rem; }
#status-box { text-align: center; min-height: 24px; }
#status-box p { margin: 0; font-size: 0.9rem; }
#translator-area { align-items: stretch; margin: 1.5rem 0; gap: 1rem; }
.lang-column { display: flex; flex-direction: column; gap: 0.75rem; }
#swap-column { display:flex; align-items: center; justify-content: center; }
#action-buttons { justify-content: center; gap: 1rem; }
#swap-button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.5rem !important;
    color: #6b7280;
    transition: all 0.2s;
    margin: auto;
    min-width: 40px;
    max-width: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}
#swap-button:hover {
    color: #d1d5db !important;
    background: rgba(255,255,255,0.1) !important;
}

#swap-button::before {
    content: '';
    display: inline-block;
    width: 1.5rem;
    height: 1.5rem;
    background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M17 1l4 4-4 4"/><path d="M21 5H9"/><path d="M7 23l-4-4 4-4"/><path d="M3 19h12"/></svg>') no-repeat center center;
    background-size: contain;
}
"""


theme = gr.themes.Default(primary_hue="blue").set(
    body_background_fill_dark="#111827",
    block_background_fill_dark="#1f2937",
    block_border_width="0px",
    block_shadow="*shadow_drop_lg",
    block_label_background_fill_dark="#1f2937",
    button_primary_background_fill_dark="*primary_500",
    button_primary_background_fill_hover_dark="*primary_600",
    button_secondary_background_fill_dark="#374151",
    button_secondary_background_fill_hover_dark="#4b5563"
)

with gr.Blocks(theme=theme, css=css, analytics_enabled=False) as iface:
    with gr.Column(elem_id="main-container"):
        gr.Markdown("<h1 id='main-title'>Çeviri Asistanı</h1>")
        status_display = gr.HTML(elem_id="status-box")

        with gr.Row(elem_id="translator-area"):
            with gr.Column(scale=10, elem_classes="lang-column"):
                source_lang_dd = gr.Dropdown(UI_LANGUAGES, label="Kaynak Dil", value="Türkçe")
                source_text_tb = gr.Textbox(lines=10, placeholder="Çevrilecek metin...", show_label=False)

            with gr.Column(scale=1, elem_id="swap-column", min_width=60):
                swap_button = gr.Button(value="", elem_id="swap-button")

            with gr.Column(scale=10, elem_classes="lang-column"):
                target_lang_dd = gr.Dropdown(UI_LANGUAGES, label="Hedef Dil", value="English")
                target_text_tb = gr.Textbox(lines=10, interactive=False, show_label=False)

        with gr.Row(elem_id="action-buttons"):
            clear_button = gr.Button("Temizle", variant="secondary")
            translate_button = gr.Button("Çevir", variant="primary", size="lg")

    # --- OLAYLARI BAĞLAMA ---
    iface.load(fn=initialize_translator, outputs=[status_display, translate_button])

    translate_button.click(
        fn=translate_text,
        inputs=[source_text_tb, source_lang_dd, target_lang_dd],
        outputs=target_text_tb
    )

    swap_button.click(
        fn=swap_languages_and_text,
        inputs=[source_lang_dd, target_lang_dd, source_text_tb, target_text_tb],
        outputs=[source_lang_dd, target_lang_dd, source_text_tb, target_text_tb]
    )

    source_lang_dd.select(
        fn=translate_text,
        inputs=[source_text_tb, source_lang_dd, target_lang_dd],
        outputs=target_text_tb
    )
    target_lang_dd.select(
        fn=translate_text,
        inputs=[source_text_tb, source_lang_dd, target_lang_dd],
        outputs=target_text_tb
    )

    clear_button.click(
        fn=clear_all,
        outputs=[source_text_tb, target_text_tb]
    )

# Uygulamayı başlat
iface.queue().launch()