import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

# إعداد الجلسة لتفعيل إعادة الضبط
if "reset" not in st.session_state:
    st.session_state["reset"] = False

st.set_page_config(page_title="Fundraising DApp", layout="centered")

st.title("🎓 Fundraising for University Students")
st.subheader("This app helps financially struggling students receive donations transparently.")

# الشريط الجانبي لاختيار الفئة
st.sidebar.title("🎯 Select Donation Category")
categories = ["Urgent Need", "Moderate Need", "Simple Need"]
selected_category = st.sidebar.selectbox("Choose a student need level:", categories)

# معلومات الحملة حسب الفئة
if selected_category == "Urgent Need":
    target_amount = 3000
    current_amount = 1800
    deadline = "2025-06-10"
elif selected_category == "Moderate Need":
    target_amount = 2000
    current_amount = 1000
    deadline = "2025-07-01"
elif selected_category == "Simple Need":
    target_amount = 1000
    current_amount = 300
    deadline = "2025-08-01"

# عرض معلومات الحملة
st.markdown(f"""
🎯 **Goal:** ${target_amount}  
📄 *Raised so far* : **${current_amount}**  
⏰ **Deadline:** {deadline}
""")

# نموذج التبرع
with st.form("donation_form"):
    donor_name = st.text_input("Enter your name:", value="" if st.session_state["reset"] else "")
    university = st.selectbox("Select the student's university:", [
        "Yarmouk University",
        "Jordan University of Science and Technology",
        "Mu'tah University",
        "Private University",
        "Other"
    ], index=0 if st.session_state["reset"] else 0)

    donation = st.number_input("Enter your donation amount ($):", min_value=1, step=1, value=1 if st.session_state["reset"] else 1)

    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("💖 Donate")
    with col2:
        reset = st.form_submit_button("🔁 Reset")

# التعامل مع زر Reset
if reset:
    st.session_state["reset"] = True

# إعادة تعيين الحالة بعد الاستخدام
if st.session_state["reset"]:
    st.session_state["reset"] = False

# حفظ التبرع
if submit:
    if donor_name.strip() == "":
        st.warning("Please enter your name before donating.")
    else:
        st.success("✅ Donation recorded successfully!")
        st.balloons()
        st.markdown(f"### 🙏 Thank you {donor_name}! You've helped a student in need 🎓❤️")

        donation_data = {
            "Name": donor_name,
            "University": university,
            "Amount": donation,
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.DataFrame([donation_data])
        filename = f"donations_{selected_category.replace(' ', '_')}.csv"
        df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)

# تنبيه
st.info("If the goal is not met before the deadline, all donations will be refunded automatically.")

# رسم مخطط دائري
progress = [current_amount, target_amount - current_amount]
labels = ['Raised', 'Remaining']
colors = ['green', 'lightgray']
fig, ax = plt.subplots()
ax.pie(progress, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.subheader("📊 Donation Progress")
st.pyplot(fig)

# عرض التبرعات المسجلة
st.markdown("## 🧾 Donation Records")
filename = f"donations_{selected_category.replace(' ', '_')}.csv"
try:
    records = pd.read_csv(filename)
    st.markdown(f"🎉 **Number of Donors:** {len(records)}")
    st.dataframe(records)
except FileNotFoundError:
    st.info("No donations recorded yet.")

# تذييل الصفحة
st.caption("Built by Taimaa Almetani 💚 using Streamlit for Social Impact")




