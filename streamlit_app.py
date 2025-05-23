import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="Fundraising DApp", layout="centered")

st.title("🎓 Fundraising for University Students")
st.subheader("This app helps financially struggling students receive donations transparently.")

# الشريط الجانبي لاختيار الفئة
st.sidebar.title("🎯 Select Donation Category")
categories = ["Urgent Need", "Medium Need", "Simple Need"]
selected_category = st.sidebar.selectbox("Choose a student need level:", categories)

# إعداد بيانات كل فئة
if selected_category == "Urgent Need":
    target_amount = 3000
    current_amount = 1800
    deadline = "2025-06-10"
elif selected_category == "Medium Need":
    target_amount = 2000
    current_amount = 900
    deadline = "2025-07-01"
elif selected_category == "Simple Need":
    target_amount = 1000
    current_amount = 300
    deadline = "2025-08-01"

# عرض الإحصائيات
st.markdown(f"""
💰 **Goal:** ${target_amount}  
📄 _Raised so far_ : **${current_amount}**  
📆 **Deadline:** {deadline}
""")

# إدخال اسم المتبرع والمبلغ
donor_name = st.text_input("Enter your name:")
donation = st.number_input("Enter your donation amount ($):", min_value=1, step=1)

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
        filename = f"donations_{selected_category.replace(' ', '_')}.csv"
        df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)

# معلومة جانبية
st.info("If the goal is not met before the deadline, all donations will be refunded automatically.")

# الرسم البياني للتقدم
progress = [current_amount, target_amount - current_amount]
labels = ['Raised', 'Remaining']
colors = ['green', 'lightgray']

fig, ax = plt.subplots()
ax.pie(progress, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')

st.subheader("📊 Donation Progress")
st.pyplot(fig)

# عرض جدول التبرعات وعدد المتبرعين
st.markdown("## 🧾 Donation Records")
filename = f"donations_{selected_category.replace(' ', '_')}.csv"

try:
    records = pd.read_csv(filename)
    donor_count = len(records)
    st.markdown(f"🎉 **Number of Donors:** {donor_count}")
    st.dataframe(records)
except FileNotFoundError:
    st.info("No donations recorded yet.")

# تذييل
st.caption("Built by Taimaa Almetani 💚 using Streamlit for Social Impact")


