import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class CareerAnalyzer:
    """Handles career path analysis using OpenAI models"""

    def __init__(self, model_name="gpt-4o-mini", temperature=0.0):
        """Initialize with the specified model parameters"""
        self.model_name = model_name
        self.temperature = temperature

    def analyze(
        self,
        professional_background,
        education_background,
        goals,
        insights,
        time_preference,
        financial_weight,
        impact_weight,
        opportunity_weight,
    ):
        """
        Analyze career paths based on user data

        Args:
            user_data (dict): User career information
            time_preference (str): User's time horizon preference
            scoring_weights (list): Weights for financial, impact, and opportunity metrics

        Returns:
            str: Formatted analysis results
        """
        # Use default equal weights if none provided
        current_role = professional_background.split("\n\n")[0]
        previous_roles = "\n\n".join(professional_background.split("\n\n")[1:])


        # Create the prompt with all available information
        prompt = f"""Analyze the following career profile and generate a taxonomy of potential career paths:

Current Role: {current_role}
"""

        # Add previous roles if present
        if previous_roles:
            prompt += f"Previous Roles: {previous_roles}\n"

        # Add all the fields from user_data
        prompt += f"""
Educational Background: {education_background}
Career Goals: {goals}
Additional Insights: {insights}

Time Preference: {time_preference}
Financial Weight: {financial_weight}
Impact Weight: {impact_weight}
Opportunity Weight: {opportunity_weight}

Help me as an expert career advisor. Provide a taxonomy to generate promising career paths on the timescale of {time_preference} and rate them them based on success on the short, medium and long term. For each path, evaluate:
1. Financial potential (scale 1-3) at 3, 10, and 10+ years
2. Human impact potential (scale 1-3) at 3, 10, and 10+ years
3. Opportunity creation potential (scale 1-3) at 3, 10, and 10+ years

Show your step by stepreasoning for each score. 

Then calculate an accurate weighted average based on the following weights:
- Financial: {financial_weight}
- Human Impact: {impact_weight}
- Opportunity Creation: {opportunity_weight}

Format the output clearly with sections for each career path, the scoring breakdown, and a final recommendation section ranking the paths from highest to lowest score.
"""

        # Add novel paths instruction if requested
        if False:
            prompt += "\nPlease include at least one novel or unconventional career path in your analysis."

        # Print the prompt for debugging
        print("\n=== CAREER ANALYSIS PROMPT ===\n")
        print(prompt)
        print("\n=== END OF PROMPT ===\n")

        try:
            # Make the API call
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a career advisor specialized in professional path analysis. Your analysis should be comprehensive, data-driven, and tailored to the individual's specific career history and goals.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
            )

            # Extract and return the result
            return response.choices[0].message.content
        except Exception as e:
            # Handle API errors gracefully
            return f"An error occurred during analysis: {str(e)}"
