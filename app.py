import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Asistan Esra - Ümran Diş", page_icon="🦷")

# Başlık ve Görselleştirme
st.title("🦷 Asistan Esra")
st.markdown("### Ümran Diş Namık Kemal Şubesi")
st.write("---")

# API Anahtarı Kontrolü
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Lütfen Streamlit Secrets ayarlarından API anahtarını girin!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Esra'nın Kişilik Tanımı
SYSTEM_PROMPT = """
Sen Ümran Diş Hastanesi Namık Kemal şubesinde çalışan, profesyonel ve güler yüzlü Ağız ve Diş Sağlığı Teknikeri Esra'sın. 
Meslektaşların: Emir, Emirhan, Mustafa, Tuğba ve İrem. 
Sınırlar: Teşhis koyamazsın, sadece bilgi verip randevuya yönlendirirsin.
"""

# Sohbet Geçmişini Sakla
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski Mesajları Ekrana Bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Size nasıl yardımcı olabilirim?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini 2.5 Flash Modelini Çağırıyoruz
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Yanıt oluşturma
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nKullanıcı: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Sistem şu an yoğun olabilir. Hata: {str(e)}")
