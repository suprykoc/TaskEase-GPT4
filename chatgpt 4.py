import requests
import customtkinter as ctk
from tkinter import messagebox

def get_response(prompt):
    url = "https://gpt.sockets.lol/gpt"
    headers = {'Content-Type': 'application/json'}
    data = {
        'model': 'gpt-4o',
        'prompt': prompt,
        'messages': [],
        'markdown': False
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            message = response.json().get("response", {}).get("choices", [{}])[0].get("message", {})
            return message.get("content", "Yanıt bulunamadı.")
        else:
            return f"Hata: {response.status_code} - {response.text}"
    except requests.exceptions.Timeout:
        return "Hata: Zaman aşımı oldu."
    except requests.exceptions.RequestException as e:
        return f"Bağlantı hatası: {e}"

def soru_gonder(event=None):
    soru = giris_alani.get()
    if not soru.strip():
        messagebox.showwarning("Uyarı", "Lütfen bir soru girin!")
        return

    yanit = get_response(soru)

    if "```" in yanit:
        parts = yanit.split("```")
        metin = parts[0].strip()
        kod = parts[1].strip() if len(parts) > 1 else "Kod bulunamadı."
    else:
        metin = yanit
        kod = ""

    metin_alani.delete("0.0", "end")
    kod_alani.delete("0.0", "end")
    metin_alani.insert("0.0", metin)
    if kod:
        kod_alani.insert("0.0", kod)

def kopyala_kod():
    kod = kod_alani.get("0.0", "end").strip()
    if kod:
        app.clipboard_clear()
        app.clipboard_append(kod)
        app.update()
        messagebox.showinfo("Bilgi", "Kod kopyalandı!")
    else:
        messagebox.showwarning("Uyarı", "Kopyalanacak kod bulunamadı.")

def kaydet_yanit():
    yanit = metin_alani.get("0.0", "end").strip()
    kod = kod_alani.get("0.0", "end").strip()
    if not yanit and not kod:
        messagebox.showwarning("Uyarı", "Kaydedilecek veri bulunamadı.")
        return

    with open("yanitlar.txt", "a", encoding="utf-8") as dosya:
        dosya.write("Metin Yanıtı:\n")
        dosya.write(yanit + "\n\n")
        dosya.write("Kod Yanıtı:\n")
        dosya.write(kod + "\n\n")

    messagebox.showinfo("Bilgi", "Yanıt başarıyla kaydedildi!")

def tema_degistir(tema):
    if tema == "Koyu":
        ctk.set_appearance_mode("dark")
    elif tema == "Açık":
        ctk.set_appearance_mode("light")

def hakkinda_ekrani():
    hakkinda_pencere = ctk.CTkToplevel(app)
    hakkinda_pencere.title("Hakkında")
    hakkinda_pencere.geometry("600x400")
    hakkinda_pencere.attributes('-topmost', True)

    ctk.CTkLabel(
        hakkinda_pencere,
        text="ChatGPT 4 - Hakkında",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="cyan",
    ).pack(pady=20)

    bilgi_metni = """
Bu uygulama, OpenAI GPT teknolojisini kullanarak sorularınıza yanıt verir.

Yapımcı: Muhammet Mert Koç
Instagram: @muhammet0.exe
Tasarım: Muhammet Mert Koç

Özellikler:
- Modern UI tasarımı
- Kod kopyalama ve kaydetme
- API tabanlı yanıt sistemi 

İletişim için Instagram hesabımdan ulaşabilirsiniz. 
"""
    bilgi_alani = ctk.CTkTextbox(
        hakkinda_pencere,
        font=ctk.CTkFont(size=14),
        width=550,
        height=250,
        wrap="word",
        state="normal",
    )
    bilgi_alani.insert("0.0", bilgi_metni)
    bilgi_alani.configure(state="disabled")
    bilgi_alani.pack(pady=20)

    ctk.CTkButton(
        hakkinda_pencere,
        text="Kapat",
        command=hakkinda_pencere.destroy,
        font=ctk.CTkFont(size=14),
    ).pack(pady=10)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("850x750")
app.state('zoomed')
app.title("ChatGPT 4")

baslik = ctk.CTkLabel(
    app,
    text="ChatGPT 4\nGeliştirici: Muhammet Mert Koç",
    font=ctk.CTkFont(size=26, weight="bold"),
)
baslik.pack(pady=20)

giris_alani = ctk.CTkEntry(app, width=750, placeholder_text="Sorunuzu buraya yazın", font=ctk.CTkFont(size=16))
giris_alani.pack(pady=10)

buton_cerceve = ctk.CTkFrame(app)
buton_cerceve.pack(pady=10)

gonder_butonu = ctk.CTkButton(
    buton_cerceve,
    text="Sor",
    command=soru_gonder,
    font=ctk.CTkFont(size=16, weight="bold"),
)
gonder_butonu.grid(row=0, column=0, padx=5)

kopyala_butonu = ctk.CTkButton(
    buton_cerceve,
    text="Kodu Kopyala",
    command=kopyala_kod,
    font=ctk.CTkFont(size=16),
)
kopyala_butonu.grid(row=0, column=1, padx=5)

kaydet_butonu = ctk.CTkButton(
    buton_cerceve,
    text="Yanıtları Kaydet",
    command=kaydet_yanit,
    font=ctk.CTkFont(size=16),
)
kaydet_butonu.grid(row=0, column=2, padx=5)

hakkinda_butonu = ctk.CTkButton(
    buton_cerceve,
    text="Hakkında",
    command=hakkinda_ekrani,
    font=ctk.CTkFont(size=16),
)
hakkinda_butonu.grid(row=0, column=3, padx=5)

tema_menusu = ctk.CTkOptionMenu(
    buton_cerceve,
    values=["Koyu", "Açık"],
    command=tema_degistir,
    font=ctk.CTkFont(size=14),
)
tema_menusu.grid(row=0, column=4, padx=5)

metin_label = ctk.CTkLabel(app, text="Metin Yanıtı:", font=ctk.CTkFont(size=16, weight="bold"))
metin_label.pack(pady=5)

metin_alani = ctk.CTkTextbox(app, width=750, height=200, font=ctk.CTkFont(size=14))
metin_alani.pack(pady=10)

kod_label = ctk.CTkLabel(app, text="Kod Yanıtı:", font=ctk.CTkFont(size=16, weight="bold"))
kod_label.pack(pady=5)

kod_alani = ctk.CTkTextbox(app, width=750, height=250, font=ctk.CTkFont(size=14))
kod_alani.pack(pady=10)

imza = ctk.CTkLabel(
    app,
    text="Muhammet Mert Koç",
    font=ctk.CTkFont(size=12, weight="bold"),
    text_color="grey",
)
imza.pack(pady=20)

app.mainloop()
