import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="FinVision Enterprise", page_icon="💎", layout="wide")
st.markdown("""<style>div[data-testid="metric-container"]{background-color:#fff;border:1px solid #e0e0e0;padding:15px;border-radius:10px;box-shadow:0 2px 4px rgba(0,0,0,0.05);}</style>""", unsafe_allow_html=True)

if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin": {
            "pass": "1234", "name": "Олександр Коваленко", "role": "Головний бухгалтер",
            "company": 'ТОВ "Вектор-Інвест"', "edrpou": "42891045",
            "demo_rev": (1200000, 1450000, 1380000, 1800000),
            "demo_cost": (850000, 920000, 900000, 1100000),
            "demo_act": (3000000, 3200000, 3150000, 3600000)
        },
        "alex": {
            "pass": "5678", "name": "Марія Савченко", "role": "Фінансовий директор",
            "company": 'ТОВ "АгроТех-Груп"', "edrpou": "39512804",
            "demo_rev": (2500000, 2900000, 3400000, 3100000),
            "demo_cost": (1800000, 2100000, 2300000, 2200000),
            "demo_act": (5500000, 5800000, 6200000, 6000000)
        }
    }

for k, v in {"logged_in": False, "use_demo": False, "curr_user": "admin", "logs": []}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def add_log(action):
    u = st.session_state.users_db[st.session_state.curr_user]
    st.session_state.logs.append({"Час": datetime.now().strftime("%H:%M:%S"), "Користувач": u["name"], "Компанія": u["company"], "Подія": action})

if not st.session_state.logged_in:
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.title("💎 Система FinVision")
        auth_t1, auth_t2 = st.tabs(["🔐 Вхід у кабінет", "📝 Реєстрація компанії"])
        with auth_t1:
            st.info("Тестові акаунти: **admin / 1234** або **alex / 5678**")
            with st.form("login_form"):
                user = st.text_input("Логін")
                pwd = st.text_input("Пароль", type="password")
                if st.form_submit_button("Увійти в систему", use_container_width=True):
                    if user in st.session_state.users_db and pwd == st.session_state.users_db[user]["pass"]:
                        st.session_state.logged_in = True
                        st.session_state.curr_user = user
                        add_log("Вхід у систему")
                        st.rerun()
                    else:
                        st.error("❌ Невірний логін або пароль!")
        with auth_t2:
            with st.form("reg_form"):
                n_log = st.text_input("Логін (латиницею)*")
                n_pwd = st.text_input("Пароль*", type="password")
                n_nam = st.text_input("Ваше ПІБ*", value="Іван Петренко")
                n_rol = st.selectbox("Посада", ["Головний бухгалтер", "Фінансовий директор", "Аудитор"])
                n_cmp = st.text_input("Назва компанії*", value='ТОВ "Нові Технології"')
                n_edr = st.text_input("Код ЄДРПОУ (8 цифр)*", value="44112233", max_chars=8)
                if st.form_submit_button("✅ Зареєструватися", use_container_width=True):
                    if not n_log or not n_pwd or not n_cmp:
                        st.warning("⚠️ Заповніть обов'язкові поля!")
                    elif n_log in st.session_state.users_db:
                        st.error("❌ Цей логін вже зайнятий!")
                    else:
                        st.session_state.users_db[n_log] = {
                            "pass": n_pwd, "name": n_nam, "role": n_rol,
                            "company": n_cmp, "edrpou": n_edr,
                            "demo_rev": (950000, 1150000, 1300000, 1600000),
                            "demo_cost": (700000, 800000, 850000, 980000),
                            "demo_act": (2200000, 2400000, 2600000, 2900000)
                        }
                        st.success(f"🎉 Компанію {n_cmp} зареєстровано! Перейдіть на вкладку «🔐 Вхід у кабінет».")
else:
    u_data = st.session_state.users_db[st.session_state.curr_user]
    st.title(f"💎 FinVision: {u_data['company']}")
    st.caption(f"Код ЄДРПОУ: {u_data['edrpou']} | Сесія: {datetime.now().strftime('%d.%m.%Y')} | Стандарт МСФЗ / П(С)БО")
    st.markdown("---")
    with st.sidebar:
        st.subheader("👤 Профіль спеціаліста")
        st.success(f"**{u_data['name']}**\n\nКомпанія: *{u_data['company']}*\n\nПосада: `{u_data['role']}`")
        
        with st.expander("⚙️ Налаштування компанії"):
            with st.form("sidebar_profile_form"):
                nn = st.text_input("ПІБ:", value=u_data["name"])
                nc = st.text_input("Компанія:", value=u_data["company"])
                ne = st.text_input("ЄДРПОУ:", value=u_data["edrpou"], max_chars=8)
                if st.form_submit_button("💾 Зберегти", use_container_width=True):
                    st.session_state.users_db[st.session_state.curr_user]["name"] = nn
                    st.session_state.users_db[st.session_state.curr_user]["company"] = nc
                    st.session_state.users_db[st.session_state.curr_user]["edrpou"] = ne
                    add_log(f"Оновлено реквізити ({nc})")
                    st.rerun()

        with st.expander("🛡️ Журнал аудиту дій"):
            if st.session_state.logs:
                st.dataframe(pd.DataFrame(st.session_state.logs), use_container_width=True)

        if st.button("🚪 Вийти з акаунта", use_container_width=True):
            add_log("Вихід із системи")
            st.session_state.logged_in = False
            st.session_state.use_demo = False
            st.rerun()
        st.markdown("---")
        uploaded_file = st.file_uploader("1. Звіт (.xlsx або .csv)", type=["xlsx", "csv"])
        if st.button("⚡ Завантажити звіт компанії", use_container_width=True):
            if not st.session_state.use_demo:
                add_log(f"Завантажено звітність {u_data['company']}")
            st.session_state.use_demo = True
        st.markdown("---")
        st.subheader("💱 Валюта звітності")
        currency = st.selectbox("Оберіть валюту:", ["UAH (₴)", "USD ($)", "EUR (€)"])
        rate, sym = 1.0, "₴"
        if currency == "USD ($)":
            rate = st.number_input("Курс USD/UAH:", min_value=1.0, value=41.5, step=0.5)
            sym = "$"
        elif currency == "EUR (€)":
            rate = st.number_input("Курс EUR/UAH:", min_value=1.0, value=45.0, step=0.5)
            sym = "€"
        st.markdown("---")
        st.subheader("🎛️ Моделювання")
        tax_rate = st.slider("Податок на прибуток (%)", 0, 30, 18)
        cost_change = st.slider("Стрес-тест витрат (%)", -30, 30, 0)

    df = None
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    elif st.session_state.use_demo:
        df = pd.DataFrame({
            "Період": ("Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"),
            "Виручка": u_data["demo_rev"],
            "Витрати": u_data["demo_cost"],
            "Активи": u_data["demo_act"]
        })
    if df is not None:
        with st.sidebar:
            periods = df["Період"].unique().tolist()
            sel_periods = st.multiselect("Квартали:", options=periods, default=periods)
        fdf = df[df["Період"].isin(sel_periods)].copy()
        if fdf.empty:
            st.warning("⚠️ Оберіть хоча б один квартал.")
        else:
            for col in ("Виручка", "Витрати", "Активи"):
                fdf[col] = fdf[col] / rate
            fdf["Скориговані витрати"] = fdf["Витрати"] * (1 + cost_change / 100)
            fdf["Прибуток до податків"] = fdf["Виручка"] - fdf["Скориговані витрати"]
            fdf["Податок"] = fdf["Прибуток до податків"].apply(lambda x: x * (tax_rate / 100) if x > 0 else 0)
            fdf["Чистий прибуток"] = fdf["Прибуток до податків"] - fdf["Податок"]
            fdf["ROS (%)"] = round((fdf["Чистий прибуток"] / fdf["Виручка"]) * 100, 2)
            fdf["ROA (%)"] = round((fdf["Чистий прибуток"] / fdf["Активи"]) * 100, 2)

            k1, k2, k3, k4 = st.columns(4)
            tot_rev, tot_net = fdf["Виручка"].sum(), fdf["Чистий прибуток"].sum()
            k1.metric("Виручка", f"{tot_rev:,.0f} {sym}")
            k2.metric("Чистий прибуток", f"{tot_net:,.0f} {sym}", delta=f"Витрати: {cost_change}%" if cost_change != 0 else None, delta_color="inverse")
            k3.metric("Середня ROS", f"{fdf['ROS (%)'].mean():.2f} %")
            k4.metric("Середня ROA", f"{fdf['ROA (%)'].mean():.2f} %")
            st.markdown("<br>", unsafe_allow_html=True)

            t1, t2, t3, t4, t5, t6, t7 = st.tabs(["📊 Аналітика", "🎯 Бюджет і Ліміти", "📋 Таблиця", "🧮 Бухгалтеру", "🔮 Прогноз", "💡 Висновок", "📚 Довідник"])

            with t1:
                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(px.bar(fdf, x="Період", y=["Виручка", "Скориговані витрати", "Чистий прибуток"], barmode="group", title=f"Доходи та витрати ({sym})"), use_container_width=True)
                with c2:
                    fig_pie = go.Figure(data=[go.Pie(labels=["Витрати", "Податки", "Чистий прибуток"], values=[fdf["Скориговані витрати"].sum(), fdf["Податок"].sum(), max(0, tot_net)], hole=.45)])
                    st.plotly_chart(fig_pie, use_container_width=True)
                st.plotly_chart(px.area(fdf, x="Період", y=["ROS (%)", "ROA (%)"], markers=True, title="Динаміка рентабельності (%)"), use_container_width=True)

            with t2:
                b1, b2, b3 = st.columns(3)
                plan_q = b1.number_input(f"План виручки ({sym}):", 100.0, value=float(round(1400000/rate, 0)), step=1000.0)
                cost_lim = b2.number_input(f"Ліміт витрат ({sym}):", 100.0, value=float(round(950000/rate, 0)), step=1000.0)
                res_pct = b3.slider("Резервний фонд (%):", 0, 50, 15)
                
                over = fdf[fdf["Скориговані витрати"] > cost_lim]
                if not over.empty:
                    st.error(f"🚨 Перевищення ліміту витрат у періодах: {', '.join(over['Період'])}")
                else:
                    st.success("✅ Ліміти витрат у нормі в усіх звітних періодах.")
                    
                st.info(f"🏦 Накопичений резервний фонд: **{max(0, tot_net * (res_pct / 100)):,.0f} {sym}**")
                
                pf_df = fdf[["Період", "Виручка", "Скориговані витрати", "Чистий прибуток"]].copy()
                pf_df["План виручки"] = plan_q
                pf_df["Виконання (%)"] = round((pf_df["Виручка"] / pf_df["План виручки"]) * 100, 1)
                st.dataframe(pf_df, use_container_width=True)

            with t3:
                st.dataframe(fdf, use_container_width=True)
                if st.download_button("📥 Завантажити звіт (CSV)", data=fdf.to_csv(index=False).encode('utf-8-sig'), file_name=f"report_{u_data['edrpou']}.csv", mime="text/csv"):
                    add_log(f"Експортовано звіт ({currency})")
            with t4:
                bc1, bc2 = st.columns(2)
                with bc1:
                    st.markdown("#### 🧾 Калькулятор ПДВ (20%)")
                    amt = st.number_input(f"Сума ПДВ ({sym}):", 0.0, value=10000.0, step=500.0)
                    mode = st.radio("Режим:", ["Виділити ПДВ", "Нарахувати ПДВ"])
                    if mode == "Виділити ПДВ":
                        st.info(f"Без ПДВ: **{amt/1.2:,.2f} {sym}** | ПДВ: **{amt-(amt/1.2):,.2f} {sym}**")
                    else:
                        st.info(f"ПДВ: **{amt*0.2:,.2f} {sym}** | З ПДВ: **{amt*1.2:,.2f} {sym}**")
                with bc2:
                    st.markdown("#### ⚖️ Точка беззбитковості")
                    fc = st.number_input(f"Постійні витрати ({sym}):", 0.0, value=round(500000.0/rate, 0), step=1000.0)
                    mp = st.slider("Маржинальність (%):", 5, 90, 35)
                    st.success(f"Точка беззбитковості: **{fc/(mp/100):,.2f} {sym}**")

            with t5:
                st.markdown("#### 🔮 Прогнозування на наступний період")
                if len(fdf) >= 2:
                    x = np.arange(len(fdf))
                    s_rev, i_rev = np.polyfit(x, fdf["Виручка"], 1)
                    p_rev = max(0, s_rev * len(fdf) + i_rev)
                    st.metric("Прогноз виручки (Q+1)", f"{p_rev:,.0f} {sym}")
                    st.plotly_chart(px.line(x=list(fdf["Період"]) + ["Прогноз (Q+1)"], y=list(fdf["Виручка"]) + [p_rev], markers=True, title="Лінійний тренд виручки"), use_container_width=True)
                else:
                    st.warning("⚠️ Оберіть мінімум 2 періоди.")

            with t6:
                st.markdown("#### 🤖 Експертний висновок системи")
                if tot_net >= 0.01:
                    st.success(f"✅ Компанія **{u_data['company']}** є прибутковою. Чистий прибуток за період складає **{tot_net:,.0f} {sym}**.")
                else:
                    st.error(f"🚨 Збиткова діяльність компанії **{u_data['company']}**. Дефіцит коштів: **{abs(tot_net):,.0f} {sym}**.")
                
                best_q = fdf.loc[fdf['Чистий прибуток'].idxmax()]['Період']
                st.info(f"🏆 Найбільш прибутковий звітний період: **{best_q}**.")
                
                if fdf['ROS (%)'].mean() >= 15:
                    st.success("📈 Високий рівень рентабельності продажів (ROS > 15%). Бізнес-модель демонструє стійкість.")
                else:
                    st.warning("⚠️ Помірна рентабельність. Рекомендується оптимізувати операційні витрати.")

            with t7:
                st.markdown("#### 📚 Методологія фінансових розрахунків")
                st.markdown("""
                У програмному комплексі **FinVision** застосовуються такі стандартизовані формули фінансового аналізу:
                
                * **Чистий прибуток:** `(Виручка - Скориговані витрати) - Податок на прибуток`
                * **ROS (Рентабельність продажів):** `(Чистий прибуток / Виручка) × 100%` — показує частку прибутку в кожній заробленій одиниці виручки.
                * **ROA (Рентабельність активів):** `(Чистий прибуток / Активи) × 100%` — оцінює ефективність використання майна підприємства.
                * **Точка беззбитковості (BEP):** `Постійні витрати / (Маржинальність % / 100)` — мінімальний обсяг виручки для покриття всіх витрат.
                * **Резервний фонд:** `Чистий прибуток × Відсоток відрахувань` — формування фінансової подушки безпеки.
                """)
    else:
        st.info(f"👈 Вітаємо, **{u_data['name']}**! Завантажте файл або натисніть **«⚡ Завантажити звіт компанії»**.")
