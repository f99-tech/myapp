import requests
import streamlit as st

st.set_page_config(
    page_title="حاسبة الزكاة الذكية", page_icon="💰", layout="wide"
)

# --------------------------------------------------
# 1. الشريط الجانبي (Sidebar) - طقس وصلاة
# --------------------------------------------------
with st.sidebar:
    st.header("📌 خدمات سريعة")

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
    ]
    selected_city = st.selectbox("اختر المدينة:", popular_cities)

    OPENWEATHER_API_KEY = "4b38f23ed6365644d9bb6b9356992389"

    # الطقس
    st.subheader("🌤️ الطقس")
    try:
        w_res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ar",
            timeout=4,
        )
        if w_res.status_code == 200:
            w_data = w_res.json()
            st.metric("الحرارة", f"{w_data['main']['temp']} °C")
            st.caption(f"الحالة: {w_data['weather'][0]['description']}")
    except:
        st.write("تعذر جلب الطقس")

    st.divider()

    # مواقيت الصلاة
    st.subheader("🕌 مواقيت الصلاة")
    try:
        p_res = requests.get(
            f"https://api.aladhan.com/v1/timingsByCity?city={selected_city}&country=&method=4",
            timeout=4,
        )
        if p_res.status_code == 200:
            p = p_res.json()["data"]["timings"]
            st.write(f"**الفجر:** {p['Fajr']}")
            st.write(f"**الظهر:** {p['Dhuhr']}")
            st.write(f"**العصر:** {p['Asr']}")
            st.write(f"**المغرب:** {p['Maghrib']}")
            st.write(f"**العشاء:** {p['Isha']}")
    except:
        st.write("تعذر جلب المواقيت")

# --------------------------------------------------
# 2. الواجهة الرئيسية - حاسبة الزكاة الذكية
# --------------------------------------------------
st.title("💰 حاسبة الزكاة الشاملة (المال وزكاة الفطر)")
st.write(
    "احسب زكاة أموالك وزكاة الفطر بناءً على النصاب وسعر جرام الذهب الحالي."
)

st.divider()

col_gold1, col_gold2 = st.columns(2)

with col_gold1:
    currency = st.selectbox(
        "اختر العملة:",
        ["درهم إماراتي (AED)", "ريال سعودي (SAR)", "دولار أمريكي (USD)"],
    )

default_gold_price = (
    300.0 if "AED" in currency else (305.0 if "SAR" in currency else 82.0)
)

with col_gold2:
    gold_price_per_gram = st.number_input(
        f"سعر جرام الذهب عيار 24 الحالي ({currency.split()[-1]}):",
        min_value=1.0,
        value=default_gold_price,
        step=1.0,
        help="يمكنك تعديل سعر الجرام حسب سعر السوق اليوم",
    )

# حساب نصاب زكاة المال (85 جرام ذهب عيار 24)
nisab_threshold = 85 * gold_price_per_gram

st.info(
    f"💡 **نصاب زكاة المال اليوم (85 جرام ذهب عيار 24):** {nisab_threshold:,.2f} {currency.split()[-1]}"
)

tab1, tab2 = st.tabs(["💵 زكاة المال والمدخرات", "🌾 زكاة الفطر"])

# --- التبويب الأول: زكاة المال ---
with tab1:
    st.subheader("حساب زكاة النقود والمدخرات")
    st.caption(
        "تجب الزكاة إذا بلغ إجمالي الأموال النصاب ومر عليها عام هجري كامل (الحول)."
    )

    c1, c2 = st.columns(2)
    with c1:
        cash = st.number_input(
            "السيولة النقدية والودائع البنكية:",
            min_value=0.0,
            value=0.0,
            step=100.0,
        )
        gold_owned = st.number_input(
            "قيمة الذهب/الفضة المعد للادخار:",
            min_value=0.0,
            value=0.0,
            step=100.0,
        )
    with c2:
        investments = st.number_input(
            "الأسهم والتجارة (المعدّة للبيع):",
            min_value=0.0,
            value=0.0,
            step=100.0,
        )
        debts_owed_to_you = st.number_input(
            "ديون لك على الآخرين (مرجوة السداد):",
            min_value=0.0,
            value=0.0,
            step=100.0,
        )

    deductions = st.number_input(
        "الديون والالتزامات الحالية الواجب سدادها فوراً (تخصم):",
        min_value=0.0,
        value=0.0,
        step=100.0,
    )

    if st.button("حساب زكاة المال"):
        total_wealth = (
            cash + gold_owned + investments + debts_owed_to_you
        ) - deductions

        st.divider()
        if total_wealth >= nisab_threshold:
            zakat_due = total_wealth * 0.025  # 2.5%
            st.success("✅ **بلغ مالك النصاب!**")

            res1, res2, res3 = st.columns(3)
            res1.metric(
                "إجمالي الصافي الخاضع للزكاة", f"{total_wealth:,.2f}"
            )
            res2.metric(
                "مقدار الزكاة الواجبة (2.5%)",
                f"{zakat_due:,.2f} {currency.split()[-1]}",
            )
            res3.metric("مقدار النصاب المطلوب", f"{nisab_threshold:,.2f}")
        else:
            st.warning("❌ **لم يبلغ مالك النصاب.**")
            st.write(
                f"إجمالي المبالغ لديك: **{total_wealth:,.2f}** | النصاب المطلوب للزكاة: **{nisab_threshold:,.2f}**"
            )

# --- التبويب الثاني: زكاة الفطر ---
with tab2:
    st.subheader("حساب زكاة الفطر")
    st.caption(
        "تخرج زكاة الفطر عن كل فرد مسلِم يعوله الشخص قبل صلاة عيد الفطر."
    )

    family_members = st.number_input(
        "عدد أفراد الأسرة (شاملاً نفسك ومن تعول):",
        min_value=1,
        value=1,
        step=1,
    )

    val_per_person = 25.0 if "AED" in currency or "SAR" in currency else 7.0
    cost_per_person = st.number_input(
        f"المقدار النقدي لزكاة الفطر للشخص الواحد ({currency.split()[-1]}):",
        min_value=1.0,
        value=val_per_person,
    )

    if st.button("حساب زكاة الفطر"):
        total_fitr = family_members * cost_per_person
        st.success(
            f"🌾 **إجمالي زكاة الفطر الواجب إخراجها:** {total_fitr:,.2f} {currency.split()[-1]}"
        )
        st.info(
            "القدر الشرعي الأصلي: صاع من طعام (حوالي 2.5 إلى 3 كجم من الأرز أو القمح) عن كل شخص."
        )
