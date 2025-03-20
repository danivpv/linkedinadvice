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

    def analyze(self, user_data, time_preference, scoring_weights=None):
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

        # Prepare consolidated insights
        insights = user_data.get("insights", "")

        if user_data.get("prev_roles"):
            insights += f"\nPrevious Roles: {user_data['prev_roles']}"

        if user_data.get("edu_achievements"):
            insights += f"\nEducational Achievements: {user_data['edu_achievements']}"

        if user_data.get("include_novel_options"):
            insights += "\nPlease include novel or unconventional career paths in your analysis."

        # Create the prompt
        prompt = f"""Analyze the following career profile and generate a taxonomy of potential career paths:

Current Role: {user_data.get("current_role", "")}
Years of Experience: {user_data.get("experience", "")}
Notable Achievements: {user_data.get("achievements", "")}
Education: {user_data.get("education", "")}
Career Goals: {user_data.get("goals", "")}
Additional Insights: {insights}
Time Preference: {time_preference}

Generate 5 potential career paths that align with this profile. For each path, evaluate:
1. Financial potential (scale 1-10) at 3, 10, and 10+ years
2. Human impact potential (scale 1-10) at 3, 10, and 10+ years
3. Opportunity creation potential (scale 1-10) at 3, 10, and 10+ years

Show your reasoning for each score. 

Then calculate a weighted average based on the following weights:
- Financial: {scoring_weights[0]}
- Human Impact: {scoring_weights[1]}
- Opportunity Creation: {scoring_weights[2]}

And the time preference: {time_preference}

Format the output clearly with sections for each career path, the scoring breakdown, and a final recommendation section ranking the paths from highest to lowest score.
"""

        try:
            # Make the API call
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a career advisor specialized in professional path analysis.",
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
