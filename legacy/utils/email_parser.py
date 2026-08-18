from email import policy
from email.parser import Parser
from typing import Dict


def parse_email(raw_email: str) -> Dict:
    """Parses a raw email string and extracts metadata and plain text body."""

    msg = Parser(policy=policy.default).parsestr(raw_email)

    return {
        "from": msg["From"],
        "to": msg["To"],
        "date": msg["Date"],
        "subject": msg["Subject"],
        "body": msg.get_body(preferencelist=('plain')).get_content() if msg.is_multipart() else msg.get_content(),
    }
