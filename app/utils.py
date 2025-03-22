"""
Utility functions for the LinkedIn Career Advice application.
Handles input processing, clipboard operations, and sharing functionality.
"""

import pyperclip


def copy_to_clipboard(text):
    """Copy text to clipboard"""
    if not pyperclip.is_available():
        print("Clipboard is not available on this system")
        return None
    pyperclip.copy(text)
    return None


def export_state(
    professional_background,
    education_background,
    goals,
    insights,
    time_preference,
    financial_weight,
    impact_weight,
    opportunity_weight,
) -> str:
    state_dict = {
        "Professional Background": professional_background,
        "Education Background": education_background,
        "Goals": goals,
        "Insights": insights,
        "Time Preference": time_preference,
        "Financial Weight": financial_weight,
        "Impact Weight": impact_weight,
        "Opportunity Weight": opportunity_weight,
    }

    formatted_output = "\n".join(f"{key}: {value}" for key, value in state_dict.items())

    return formatted_output
