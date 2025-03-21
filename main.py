import os

import gradio as gr
from dotenv import load_dotenv

from linkedinadvice.career_analysis import CareerAnalyzer
from linkedinadvice.monitoring import monitor_api
from linkedinadvice.utils import (
    copy_to_clipboard,
    process_input_data,
    share_to_linkedin,
)

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize career analyzer
analyzer = CareerAnalyzer(model_name="gpt-4o-mini")

ROLE_PLACEHOLDER = [
    "e.g. Software Engineer",
    "e.g. Product Manager",
    "e.g. Senior Software Engineer",
    "e.g. Director of Engineering",
    "e.g. Chief Technology Officer",
    "e.g. QA Engineer",
    "e.g. DevOps Engineer",
    "e.g. Cloud Engineer",
    "e.g. Security Engineer",
    "e.g. Site Reliability Engineer",
    "e.g. Infrastructure Engineer",
]


@monitor_api
def analyze_career(
    roles_data,
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
        "roles": roles_data,
        "achievements": achievements,
        "educations": education,
        "edu_achievements": edu_achievements,
        "goals": goals,
        "insights": insights,
        "time_preference": time_preference,
        "financial_weight": financial_weight,
        "impact_weight": impact_weight,
        "opportunity_weight": opportunity_weight,
        "include_novel_options": include_novel_options,
    }

    # Get analysis
    result = analyzer.analyze(
        user_data=user_data,
        time_preference=time_map.get(time_preference, "balanced"),
        scoring_weights=weights,
    )

    return result


# Building the interface
with gr.Blocks(theme="soft") as demo:
    gr.Markdown(
        """
        # Career Pathway Analysis
        
        This tool analyzes your professional background and provides tailored career path recommendations.
        It evaluates options based on financial potential, human impact, and opportunity creation.
        """
    )
    with gr.Row():
        submit_btn = gr.Button("Analyze Career Paths", variant="primary", size="lg")
        clear_btn = gr.Button("Clear All", variant="stop", size="lg")
        example_btn = gr.Button("Load Example", variant="secondary", size="lg")

    # State for number of roles
    role_count = gr.State(1)  # Start with 1 role field
    education_count = gr.State(1)  # Start with 1 education field
    roles_data = gr.State("")  # State to store combined roles data
    exps_data = gr.State("")  # State to store combined experiences
    achievements_data = gr.State("")  # State to store combined achievements
    educations_data = gr.State("")  # State to store combined educations
    edu_achievements_data = gr.State("")  # State to store combined edu achievements

    @gr.render(inputs=[role_count, education_count])
    def render_roles(r_count, e_count):
        with gr.Row():
            with gr.Column(scale=3):
                roles = []
                exps = []
                achievements = []
                educations = []
                edu_achievements = []

                with gr.Group():
                    gr.Markdown("### Professional Information")
                    gr.Markdown("*Add your current and previous professional roles*")
                    with gr.Row():
                        add_role_btn = gr.Button(
                            "➕ Add", variant="secondary", size="sm", key="add_role_btn"
                        )
                        remove_role_btn = gr.Button(
                            "➖ Remove",
                            variant="secondary",
                            size="sm",
                            key="remove_role_btn",
                        )
                    for i in range(r_count):
                        with gr.Row():
                            role = gr.Textbox(
                                key=f"role_{i}",
                                label=f"Role {i + 1}"
                                + (" (Current)" if i == 0 else ""),
                                placeholder=ROLE_PLACEHOLDER[i % len(ROLE_PLACEHOLDER)],
                                scale=3,
                            )
                            exp = gr.Number(
                                key=f"exp_{i}",
                                label="Years",
                                value=1,
                                minimum=0,
                                scale=1,
                            )

                        achievement = gr.Textbox(
                            key=f"achievement_{i}",
                            label="Notable Achievements",
                            lines=2,
                            placeholder="List key accomplishments, awards, or significant contributions.",
                        )
                        roles.append(role)
                        exps.append(exp)
                        achievements.append(achievement)

                with gr.Group():
                    gr.Markdown("### Educational Background")
                    gr.Markdown("*Add your current and previous academic experiences*")
                    with gr.Row():
                        add_education_btn = gr.Button(
                            "➕ Add",
                            variant="secondary",
                            size="sm",
                            key="add_education_btn",
                        )
                        remove_education_btn = gr.Button(
                            "➖ Remove",
                            variant="secondary",
                            size="sm",
                            key="remove_education_btn",
                        )
                    for i in range(e_count):
                        with gr.Row():
                            education = gr.Textbox(
                                key=f"education_{i}",
                                label="Academic Experience",
                                lines=3,
                                placeholder="e.g. Bachelor of Science in Computer Science, University of Technology",
                            )
                            edu_achievement = gr.Textbox(
                                key=f"edu_achievement_{i}",
                                label="Academic Achievements",
                                lines=3,
                                placeholder="Awards, honors, notable projects or research during your education",
                            )
                        educations.append(education)
                        edu_achievements.append(edu_achievement)

                add_education_btn.click(
                    lambda x: x + 1,
                    inputs=[education_count],
                    outputs=[education_count],
                )

                remove_education_btn.click(
                    lambda x: max(x - 1, 1),
                    inputs=[education_count],
                    outputs=[education_count],
                )

                add_role_btn.click(
                    lambda x: x + 1,
                    inputs=[role_count],
                    outputs=[role_count],
                )

                remove_role_btn.click(
                    lambda x: max(x - 1, 1),
                    inputs=[role_count],
                    outputs=[role_count],
                )

                with gr.Group():
                    gr.Markdown("### Future Plans")
                    goals = gr.Textbox(
                        label="Career Goals",
                        lines=3,
                        placeholder="Describe your short-term and long-term career objectives",
                    )
                    insights = gr.Textbox(
                        label="Additional Insights",
                        lines=3,
                        placeholder="Other relevant information like skills, interests, or constraints",
                    )

                with gr.Group():
                    gr.Markdown("### Analysis Preferences")
                    gr.Markdown(
                        "*Adjust the importance of each factor in career evaluation*"
                    )

                    time_preference = gr.Radio(
                        [
                            "Short-term (3 years)",
                            "Mid-term (10 years)",
                            "Long-term (10+ years)",
                        ],
                        label="Time Horizon Preference",
                        value="Mid-term (10 years)",
                    )

                    with gr.Row():
                        with gr.Column(scale=1):
                            financial_weight = gr.Radio(
                                [1, 2, 3],
                                value=2,
                                label="💰 Financial Potential",
                                info="Earning potential and financial growth",
                                elem_classes=["weight-radio"],
                            )
                        with gr.Column(scale=1):
                            impact_weight = gr.Radio(
                                [1, 2, 3],
                                value=2,
                                label="💫 Human Impact",
                                info="Positive impact on others and society",
                                elem_classes=["weight-radio"],
                            )
                        with gr.Column(scale=1):
                            opportunity_weight = gr.Radio(
                                [1, 2, 3],
                                value=2,
                                label="🚪 Opportunity Creation",
                                info="Doors opened for future growth and options",
                                elem_classes=["weight-radio"],
                            )

            with gr.Column(scale=2):
                output = gr.Textbox(label="Career Analysis Report", lines=25)

                with gr.Row():
                    copy_btn = gr.Button("📋 Copy to Clipboard", variant="secondary")
                    share_btn = gr.Button("🔗 Share on LinkedIn", variant="secondary")

                share_output = gr.Textbox(label="Share Link", visible=False)

                # Add info section at the bottom
                with gr.Accordion("About This Tool", open=False):
                    gr.Markdown(
                        """
                        This career analysis tool uses AI to generate personalized career path recommendations 
                        based on your professional background, education, and goals.
                        
                        **How It Works:**
                        1. Enter your current and previous roles with years of experience
                        2. Provide information about your achievements and education
                        3. Set your preferences for analysis (time horizon and factor weights)
                        4. Get a detailed analysis of potential career paths with scoring
                        
                        The analysis evaluates each career path on three dimensions:
                        - **Financial Potential**: Earning capacity and financial growth
                        - **Human Impact**: Contribution to society and positive influence
                        - **Opportunity Creation**: Future opportunities and career flexibility
                        
                        You can adjust the weights to prioritize what matters most to you.
                        """
                    )

        # Set up main submit handler
        submit_btn.click(
            fn=lambda *args: process_input_data(
                r_count,
                args[: r_count * 2],  # roles and exps
                args[r_count * 2 : r_count * 3],  # achievements
                args[r_count * 3 : r_count * 3 + e_count],  # educations
                args[r_count * 3 + e_count :],  # edu achievements
            ),
            inputs=[*roles, *exps, *achievements, *educations, *edu_achievements],
            outputs=[
                roles_data,
                achievements_data,
                educations_data,
                edu_achievements_data,
            ],
            show_progress=False,
        ).then(
            analyze_career,
            inputs=[
                roles_data,  # Combined roles from the first step
                achievements_data,  # Combined achievements
                educations_data,  # Combined education
                edu_achievements_data,  # Combined educational achievements
                goals,
                insights,
                time_preference,
                financial_weight,
                impact_weight,
                opportunity_weight,
            ],
            outputs=output,
        )

        # Copy and share functionality

        share_btn.click(share_to_linkedin, inputs=output, outputs=share_output)
        share_btn.click(
            lambda: True,
            None,
            share_output,
            js="(x) => {share_output.style.display = 'block';}",
        )

        copy_btn.click(
            copy_to_clipboard,
            inputs=output,
        )


# Launch the app
if __name__ == "__main__":
    demo.launch()
