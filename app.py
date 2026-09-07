import requests
import streamlit as st
import streamlit.components.v1 as components

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="منصة الخدمات اليومية", page_icon="🌐", layout="centered"
)

st.title("🌐 منصة الخدمات والطقس اليومية")
st.write(
    "تطبيق متكامل لعرض حالة الطقس، مواقيت الصلاة، وأسعار الذهب والعملات المباشرة."
)

# --------------------------------------------------
# 2. أداة أسعار الذهب والعملات المباشرة (TradingView Widget)
# --------------------------------------------------
st.subheader("📈 أسعار الذهب والعملات (تحديث مباشر)")

tradingview_html = """
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-tickers.js" async>
  {
  "symbols": [
    {
      "proName": "OANDA:XAUUSD",
      "title": "الذهب (USD/Oz)"
    },
    {
      "proName": "FX_IDC:USDAED",
      "title": "USD / AED"
    },
    {
      "proName": "FX_IDC:USDSAR",
      "title": "USD / SAR"
    },
    {
      "proName": "BITSTAMP:BTCUSD",
      "title": "البيتكوين (BTC)"
    }
  ],
  "isTransparent": false,
  "showSymbolLogo": true,
  "colorTheme": "dark",
  "locale": "ar"
}
  </script>
</div>
<!-- TradingView Widget END -->
"""
# عرض كود TradingView داخل الصفحة
components.html(tradingview_html, height=90)

st.divider()

# --------------------------------------------------
# 3. اختيار المدينة للطقس ومواقيت الصلاة
# --------------------------------------------------
popular_cities = [
    "Abu Dhabi",
    "Dubai",
    "Riyadh",
    "Cairo",
    "Mecca",
    "Medina",
    "Doha",
    "Kuwait City",
    "Muscat",
    "Manama",
    "Amman",
    "Beirut",
    "London",
    "Paris",
    "New York",
    "Tokyo",
    "Beijing",
    "Istanbul",
]

selected_city = st.selectbox("اختر المدينة لعرض الخدمات:", popular_cities)

# مفتاح OpenWeatherMap API
OPENWEATHER_API_KEY = "4b38f23ed6365644d9bb6b9356992389"

col1, col2 = st.columns(2)

# --- القسم الأول: الطقس ---
with col1:
    st.markdown("### 🌤️ حالة الطقس")
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ar"

    try:
        w_res = requests.get(weather_url)
        if w_res.status_code == 200:
            w_data = w_res.json()
            st.metric("درجة الحرارة", f"{w_data['main']['temp']} °C")
            st.write(f"**الحالة:** {w_data['weather'][0]['description']}")
            st.write(f"**الرطوبة:** {w_data['main']['humidity']}%")
            st.write(f"**سرعة الرياح:** {w_data['wind']['speed']} م/ث")
        else:
            st.error("عذراً، تعذر جلب بيانات الطقس.")
    except Exception as e:
        st.error(f"خطأ بالاتصال: {e}")

# --- القسم الثاني: مواقيت الصلاة (Aladhan API) ---
with col2:
    st.markdown("### 🕌 مواقيت الصلاة")
    prayer_url = f"https://api.aladhan.com/v1/timingsByCity?city={selected_city}&country=&method=4"

    try:
        p_res = requests.get(prayer_url)
        if p_res.status_code == 200:
            p_data = p_res.json()["data"]["timings"]
            st.write(f"**الفجر:** {p_data['Fajr']}")
            st.write(f"**الشروق:** {p_data['Sunrise']}")
            st.write(f"**الظهر:** {p_data['Dhuhr']}")
            st.write(f"**العصر:** {p_data['Asr']}")
            st.write(f"**المغرب:** {p_data['Maghrib']}")
            st.write(f"**العشاء:** {p_data['Isha']}")
        else:
            st.error("تعذر جلب مواقيت الصلاة.")
    except Exception as e:
        st.error(f"خطأ بالاتصال: {e}")
