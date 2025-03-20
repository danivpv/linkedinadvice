import os

import gradio as gr
from dotenv import load_dotenv

from linkedinadvice.career_analysis import CareerAnalyzer
from linkedinadvice.monitoring import monitor_api
from linkedinadvice.utils import copy_to_clipboard, get_share_link

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize career analyzer
analyzer = CareerAnalyzer(model_name="gpt-4o-mini")


@monitor_api
def analyze_career(
    current_role,
    experience,
    prev_roles,
    achievements,
    education,
    edu_achievements,
    goals,
    insights,
    time_preference,
    include_novel_options,
    financial_weight,
    impact_weight,
    opportunity_weight,
):
    # Normalize weights to ensure they sum to 1
    total_weight = financial_weight + impact_weight + opportunity_weight
    if total_weight == 0:
        # If all weights are 0, use equal weights
        weights = [0.33, 0.33, 0.34]
    else:
        weights = [
            financial_weight / total_weight,
            impact_weight / total_weight,
            opportunity_weight / total_weight,
        ]

    # Map time preference radio button to actual preference
    time_map = {
        "Short-term (3 years)": "short-term",
        "Mid-term (10 years)": "mid-term",
        "Long-term (10+ years)": "long-term",
    }

    # Prepare user data
    user_data = {
        "current_role": current_role,
        "experience": experience,
        "prev_roles": prev_roles,
        "achievements": achievements,
        "education": education,
        "edu_achievements": edu_achievements,
        "goals": goals,
        "insights": insights,
        "include_novel_options": include_novel_options,
    }

    # Get analysis
    result = analyzer.analyze(
        user_data=user_data,
        time_preference=time_map.get(time_preference, "balanced"),
        scoring_weights=weights,
    )

    return result


def share_to_linkedin(text):
    """Generate a LinkedIn sharing link"""
    share_link = get_share_link(text)
    return f"Share on LinkedIn: {share_link}"


# Building the interface
with gr.Blocks(theme="soft") as demo:
    gr.Markdown("# Career Pathway Analysis")

    with gr.Row():
        with gr.Column():
            with gr.Group():
                gr.Markdown("### Professional Information")
                current_role = gr.Textbox(label="Current Role")
                experience = gr.Number(label="Years of Experience", value=0)
                prev_roles = gr.Textbox(label="Previous Roles (optional)")
                achievements = gr.Textbox(label="Notable Achievements", lines=3)

            with gr.Group():
                gr.Markdown("### Educational Background")
                education = gr.Textbox(label="Academic Experience")
                edu_achievements = gr.Textbox(label="Academic Achievements", lines=3)

            with gr.Group():
                gr.Markdown("### Future Plans")
                goals = gr.Textbox(label="Career Goals", lines=3)
                insights = gr.Textbox(label="Additional Insights", lines=3)

            with gr.Group():
                gr.Markdown("### Analysis Preferences")
                time_preference = gr.Radio(
                    [
                        "Short-term (3 years)",
                        "Mid-term (10 years)",
                        "Long-term (10+ years)",
                    ],
                    label="Time Horizon Preference",
                    value="Mid-term (10 years)",
                )

                include_novel = gr.Checkbox(
                    label="Include novel/unconventional career options"
                )

                gr.Markdown("### Scoring Weights")
                financial_weight = gr.Slider(
                    minimum=0, maximum=10, value=5, step=1, label="Financial Potential"
                )
                impact_weight = gr.Slider(
                    minimum=0, maximum=10, value=5, step=1, label="Human Impact"
                )
                opportunity_weight = gr.Slider(
                    minimum=0, maximum=10, value=5, step=1, label="Opportunity Creation"
                )

            submit_btn = gr.Button("Analyze Career Paths", variant="primary")

        with gr.Column():
            output = gr.Textbox(label="Career Analysis Report", lines=25)

            with gr.Row():
                copy_btn = gr.Button("Copy to Clipboard")
                share_btn = gr.Button("Share on LinkedIn")

            share_output = gr.Textbox(label="Share Link", visible=False)

    # Set up event handlers
    submit_btn.click(
        analyze_career,
        inputs=[
            current_role,
            experience,
            prev_roles,
            achievements,
            education,
            edu_achievements,
            goals,
            insights,
            time_preference,
            include_novel,
            financial_weight,
            impact_weight,
            opportunity_weight,
        ],
        outputs=output,
    )

    # Copy and share functionality
    copy_btn.click(
        copy_to_clipboard,
        inputs=output,
        outputs=gr.Textbox(value="Copied to clipboard!"),
    )
    share_btn.click(share_to_linkedin, inputs=output, outputs=share_output)
    share_btn.click(
        lambda: True,
        None,
        share_output,
        js="(x) => {share_output.style.display = 'block';}",
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()
