import os

import gradio as gr
from dotenv import load_dotenv

from app.constants import ROLE_PLACEHOLDER
from app.utils import copy_to_clipboard, export_state
from linkedinadvice.career_analysis import CareerAnalyzer
from linkedinadvice.monitoring import monitor_api

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize career analyzer
analyzer = CareerAnalyzer(model_name="gpt-4o-mini")


@monitor_api
def analyze_career(
    *args,
):
    result = analyzer.analyze(*args)

    return result


# Building the interface
with gr.Blocks(theme="soft") as demo:
    # State for number of roles
    role_count = gr.State(1)  # Start with 1 role field
    education_count = gr.State(1)  # Start with 1 education field
    professional_background_dict = gr.State({})  # State to store combined roles data
    education_background_dict = gr.State({})  # State to store combined education data
    professional_background = gr.State("")  # State to store combined roles data
    professional_achievements = gr.State("")  # State to store combined roles data
    education_background = gr.State("")  # State to store combined education background
    education_achievements = gr.State("")  # State to store education achievements
    goals = gr.State("")  # State to store combined goals
    insights = gr.State("")  # State to store combined insights
    time_preference = gr.State("Mid-term (10 years)")  # State to store time preference
    financial_weight = gr.State(2)  # State to store financial weight
    impact_weight = gr.State(2)  # State to store impact weight
    opportunity_weight = gr.State(2)  # State to store opportunity weight
    output = gr.State("")  # State to store output
    raw_list_inputs = gr.State([])  # State to store raw list inputs

    gr.Markdown(
        """
        # Career Pathway Analysis
        
        This tool analyzes your professional background and provides tailored career path recommendations.
        It evaluates options based on financial potential, human impact, and opportunity creation.
        """
    )

    with gr.Row():
        submit_btn = gr.Button("Analyze Career Paths", variant="primary", size="lg")
        clear_btn = gr.Button("Clear", variant="stop", size="lg")
        example_btn = gr.Button("Load Example", variant="secondary", size="lg")

    with gr.Row():
        with gr.Column(scale=3):
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

                @gr.render(inputs=role_count)
                def render_roles(r_count):
                    for i in range(r_count):
                        if i not in professional_background_dict.value:
                            professional_background_dict.value[i] = {
                                "role": "",
                                "exp": "",
                                "professional_achievement": "",
                            }
                        with gr.Row():
                            interactive = i == r_count - 1
                            role = gr.Textbox(
                                key=f"role_{i}",
                                label=f"Role {i + 1}"
                                + (" (Current)" if i == 0 else ""),
                                placeholder=ROLE_PLACEHOLDER[i % len(ROLE_PLACEHOLDER)],
                                scale=3,
                                interactive=interactive,
                                inputs=professional_background_dict.value[i].get(
                                    "role", ""
                                ),
                            )

                            def update_professional_background_dict(key, value, i):
                                professional_background_dict.value[i][key] = value
                                final_string = ""
                                for i in professional_background_dict.value:
                                    role = professional_background_dict.value[i].get(
                                        "role"
                                    )
                                    exp = professional_background_dict.value[i].get(
                                        "exp"
                                    )
                                    professional_achievement = (
                                        professional_background_dict.value[i].get(
                                            "professional_achievement"
                                        )
                                    )
                                    final_string += f"{role} - {exp} years. Achieved: \n{professional_achievement}\n\n"

                                return professional_background_dict.value, final_string

                            role.input(
                                lambda x: update_professional_background_dict(
                                    "role", x, i
                                ),
                                inputs=[role],
                                outputs=[
                                    professional_background_dict,
                                    professional_background,
                                ],
                            )

                            exp = gr.Number(
                                key=f"exp_{i}",
                                label="Years",
                                value=1,
                                minimum=0,
                                scale=1,
                                interactive=interactive,
                            )
                            exp.input(
                                lambda x: update_professional_background_dict(
                                    "exp", x, i
                                ),
                                inputs=[exp],
                                outputs=[
                                    professional_background_dict,
                                    professional_background,
                                ],
                            )

                        professional_achievement = gr.Textbox(
                            key=f"professional_achievement_{i}",
                            label="Notable Achievements",
                            lines=2,
                            placeholder="List key accomplishments, awards, or significant contributions.",
                            interactive=interactive,
                        )

                        professional_achievement.input(
                            lambda x: update_professional_background_dict(
                                "professional_achievement", x, i
                            ),
                            inputs=[professional_achievement],
                            outputs=[
                                professional_background_dict,
                                professional_background,
                            ],
                        )

                        raw_list_inputs.value.extend(
                            [role, exp, professional_achievement]
                        )

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

                @gr.render(inputs=education_count)
                def render_education(e_count):
                    for i in range(e_count):
                        if i not in education_background_dict.value:
                            education_background_dict.value[i] = {
                                "education": "",
                                "education_achievement": "",
                            }
                        with gr.Row():
                            education = gr.Textbox(
                                key=f"education_{i}",
                                label="Academic Experience",
                                lines=3,
                                placeholder="e.g. Bachelor of Science in Computer Science, University of Technology",
                            )

                            def update_educational_background_dict(key, value, i):
                                education_background_dict.value[i][key] = value
                                final_string = ""
                                for i in education_background_dict.value:
                                    education = education_background_dict.value[i].get(
                                        "education"
                                    )
                                    edu_achievement = education_background_dict.value[
                                        i
                                    ].get("edu_achievement")
                                    final_string += f"{education}. Achieved: \n{edu_achievement}\n\n"

                                return education_background_dict.value, final_string

                            education.input(
                                lambda x: update_educational_background_dict(
                                    "education", x, i
                                ),
                                inputs=[education],
                                outputs=[
                                    education_background_dict,
                                    education_background,
                                ],
                            )

                            edu_achievement = gr.Textbox(
                                key=f"edu_achievement_{i}",
                                label="Academic Achievements",
                                lines=3,
                                placeholder="Awards, honors, notable projects or research during your education",
                            )

                            edu_achievement.input(
                                lambda x: update_educational_background_dict(
                                    "education_achievement", x, i
                                ),
                                inputs=[education_achievements],
                                outputs=[
                                    education_background_dict,
                                    education_background,
                                ],
                            )

                        if education.value:
                            education_background.value += education.value
                        if edu_achievement.value:
                            education_achievements.value += edu_achievement.value

                        raw_list_inputs.value.extend([education, edu_achievement])

            with gr.Group():
                gr.Markdown("### Future Plans")
                goals = gr.Textbox(
                    label="Career Goals",
                    lines=3,
                    placeholder="Describe your short-term and long-term career objectives",
                    key="goals",
                )

                insights = gr.Textbox(
                    label="Additional Insights",
                    lines=3,
                    placeholder="Other relevant information like skills, interests, or constraints",
                    key="insights",
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
                    key="time_preference",
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        financial_weight = gr.Radio(
                            [1, 2, 3],
                            value=2,
                            label="💰 Financial Potential",
                            info="Earning potential and financial growth",
                            elem_classes=["weight-radio"],
                            key="financial_weight",
                        )
                    with gr.Column(scale=1):
                        impact_weight = gr.Radio(
                            [1, 2, 3],
                            value=2,
                            label="💫 Human Impact",
                            info="Positive impact on others and society",
                            elem_classes=["weight-radio"],
                            key="impact_weight",
                        )
                    with gr.Column(scale=1):
                        opportunity_weight = gr.Radio(
                            [1, 2, 3],
                            value=2,
                            label="🚪 Opportunity Creation",
                            info="Doors opened for future growth and options",
                            elem_classes=["weight-radio"],
                            key="opportunity_weight",
                        )

        with gr.Column(scale=2):
            output_box = gr.Markdown(
                output.value,
                label="Career Analysis Report",
                container=True,
                height=614,
                show_copy_button=False,
            )

            with gr.Row():
                copy_btn = gr.Button("📋 Copy to Clipboard", variant="secondary")
                share_btn = gr.Button("🔗 Share on LinkedIn", variant="secondary")

                # Copy and share functionality
                copy_btn.click(
                    copy_to_clipboard,
                    inputs=output_box,
                )

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

    submit_btn.click(
        lambda *args: analyze_career(*args) if export_state(*args) or True else None,
        inputs=[
            professional_background,
            education_background,
            goals,
            insights,
            time_preference,
            financial_weight,
            impact_weight,
            opportunity_weight,
        ],
        outputs=[output_box],
    )

    clear_btn.click(
        fn=lambda: None, inputs=[], outputs=[], js="() => location.reload()"
    )

    """ 
    example_btn.click(
        fn=lambda _: SAMPLE_RESULT,
        inputs=[output_box],
        outputs=[output_box],
    )
     """

# Launch the app
if __name__ == "__main__":
    demo.launch()
