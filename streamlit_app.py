import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fundraising DApp", layout="centered")

st.title("🎓 Fundraising for University Students")
st.subheader("This app helps financially struggling students receive donations transparently.")

# 🎯 Sidebar to select donation category
st.sidebar.title("🎯 Select Donation Category")
categories = ["Urgent Need", "Moderate Need", "Simple Need"]
selected_category = st.sidebar.selectbox("Choose a student need level:", categories)

# 🎯 Set values based on selected category
if selected_category == "Urgent Need":
    target_amount = 3000
    deadline = "2025-06-10"
elif selected_category == "Moderate Need":
    target_amount = 2000
    deadline = "2025-07-01"
elif selected_category == "Simple Need":
    target_amount = 1000
    deadline = "2025-08-01"

filename = f"donations_{selected_category.replace(' ', '_')}.csv"

# 📂 Try to read existing donations
if os.path.exists(filename):
    records = pd.read_csv(filename)
    total_raised = records['Amount'].sum()
else:
    records = pd.DataFrame(columns=["Name", "University", "Amount", "Date"])
    total_raised = 0

# 🎯 Campaign info
st.markdown(f"""
🎯 **Goal:** ${target_amount}  
📄 *Raised so far* : **${total_raised}**  
⏰ **Deadline:** {deadline}
""")

# 💳 Donation form
st.markdown("### 💬 Enter Donation Details")
with st.form("donation_form"):
    donor_name = st.text_input("Enter your name:")
    university = st.selectbox("Select the student's university:", [
        "Yarmouk University",
        "Jordan University of Science and Technology",
        "University of Jordan",
        "Hashemite University",
        "Al al-Bayt University",
        "Al-Balqa Applied University",
        "German Jordanian University",
        "Zarqa University",
        "Philadelphia University",
        "Mutah University",
        "Other"
    ])
    donation = st.number_input("Enter your donation amount ($):", min_value=1, step=1)
    submit = st.form_submit_button("💖 Donate")

# ✅ Save donation
if submit:
    if donor_name.strip() == "":
        st.warning("Please enter your name before donating.")
    else:
        st.success("✅ Donation recorded successfully!")
        st.balloons()
        st.markdown(f"### 🙏 Thank you {donor_name}! You've helped a student in need 🎓❤️")

        new_donation = {
            "Name": donor_name,
            "University": university,
            "Amount": donation,
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        new_df = pd.DataFrame([new_donation])
        new_df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
        records = pd.read_csv(filename)
        total_raised = records['Amount'].sum()

# ℹ️ Info
st.info("If the goal is not met before the deadline, all donations will be refunded automatically.")

# 📊 Show pie chart if donations exist
if not records.empty:
    progress = [total_raised, max(target_amount - total_raised, 0)]
    labels = ['Raised', 'Remaining']
    colors = ['green', 'lightgray']
    fig, ax = plt.subplots()
    ax.pie(progress, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.subheader("📊 Donation Progress")
    st.pyplot(fig)

    # 📑 Donation Records
    st.markdown("## 🧾 Donation Records")
    st.markdown(f"🎉 **Number of Donors:** {len(records)}")
    st.dataframe(records)

# 👣 Footer
st.caption("Built by Taimaa Almetani 💚 using Streamlit for Social Impact")








