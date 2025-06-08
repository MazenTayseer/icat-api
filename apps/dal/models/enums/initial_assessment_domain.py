class InitialAssessmentDomain:
    AUTHENTICATION = "AUTHENTICATION_AND_DEVICE_SECURITY"
    DATA_PRIVACY = "DATA_PRIVACY_AND_RESPONSIBLE_SHARING"
    FINANCIAL = "FINANCIAL_AND_PAYMENT_SECURITY"
    PASSWORD = "PASSWORD_HYGIENE"
    PHISHING = "PHISHING_AND_SOCIAL_ENGINEERING"
    SAFE_BROWSING = "SAFE_BROWSING_AND_PUBLIC_WIFI"

    choices = [
        (AUTHENTICATION, "Authentication & Device Security"),
        (DATA_PRIVACY, "Data Privacy & Responsible Sharing"),
        (FINANCIAL, "Financial & Payment Security"),
        (PASSWORD, "Password Hygiene"),
        (PHISHING, "Phishing & Social Engineering"),
        (SAFE_BROWSING, "Safe Browsing & Public Wi-Fi"),
    ]
