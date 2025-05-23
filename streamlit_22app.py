import streamlit as st

st.set_page_config(page_title="Fundraising DApp", layout="centered")

st.title("🎓 Fundraising for Students in Need")
st.subheader("This app helps students collect donations transparently.")

# Campaign details
target_amount = 1000
current_amount = 630
deadline = "2025-06-10"

st.markdown(f"""
**Goal:** ${target_amount}  
**Raised so far:** ${current_amount}  
**Deadline:** {deadline}
""")

# Donation input
donation = st.number_input("Enter your donation amount ($):", min_value=1, step=1)

if st.button("Donate"):
    st.success("✅ Donation simulated! (blockchain integration coming soon)")

# Info
st.info("If the goal is not met before the deadline, all donations will be refunded automatically.")

st.markdown("---")
st.caption("Built by Taimaa Almetani 💚 using Streamlit + Web3 Vision")
import matplotlib.pyplot as plt

# البيانات
progress = [current_amount, target_amount - current_amount]
labels = ['Raised', 'Remaining']
colors = ['green', 'lightgray']

# الرسم
fig, ax = plt.subplots()
ax.pie(progress, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # حتى يكون الشكل دائري تمامًا

# عرض الرسم في Streamlit
st.subheader("📊 Donation Progress")
st.pyplot(fig)
