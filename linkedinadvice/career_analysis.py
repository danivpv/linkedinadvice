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

    def analyze(self, user_data):
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
        if scoring_weights is None:
            scoring_weights = [
                0.33,
                0.33,
                0.34,
            ]  # Slightly more on opportunity to sum to 1.0

        # Parse the roles data to extract current role and experience
        roles_list = user_data.get("roles", "").split("\n")

        # Identify current role (first one in the list)
        current_role = ""
        current_experience = 0
        if roles_list and roles_list[0]:
            parts = roles_list[0].split(" (")
            if len(parts) == 2:
                current_role = parts[0]
                exp_part = parts[1].split(" years")[0]
                try:
                    current_experience = int(exp_part)
                except ValueError:
                    current_experience = 0

        # Format previous roles (all except the first one)
        prev_roles_str = ", ".join(roles_list[1:]) if len(roles_list) > 1 else ""

        # Create the prompt with all available information
        prompt = f"""Analyze the following career profile and generate a taxonomy of potential career paths:

Current Role: {current_role}
Years in Current Role: {current_experience}
"""

        # Add previous roles if present
        if prev_roles_str:
            prompt += f"Previous Roles: {prev_roles_str}\n"

        # Add all the fields from user_data
        prompt += f"""Professional Achievements: {user_data.get("achievements", "")}
Educational Background: {user_data.get("educations", "")}
Educational Achievements: {user_data.get("edu_achievements", "")}
Career Goals: {user_data.get("goals", "")}
Additional Insights: {user_data.get("insights", "")}

Time Preference: {user_data.get("time_preference")}
Financial Weight: {user_data.get("financial_weight", scoring_weights[0])}
Impact Weight: {user_data.get("impact_weight", scoring_weights[1])}
Opportunity Weight: {user_data.get("opportunity_weight", scoring_weights[2])}

Generate 5 potential career paths that align with this profile. For each path, evaluate:
1. Financial potential (scale 1-10) at 3, 10, and 10+ years
2. Human impact potential (scale 1-10) at 3, 10, and 10+ years
3. Opportunity creation potential (scale 1-10) at 3, 10, and 10+ years

Show your reasoning for each score. 

Then calculate a weighted average based on the following weights:
- Financial: {scoring_weights[0]}
- Human Impact: {scoring_weights[1]}
- Opportunity Creation: {scoring_weights[2]}

And the time preference: {user_data.get("time_preference")}

Format the output clearly with sections for each career path, the scoring breakdown, and a final recommendation section ranking the paths from highest to lowest score.
"""

        # Add novel paths instruction if requested
        if user_data.get("include_novel_options"):
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
