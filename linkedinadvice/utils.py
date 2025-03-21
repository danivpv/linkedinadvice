"""
Utility functions for the LinkedIn Career Advice application.
Handles input processing, clipboard operations, and sharing functionality.
"""

import re
import urllib.parse


def combine_roles(count, *args):
    """
    Combine roles and experience into a formatted string.

    Args:
        count (int): Number of roles to process
        *args: List of alternating role names and experience years

    Returns:
        str: Formatted string of roles with experience years
    """
    roles_text = ""

    for i in range(count):
        # Calculate the index in args for this role's name and experience
        name_idx = i
        exp_idx = i + count // 2 + 1

        if name_idx < len(args) and exp_idx < len(args):
            role_name = args[name_idx]
            experience = args[exp_idx]

            if role_name and experience is not None:
                roles_text += f"{role_name} ({experience} years)\n"

    return roles_text.strip()


def share_to_linkedin(text):
    """Generate a LinkedIn sharing link"""
    share_link = get_share_link(text)
    return f"Share on LinkedIn: {share_link}"


def combine_text_fields(text_list):
    """
    Combine multiple text fields into a single string, separated by newlines.
    Filters out any empty inputs.

    Args:
        text_list (list): List of text strings to combine

    Returns:
        str: Combined string with entries separated by double newlines
    """
    return "\n\n".join([text for text in text_list if text])


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
    """
    Generate a LinkedIn sharing link with the provided text.

    Args:
        text (str): Text to share on LinkedIn

    Returns:
        str: URL for sharing on LinkedIn
    """
    # Create a shortened version for sharing (LinkedIn has character limits)
    summary = text[:500] + "..." if len(text) > 500 else text

    # Get the LinkedIn sharing URL with the text encoded
    base_url = "https://www.linkedin.com/sharing/share-offsite/"
    params = {
        "url": "https://huggingface.co/spaces/LinkedIn-Advice/career-path-advisor",
        "title": "My Career Path Analysis",
        "summary": summary,
    }

    share_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return share_url


def process_input_data(
    role_count, roles_and_exps, achievements, educations, edu_achievements
):
    # Process roles and experience
    roles_data = combine_roles(role_count, *roles_and_exps)

    # Process achievements, education, and educational achievements
    achievements_data = combine_text_fields(achievements)
    education_data = combine_text_fields(educations)
    edu_achievements_data = combine_text_fields(edu_achievements)

    print(roles_data)
    print(achievements_data)
    print(education_data)
    print(edu_achievements_data)

    return roles_data, achievements_data, education_data, edu_achievements_data


def copy_to_clipboard(text):
    pass
