import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="University Tuition Support", layout="centered")

# عنوان الصفحة
st.title("🎓 Fundraising for University Students")
st.subheader("This app helps financially struggling students receive donations transparently.")

# تحديد الحملة
st.sidebar.title("🎯 Select Donation Category")
campaigns = {
    "💥 Urgent Need": {
        "target": 3000,
        "current": 1800,
        "deadline": "2025-06-10"
    },
    "⚠️ Medium Need": {
        "target": 2000,
        "current": 850,
        "deadline": "2025-07-15"
    },
    "✅ Simple Need": {
        "target": 1000,
        "current": 300,
        "deadline": "2025-08-01"
    }
}
selected_campaign = st.sidebar.selectbox("Choose a student need level:", list(campaigns.keys()))
campaign_data = campaigns[selected_campaign]
target_amount = campaign_data["target"]
current_amount = campaign_data["current"]
deadline = campaign_data["deadline"]

# عرض تفاصيل الحملة
st.markdown(f"""
**🎯 Goal:** ${target_amount}  
**📈 Raised so far:** ${current_amount}  
**⏰ Deadline:** {deadline}
""")

# إدخال بيانات المتبرع
donor_name = st.text_input("Enter your name:")
donation = st.number_input("Enter your donation amount ($):", min_value=1, step=1)

# زر التبرع
if st.button("Donate"):
    if donor_name.strip() == "":
        st.warning("Please enter your name before donating.")
    else:
        st.success("✅ Donation recorded successfully!")
        donation_data = {
            "Name": donor_name,
            "Amount": donation,
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.DataFrame([donation_data])
        filename = f"donations_{selected_campaign.replace(' ', '_')}.csv"
        df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)

# ملاحظة عامة
st.info("If the goal is not met before the deadline, all donations will be refunded automatically.")

# عرض شريط التقدم (Pie Chart)
progress = [current_amount, target_amount - current_amount]
labels = ['Raised', 'Remaining']
colors = ['green', 'lightgray']
fig, ax = plt.subplots()
ax.pie(progress, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.subheader("📊 Donation Progress")
st.pyplot(fig)

# عرض السجلات
st.markdown("## 🧾 Donation Records")
filename = f"donations_{selected_campaign.replace(' ', '_')}.csv"
try:
    records = pd.read_csv(filename)
    st.dataframe(records)
    # إظهار عدد المتبرعين
    num_donors = len(records)
    st.success(f"🙋 Total Donors for this category: {num_donors}")
except FileNotFoundError:
    st.info("No donations recorded yet.")

# توقيع
st.markdown("---")
st.caption("Built by Taimaa Almetani 💚 using Streamlit for Social Impact")

