# Graphical Scratch-style Translator
# Install required libraries first:
#   pip3 install deep-translator gtts SpeechRecognition --break-system-packages
#   sudo apt install mpg123 python3-pyaudio portaudio19-dev python3-tk

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import tempfile
import os

# ── Language data ────────────────────────────────────────────────────────────

LANGUAGES = {
    "English": "en",
    "Arabic":     "ar",
    "Belarusian": "be",
    "Chinese (Simplified)":    "zh-CN",
    "Dutch":      "nl",
    "Chinese (Traditional)": "zh-TW",
    "French":     "fr",
    "German":     "de",
    "Greek":      "el",
    "Hindi":      "hi",
    "Italian":    "it",
    "Japanese":   "ja",
    "Korean":     "ko",
    "Polish":     "pl",
    "Portuguese": "pt",
    "Russian":    "ru",
    "Spanish":    "es",
    "Swedish":    "sv",
    "Turkish":    "tr",
    "Ukrainian":  "uk",
    "Vietnamese": "vi",
    "Romanian": "ro",
    "Scottish Gaelic": "gd",
    "Scottish": "gd",
    "Malay": "ms",
    "Indonesian": "id",
    "Indo": "id",
    "Thai": "th",
    "Hebrew": "he",
    "Persian": "fa",
    "Farsi": "fa",
    "Bengali": "bn",
    "Tamil": "ta",
    "Urdu": "ur",
    "Swahili" : "sw",
   "Filipino": "tl",
    "Tagalog": "tl",
   "Croatian": "hr",
   "Czech": "cs",
   "Slovak": "sk",
   "Finnish": "fi",
   "Danish" : "da",
   "Norwegian": "no",
   "Bulgarian": "bg",
   "Serbian": "sr",
   "Catalan": "ca",
}

# Languages gTTS doesn't support
NO_TTS = {"be", "gd", "la"}

# ── Colours & fonts ──────────────────────────────────────────────────────────

BG        = "#0f1117"
PANEL     = "#1a1d27"
ACCENT    = "#4f8ef7"
ACCENT2   = "#a259ff"
TEXT      = "#e8eaf0"
SUBTEXT   = "#7b8099"
SUCCESS   = "#3ddba0"
ERROR     = "#ff5f6d"
BORDER    = "#2a2d3e"

FONT_TITLE  = ("Georgia", 22, "bold")
FONT_LABEL  = ("Georgia", 10)
FONT_INPUT  = ("Courier", 13)
FONT_BTN    = ("Georgia", 11, "bold")
FONT_SMALL  = ("Georgia", 9)

# ── Helper functions ─────────────────────────────────────────────────────────

def speak(text, lang_code):
    if lang_code in NO_TTS:
        return False
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang_code)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp = f.name
        tts.save(tmp)
        os.system(f"mpg123 -q {tmp}")
        os.remove(tmp)
        return True
    except Exception:
        return False

def do_translate(text, lang_name):
    from deep_translator import GoogleTranslator
    code = LANGUAGES[lang_name]
    return GoogleTranslator(source="auto", target=code).translate(text), code

def do_listen():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=6)
    return r.recognize_google(audio)

# ── Main App ─────────────────────────────────────────────────────────────────

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Translator")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.geometry("680x560")

        self._build_ui()

    def _build_ui(self):
        # ── Title bar ──
        title_frame = tk.Frame(self.root, bg=BG)
        title_frame.pack(fill="x", padx=30, pady=(24, 0))

        tk.Label(title_frame, text="✦ Translator", font=FONT_TITLE,
                 bg=BG, fg=TEXT).pack(side="left")

        tk.Label(title_frame, text="powered by Google",
                 font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(side="left", padx=(10,0), pady=(8,0))

        # ── Input panel ──
        in_frame = tk.Frame(self.root, bg=PANEL, bd=0, highlightthickness=1,
                            highlightbackground=BORDER)
        in_frame.pack(fill="x", padx=30, pady=(18, 0))

        tk.Label(in_frame, text="TEXT TO TRANSLATE", font=FONT_SMALL,
                 bg=PANEL, fg=SUBTEXT).pack(anchor="w", padx=14, pady=(10,2))

        self.input_box = tk.Text(in_frame, height=4, font=FONT_INPUT,
                                 bg=PANEL, fg=TEXT, insertbackground=ACCENT,
                                 relief="flat", padx=12, pady=8,
                                 wrap="word", bd=0)
        self.input_box.pack(fill="x", padx=4, pady=(0,4))
        self.input_box.bind("<Control-Return>", lambda e: self._translate())

        # ── Controls row ──
        ctrl = tk.Frame(self.root, bg=BG)
        ctrl.pack(fill="x", padx=30, pady=(14, 0))

        # Language dropdown
        tk.Label(ctrl, text="LANGUAGE", font=FONT_SMALL,
                 bg=BG, fg=SUBTEXT).pack(side="left")

        self.lang_var = tk.StringVar(value="Spanish")
        lang_menu = ttk.Combobox(ctrl, textvariable=self.lang_var,
                                 values=sorted(LANGUAGES.keys()),
                                 state="readonly", width=16,
                                 font=FONT_LABEL)
        lang_menu.pack(side="left", padx=(8, 20))

        # Style the combobox
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=PANEL,
                        background=PANEL,
                        foreground=TEXT,
                        selectbackground=ACCENT,
                        selectforeground=TEXT,
                        bordercolor=BORDER,
                        arrowcolor=ACCENT)

        # Buttons
        self.translate_btn = tk.Button(ctrl, text="Translate  →",
                                       font=FONT_BTN, bg=ACCENT, fg="white",
                                       relief="flat", padx=18, pady=7,
                                       cursor="hand2",
                                       activebackground=ACCENT2,
                                       activeforeground="white",
                                       command=self._translate)
        self.translate_btn.pack(side="left")

        self.mic_btn = tk.Button(ctrl, text="🎤 Dictate",
                                 font=FONT_BTN, bg=PANEL, fg=TEXT,
                                 relief="flat", padx=14, pady=7,
                                 cursor="hand2",
                                 highlightthickness=1,
                                 highlightbackground=BORDER,
                                 activebackground=BORDER,
                                 activeforeground=TEXT,
                                 command=self._dictate)
        self.mic_btn.pack(side="left", padx=(10,0))

        # ── Output panel ──
        out_frame = tk.Frame(self.root, bg=PANEL, bd=0, highlightthickness=1,
                             highlightbackground=BORDER)
        out_frame.pack(fill="both", expand=True, padx=30, pady=(18, 0))

        out_top = tk.Frame(out_frame, bg=PANEL)
        out_top.pack(fill="x", padx=14, pady=(10, 2))

        tk.Label(out_top, text="TRANSLATION", font=FONT_SMALL,
                 bg=PANEL, fg=SUBTEXT).pack(side="left")

        self.speak_btn = tk.Button(out_top, text="🔊 Speak",
                                   font=FONT_SMALL, bg=PANEL, fg=ACCENT,
                                   relief="flat", cursor="hand2",
                                   activebackground=PANEL,
                                   activeforeground=ACCENT2,
                                   command=self._speak_result)
        self.speak_btn.pack(side="right")

        self.output_box = tk.Text(out_frame, height=6, font=FONT_INPUT,
                                  bg=PANEL, fg=SUCCESS, insertbackground=ACCENT,
                                  relief="flat", padx=12, pady=8,
                                  wrap="word", bd=0, state="disabled")
        self.output_box.pack(fill="both", expand=True, padx=4, pady=(0,4))

        # ── Status bar ──
        self.status_var = tk.StringVar(value="Ready  ✦")
        tk.Label(self.root, textvariable=self.status_var, font=FONT_SMALL,
                 bg=BG, fg=SUBTEXT).pack(anchor="w", padx=30, pady=(10, 16))

        self._last_code = None

    # ── Actions ──────────────────────────────────────────────────────────────

    def _set_output(self, text, color=None):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        if color:
            self.output_box.configure(fg=color)
        self.output_box.configure(state="disabled")

    def _translate(self):
        text = self.input_box.get("1.0", "end").strip()
        if not text:
            self.status_var.set("⚠  Please enter some text first.")
            return
        lang = self.lang_var.get()
        self.status_var.set(f"Translating to {lang}...")
        self.translate_btn.configure(state="disabled")

        def run():
            try:
                result, code = do_translate(text, lang)
                self._last_code = code
                self._last_result = result
                self._set_output(result, SUCCESS)
                self.status_var.set(f"✓  Translated to {lang}")
                # Auto-speak
                if code not in NO_TTS:
                    threading.Thread(target=speak, args=(result, code), daemon=True).start()
                else:
                    self.status_var.set(f"✓  Translated to {lang}  (TTS not available)")
            except Exception as e:
                self._set_output(str(e), ERROR)
                self.status_var.set("✗  Translation failed.")
            finally:
                self.translate_btn.configure(state="normal")

        threading.Thread(target=run, daemon=True).start()

    def _speak_result(self):
        if not hasattr(self, "_last_result") or not self._last_result:
            return
        if self._last_code in NO_TTS:
            self.status_var.set("⚠  TTS not available for this language.")
            return
        self.status_var.set("🔊 Speaking...")
        threading.Thread(target=speak, args=(self._last_result, self._last_code), daemon=True).start()

    def _dictate(self):
        self.status_var.set("🎤 Listening... speak now!")
        self.mic_btn.configure(state="disabled", text="🎤 Listening...")

        def run():
            try:
                text = do_listen()
                self.input_box.delete("1.0", "end")
                self.input_box.insert("1.0", text)
                self.status_var.set(f"✓  Heard: {text}")
            except Exception as e:
                self.status_var.set(f"✗  Dictation failed: {e}")
            finally:
                self.mic_btn.configure(state="normal", text="🎤 Dictate")

        threading.Thread(target=run, daemon=True).start()

# ── Run ───────────────────────────────────────────────────────────────────────

root = tk.Tk()
app = TranslatorApp(root)
root.mainloop()