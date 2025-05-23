import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fundraising DApp", layout="centered")

st.title("🎓 Fundraising for University Students")
st.subheader("This app helps financially struggling students receive donations transparently.")

# Sidebar for donation categories
st.sidebar.title("🎯 Select Donation Category")
categories = ["Urgent Need", "Moderate Need", "Simple Need"]
selected_category = st.sidebar.selectbox("Choose a student need level:", categories)

# Set goal and deadline
if selected_category == "Urgent Need":
    target_amount = 3000
    deadline = "2025-06-10"
elif selected_category == "Moderate Need":
    target_amount = 2000
    deadline = "2025-07-01"
else:
    target_amount = 1000
    deadline = "2025-08-01"

filename = f"donations_{selected_category.replace(' ', '_')}.csv"

# Load current donations
if os.path.exists(filename):
    records = pd.read_csv(filename)
    current_amount = records["Amount"].sum()
else:
    records = pd.DataFrame(columns=["Name", "University", "Amount", "Date"])
    current_amount = 0

# Display campaign info
st.markdown(f"""
🎯 **Goal:** ${target_amount}  
📄 *Raised so far:* **${current_amount}**  
⏰ **Deadline:** {deadline}
""")

# Donation form
st.markdown("---")
st.markdown("### 💸 Make a Donation")
with st.form("donation_form"):
    donor_name = st.text_input("Enter your name:")
    university = st.selectbox("Select the student's university:", [
        "Yarmouk University",
        "Jordan University of Science and Technology",
        "Mu'tah University",
        "Private University",
        "Other"
    ])
    donation = st.number_input("Enter your donation amount ($):", min_value=1, step=1)
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("💖 Donate")
    with col2:
        clear = st.form_submit_button("🔁 Reset")

if clear:
    st.session_state["donation_form"] = ""
    st.experimental_rerun()

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
        new_record = pd.DataFrame([donation_data])
        new_record.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
        st.experimental_rerun()

# Show donation summary only if there are donations
if not records.empty:
    st.markdown("---")
    st.subheader("📊 Donation Progress")
    progress = [current_amount, target_amount - current_amount]
    labels = ['Raised', 'Remaining']
    colors = ['green', 'lightgray']
    fig, ax = plt.subplots()
    ax.pie(progress, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("## 🧾 Donation Records")
    st.markdown(f"🎉 **Number of Donors:** {len(records)}")
    st.dataframe(records)
else:
    st.info("No donations recorded yet. Only the target amount is shown.")

# Footer
st.caption("Built by Taimaa Almetani 💚 using Streamlit for Social Impact")






