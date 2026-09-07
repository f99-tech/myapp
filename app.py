import streamlit as st
import requests

st.set_page_config(page_title="تطبيق حالة الطقس", page_icon="🌤️", layout="centered")

st.title("🌤️ تطبيق حالة الطقس")
st.write("اختر مدينة من القائمة أو أدخل اسم أي مدينة يدويًا للحصول على حالة الطقس الحالية.")

API_KEY = "4b38f23ed6365644d9bb6b9356992389"

# قائمة تضم 20 مدينة شهيرة حول العالم والمنطقة
popular_cities = [
    "إدخال يدوياً...",
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
    "Shanghai",
    "Istanbul",
    "Rome"
]

selected_city = st.selectbox("اختر المدينة من القائمة:", popular_cities)

if selected_city == "إدخال يدوياً...":
    city_name = st.text_input("أو أدخل اسم المدينة باللغة الإنجليزية:", "")
else:
    city_name = selected_city

if st.button("عرض حالة الطقس"):
    if city_name.strip():
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=ar"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                
                city = data["name"]
                country = data["sys"]["country"]
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                description = data["weather"][0]["description"]
                wind_speed = data["wind"]["speed"]
                
                st.success(f"حالة الطقس في {city}، {country}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="درجة الحرارة", value=f"{temp} °C", delta=f"الملموسة: {feels_like} °C")
                    st.write(f"**الوصف:** {description}")
                with col2:
                    st.metric(label="الرطوبة", value=f"{humidity} %")
                    st.metric(label="سرعة الرياح", value=f"{wind_speed} م/ث")
                    
            elif response.status_code == 404:
                st.error("لم يتم العثور على المدينة. يرجى التأكد من كتابة الاسم بشكل صحيح.")
            else:
                st.error(f"حدث خطأ أثناء جلب البيانات. رمز الخطأ: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            st.error(f"حدث خطأ في الاتصال بالشبكة: {e}")
    else:
        st.warning("يرجى اختيار أو إدخال اسم المدينة أولاً.")
