from html import escape

def format_projects(projects):
    if not projects:
        return "<b>My projects</b>\nNo projects yet."
    lines = ["<b>My projects</b>"]
    for i,p in enumerate(projects, 1):
        lines.append(f"\n{i}. <b>{escape(p.title)}</b>\n{escape(p.description)}")
        if p.url:
            lines.append(f"<a href='{escape(p.url)}'>Link</a>")
    return "\n".join(lines)

MENU_TEXT = "Choose a section:"

ABOUT_TEXT = (
    "Hello! My name is Matthew.\n"
    "I'm studying at university and I love to create bots.\n"
    "I have experience in Python."
)

PROJECTS_TEXT = "<b>My projects</b>\n• Business card bot (this one)"

CONTACTS_TEXT = "Contacts:"

HELP_TEXT = (
    "I'm Matthew's business card bot.\n"
    "Available commands:\n"
    "/start - Start the bot\n"
    "/menu - Main menu\n"
    "/about - About me\n"
    "/projects - My projects\n"
    "/contacts - Contacts"
)

UNKNOWN_TEXT = "I don't understand. Press /start or /menu."

FEEDBACK_ASK = "Write your message and I will pass it to Matthew. Text only."