"""
MindCare Safety & Crisis Guardrail System
Detects acute emotional distress, self-harm signals, and suicidal ideation.
Intercepts requests to immediately provide official verified emergency helplines.
"""

import re
from typing import Tuple, Optional
from app.models.schemas import SafetyAlert, HelplineInfo

CRISIS_PATTERNS = [
    r"\b(suicid\w*|kill(ing)?\s+(my\s*self|myself))\b",
    r"\b(end(ing)?\s+my\s+life|want\s+to\s+die|wish\s+i\s+(were|was)\s+dead)\b",
    r"\b(self[\s\-_]*harm\w*|hurt(ing)?\s+myself|cutt(ing)?\s+myself)\b",
    r"\b(overdos\w*|hang(ing)?\s+myself|slit(ting)?\s+my\s+wrist\w*)\b",
    r"\b(no\s+reason\s+to\s+live|better\s+off\s+dead|can'?t\s+go\s+on\s+anymore)\b",
    r"\b(take\s+my\s+own\s+life|goodbye\s+cruel\s+world)\b",
]

VERIFIED_HELPLINES = [
    HelplineInfo(
        name="Tele-MANAS (Govt of India)",
        number="14416 or 1800-891-4416",
        region="India (National, 24/7, Toll-Free)",
        description="Comprehensive, round-the-clock mental health support service by Ministry of Health and Family Welfare, Govt of India."
    ),
    HelplineInfo(
        name="KIRAN Mental Health Helpline",
        number="1800-599-0019",
        region="India (24/7, Multilingual)",
        description="Ministry of Social Justice and Empowerment crisis helpline providing psychological first-aid."
    ),
    HelplineInfo(
        name="Vandrevala Foundation Helpline",
        number="+91 9999 666 555",
        region="India (24/7 Free Support)",
        description="Experienced mental health counselors available via call and WhatsApp."
    ),
    HelplineInfo(
        name="988 Suicide & Crisis Lifeline",
        number="988 (Call or Text)",
        region="USA & Canada (24/7)",
        description="Free and confidential emotional support to people in suicidal crisis or emotional distress."
    ),
    HelplineInfo(
        name="NHS 111 Mental Health Services",
        number="111",
        region="United Kingdom (24/7)",
        description="Direct triage to local NHS mental health crisis teams."
    ),
    HelplineInfo(
        name="Find A Helpline (Global)",
        number="https://findahelpline.com",
        region="Worldwide Directory",
        description="Free, confidential crisis support services in over 130 countries."
    )
]

STANDARD_DISCLAIMER = (
    "MindCare Signal is an educational wellness and self-reflection platform powered by machine learning and curated health guides. "
    "It is NOT a medical diagnosis, clinical treatment, or crisis intervention service. "
    "If you or someone you know is struggling or in distress, please connect with a qualified mental health professional or emergency helpline immediately."
)


class SafetyGuard:
    def __init__(self):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in CRISIS_PATTERNS]

    def check_text(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Scans input string for crisis indicators.
        Returns: (is_crisis, matched_trigger_word)
        """
        if not text:
            return False, None

        for pattern in self.patterns:
            match = pattern.search(text)
            if match:
                return True, match.group(0)

        return False, None

    def create_crisis_alert(self, trigger: str = "") -> SafetyAlert:
        """
        Creates a structured crisis response, strictly prioritizing student safety.
        """
        message = (
            "You matter, and you do not have to carry this alone. "
            "Please pause and reach out immediately to one of the free, confidential support services below. "
            "Trained, compassionate professionals are available 24/7 to listen and support you."
        )

        return SafetyAlert(
            is_crisis=True,
            trigger_detected=trigger,
            message=message,
            helplines=VERIFIED_HELPLINES,
            medical_disclaimer=STANDARD_DISCLAIMER
        )

    def get_disclaimer(self) -> str:
        return STANDARD_DISCLAIMER


safety_guard = SafetyGuard()
