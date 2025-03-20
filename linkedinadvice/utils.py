import re

import pyperclip


def copy_to_clipboard(text):
    """Copy text to clipboard"""
    pyperclip.copy(text)
    return "Report copied to clipboard!"


def format_for_linkedin(text):
    """Format analysis for LinkedIn sharing"""
    # Extract just the summary/conclusion part to keep LinkedIn share concise
    conclusion_match = re.search(
        r"(?:Conclusion|Final Recommendation).*?:(.*?)(?=$)", text, re.DOTALL
    )

    if conclusion_match:
        conclusion = conclusion_match.group(1).strip()
        formatted = "I received this career path analysis insight:\n\n" + conclusion
        return formatted[:500] + "..." if len(formatted) > 500 else formatted

    # Fallback if no conclusion section found
    shortened = text[:500] + "..." if len(text) > 500 else text
    return "Career Path Analysis Results:\n\n" + shortened


def get_share_link(text):
    """Generate LinkedIn share link"""
    formatted_text = format_for_linkedin(text)
    encoded_text = formatted_text.replace(" ", "%20").replace("\n", "%0A")
    return f"https://www.linkedin.com/sharing/share-offsite/?url=https://huggingface.co/spaces/YourUsername/career-advisor&title=Career%20Path%20Analysis&summary={encoded_text}"
