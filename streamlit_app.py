import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fundraising DApp", layout="centered")

st.title("🎓 Fundraising for University Students")
st.subheader("This app helps financially struggling students receive donations transparently.")

# Sidebar to select donation category
st.sidebar.title("🎯 Select Donation Category")
categories = ["Urgent Need", "Moderate Need", "Simple Need"]
selected_category = st.sidebar.selectbox("Choose a student need level:", categories)

# Set donation goal and deadline based on category
if selected_category == "Urgent Need":
    target_amount = 3000
    deadline = "2025-06-10"
elif selected_category == "Moderate Need":
    target_amount = 2000
    deadline = "2025-07-01"
elif selected_category == "Simple Need":
    target_amount = 1000
    deadline = "2025-08-01"

# CSV filename based on category
filename = f"donations_{selected_category.replace(' ', '_')}.csv"

# Check if file exists and has data
has_donations = os.path.exists(filename) and os.path.getsize(filename) > 0

if has_donations:
    try:
        records = pd.read_csv(filename)
        current_amount = records["Amount"].sum()

        st.markdown(f"""
        🎯 **Goal:** ${target_amount}  
        📄 *Raised so far* : **${current_amount}**  
        ⏰ **Deadline:** {deadline}
        """)

        st.subheader("📊 Donation Progress")
        progress = [current_amount, max(target_amount - current_amount, 0)]
        labels = ['Raised', 'Remaining']
        colors = ['green', 'lightgray']
        fig, ax = plt.subplots()
        ax.pie(progress, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        st.markdown("## 🧾 Donation Records")
        st.markdown(f"🎉 **Number of Donors:** {len(records)}")
        st.dataframe(records)

    except Exception as e:
        st.error(f"Error loading records: {e}")
else:
    st.markdown(f"""
    🎯 **Goal:** ${target_amount}  
    ⏰ **Deadline:** {deadline}
    """)
    st.info("No donations yet. Be the first to support this cause!")

# Donation form
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
    submit = st.form_submit_button("💖 Donate")

# Handle donation submission
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
        df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)

# Footer
st.info("If the goal is not met before the deadline, all donations will be refunded automatically.")
st.caption("Built by Taimaa Almetani 💚 using Streamlit for Social Impact")





