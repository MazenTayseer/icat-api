from setup import django_setup

django_setup()

from apps.dal.models import PhishingScenario, Simulation

SCENARIOS = [
    {
        "tag": "vpn_reset",
        "name": "VPN Reset",
        "subject": "URGENT: VPN password reset required",
        "seed": """
Write a professional phishing email that appears to come from the company
IT help desk. Goal: make the user click a "Reset VPN Password" button
today. Tone: polite urgency, reference security audit, use first name
placeholder <<NAME>> in greeting. Return ONLY the raw HTML for the email
body (120–160 words) with a single <b>Reset Now</b> button—no markdown or
explanations.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    },
    {
        "tag": "account_reauth",
        "name": "Account Reauthentication",
        "subject": "Session expired – re-authenticate your corporate account",
        "seed": """
Compose a friendly but time-sensitive email telling the employee their
single-sign-on session expired and they must sign in again to avoid
interruption. Use <<NAME>> in the salutation. Add one sentence referencing
a routine update. Include a single <b>Sign In</b> button.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    },
    {
        "tag": "payroll_update",
        "name": "Payroll Update",
        "subject": "Action needed: Payroll information verification",
        "seed": """
Craft a realistic email from the HR payroll department asking the employee
to verify direct-deposit details before the upcoming payday. Friendly but
official tone. Use <<NAME>> as greeting. Mention "bi-annual payroll audit".
Include one <b>Verify Details</b> button.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    },
    {
        "tag": "onedrive_share",
        "name": "OneDrive Share",
        "subject": "<<NAME>>, a file has been shared with you on OneDrive",
        "seed": """
Write a convincing share-notification that looks like Microsoft OneDrive.
It should say a "2025 Q3 Budget.xlsx" file was shared and needs review.
Short and corporate, blue accent links. Greeting uses <<NAME>>. Single
<b>Open Document</b> button.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    },
    {
        "tag": "tax_compliance",
        "name": "Tax Compliance",
        "subject": "Important: Digital tax form signature required",
        "seed": """
Create an urgent but polite email from "Finance Compliance" stating that
new digital tax forms must be signed to avoid reporting delays. Salutation
with <<NAME>>. Reference internal memo #2025-TX-17. Provide a single
<b>Review Form</b> button.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    },
    {
        "tag": "benefits_enroll",
        "name": "Benefits Enrollment",
        "subject": "Open enrollment closes Friday – confirm your selections",
        "seed": """
Draft a benefits-team email reminding employees that open enrollment ends
this week. Encourage them to confirm health-plan selections. Friendly,
HR-style language. Use <<NAME>>. Include one <b>Confirm Enrollment</b>
button.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    },
    {
        "tag": "license_termination",
        "name": "License Termination",
        "subject": "Software license termination notice – immediate action required",
        "seed": """
Write a slightly technical email pretending to be from the "Software Asset
Management" team warning that the employee's Adobe Creative Cloud license
will be terminated unless they re-validate their account. Greeting uses
<<NAME>>. One <b>Re-Validate License</b> button.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    },
    {
        "tag": "parcel_delivery",
        "name": "Parcel Delivery",
        "subject": "Package held at customs – confirm shipping fee",
        "seed": """
Compose an email that appears to come from an international parcel service
claiming a package for <<NAME>> is on hold because a small customs fee is
unpaid. Friendly but urgent tone ("will be returned in 48 hrs"). Include a
single <b>Pay Fee</b> button.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    },
    {
        "tag": "calendar_update",
        "name": "Calendar Update",
        "subject": "<<NAME>>, meeting time changed – please reconfirm",
        "seed": """
Create an Outlook-style meeting update stating that tomorrow's "Project
Sync" has moved from 3 pm to 1 pm. Ask the attendee to reconfirm via the
updated invitation. Greeting with <<NAME>>. One <b>Accept New Time</b>
button.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    },
    {
        "tag": "teams_voicemail",
        "name": "Teams Voicemail",
        "subject": "You have 1 unread Teams voicemail",
        "seed": """
Generate a Microsoft Teams notification email telling <<NAME>> they missed
a voicemail from an internal extension. Instruct them to click to listen.
Brief, corporate Teams styling. Single <b>Play Voicemail</b> button.
Return ONLY the raw HTML for the email body, with no explanation or markdown fence.
""".strip()
    }
]

if __name__ == "__main__":
    simulation, _ = Simulation.objects.get_or_create(
        name="Phishing",
        defaults={'name': "Phishing"}
    )

    print("Created new Phishing simulation")

    PhishingScenario.objects.filter(simulation=simulation).delete()
    print("Cleared existing phishing scenarios")

    scenarios_created = 0
    for scenario_data in SCENARIOS:
        PhishingScenario.objects.create(
            simulation=simulation,
            name=scenario_data["name"],
            tag=scenario_data["tag"],
            subject=scenario_data["subject"],
            seed=scenario_data["seed"]
        )
        scenarios_created += 1

    print(f"Successfully created {scenarios_created} phishing scenarios")
    print("Database populated successfully")
