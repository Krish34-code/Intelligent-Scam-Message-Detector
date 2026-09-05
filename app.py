import streamlit as st
import re


# ---------------------------------
# PAGE SETTINGS
# ---------------------------------

st.set_page_config(
    page_title="Scam Message Detector",
    page_icon="🛡️"
)


# ---------------------------------
# WEBSITE TITLE
# ---------------------------------

st.title("🛡️ Intelligent Scam Message Detector")

st.write(
    "Paste a suspicious SMS, WhatsApp message, or email "
    "and the system will analyze potential scam indicators."
)


# ---------------------------------
# MESSAGE INPUT BOX
# ---------------------------------

message = st.text_area(
    "Paste suspicious message here:",
    height=200
)


# ---------------------------------
# ANALYZE BUTTON
# ---------------------------------

if st.button("🔍 Analyze Message"):

    # Check if message is empty
    if message.strip() == "":

        st.warning("Please enter a message first.")

    else:

        # Convert message to lowercase
        text = message.lower()

        # Starting risk score
        score = 0

        # Store detected problems
        detected = []

        # Store possible scam categories
        categories = []


        # ---------------------------------
        # 1. URGENCY WORD DETECTION
        # ---------------------------------

        urgency_words = [
            "urgent",
            "immediately",
            "act now",
            "hurry",
            "final warning"
        ]

        for word in urgency_words:

            if word in text:

                score += 8

                detected.append(
                    f"Urgency language detected: {word}"
                )


        # ---------------------------------
        # 2. BANKING / KYC DETECTION
        # ---------------------------------

        banking_words = [
            "kyc",
            "account blocked",
            "account suspended",
            "verify your account",
            "bank account"
        ]

        banking_found = False

        for word in banking_words:

            if word in text:

                score += 12

                banking_found = True

                detected.append(
                    f"Banking/KYC pattern detected: {word}"
                )

        if banking_found:

            categories.append(
                "Banking / KYC Fraud"
            )


        # ---------------------------------
        # 3. LOTTERY / PRIZE SCAM
        # ---------------------------------

        lottery_words = [
            "you have won",
            "winner",
            "lottery",
            "claim your prize",
            "congratulations"
        ]

        lottery_found = False

        for word in lottery_words:

            if word in text:

                score += 12

                lottery_found = True

                detected.append(
                    f"Prize/Lottery pattern detected: {word}"
                )

        if lottery_found:

            categories.append(
                "Lottery / Prize Scam"
            )


        # ---------------------------------
        # 4. JOB SCAM
        # ---------------------------------

        job_words = [
            "work from home",
            "registration fee",
            "earn daily",
            "job offer",
            "guaranteed income"
        ]

        job_found = False

        for word in job_words:

            if word in text:

                score += 10

                job_found = True

                detected.append(
                    f"Job scam indicator detected: {word}"
                )

        if job_found:

            categories.append(
                "Possible Job Scam"
            )


        # ---------------------------------
        # 5. INVESTMENT SCAM
        # ---------------------------------

        investment_words = [
            "double your money",
            "guaranteed returns",
            "high returns",
            "crypto profit"
        ]

        investment_found = False

        for word in investment_words:

            if word in text:

                score += 12

                investment_found = True

                detected.append(
                    f"Investment scam indicator detected: {word}"
                )

        if investment_found:

            categories.append(
                "Possible Investment Scam"
            )


        # ---------------------------------
        # 6. URL DETECTION
        # ---------------------------------

        urls = re.findall(
            r'https?://[^\s]+|www\.[^\s]+',
            text
        )

        if urls:

            score += 20

            detected.append(
                "URL detected in message"
            )

            categories.append(
                "Possible Phishing"
            )


        # ---------------------------------
        # 7. SENSITIVE INFORMATION
        # ---------------------------------

        sensitive_words = [
            "otp",
            "pin",
            "cvv",
            "password"
        ]

        for word in sensitive_words:

            if word in text:

                score += 15

                detected.append(
                    f"Sensitive information reference: {word}"
                )


        # ---------------------------------
        # LIMIT SCORE TO 100
        # ---------------------------------

        score = min(score, 100)


        # ---------------------------------
        # RISK LEVEL
        # ---------------------------------

        if score >= 60:

            risk = "🔴 HIGH RISK"

        elif score >= 30:

            risk = "🟠 MEDIUM RISK"

        else:

            risk = "🟢 LOW RISK"


        # ---------------------------------
        # SHOW RESULTS
        # ---------------------------------

        st.divider()

        st.subheader("📊 Analysis Result")

        st.metric(
            "Risk Score",
            f"{score}/100"
        )

        st.subheader(risk)


        # Show scam category

        if categories:

            st.write("### Possible Scam Category")

            unique_categories = list(
                set(categories)
            )

            for category in unique_categories:

                st.write("•", category)


        # Show detected indicators

        if detected:

            st.write("### Detected Risk Indicators")

            for item in detected:

                st.write("⚠️", item)

        else:

            st.success(
                "No major scam indicators were detected."
            )


        # ---------------------------------
        # SAFETY RECOMMENDATION
        # ---------------------------------

        st.write("### 🛡️ Safety Recommendation")

        if score >= 60:

            st.error(
                "Do not click suspicious links, share OTP, PIN, "
                "CVV, or passwords, or send money. Verify the "
                "sender through official channels."
            )

        elif score >= 30:

            st.warning(
                "Be cautious. Verify the sender before taking "
                "any action."
            )

        else:

            st.info(
                "No major scam indicators were detected, "
                "but always remain cautious."
            )