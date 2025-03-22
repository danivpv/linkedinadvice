# Example data to load when the "Load Example" button is clicked

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

SAMPLE_RESULT = """
Based on the provided career profile, we can identify several potential career paths that align with the individual's experience, skills, and aspirations. 
For each option, I’ll assess its performance in the short, medium, and long term for each criterion. I’ll assign rough scores (1-5, where 1 is low and 5 is high) based on your background and goals, then explain the reasoning.

### Option 1: Pursue a PhD
- **Short-term** (1-3 years):
Financial Success: 2 (Stipends are modest, typically $20K-$40K/year, depending on location and funding.)
Impact on Helping Others: 2 (Focus is on learning and early research, with limited immediate impact.)
Winning Track Record: 3 (You’re building toward a prestigious degree, but no major achievements yet.)
- **Medium-term** (3-10 years):
Financial Success: 4 (Post-PhD, you could secure high-paying roles in industry or academia, e.g., $100K+ in tech.)
Impact on Helping Others: 4 (Research in AI or data science could address significant problems.)
Winning Track Record: 5 (A PhD is a globally recognized achievement, opening doors to elite roles.)
- **Long-term** (10+ years):
Financial Success: 4 (Potential for six-figure salaries in industry or stable academic positions.)
Impact on Helping Others: 5 (Breakthrough research or leadership in impactful projects.)
Winning Track Record: 5 (A PhD can lead to a career of notable contributions.)

### Option 2: Continue in Data Science (Industry)
- **Short-term**:
Financial Success: 4 (With 2 years of experience, you can likely secure $80K-$120K roles.)
Impact on Helping Others: 3 (Depends on projects—e.g., healthcare analytics could be impactful.)
Winning Track Record: 4 (Successful projects or promotions enhance your resume.)
- **Medium-term**:
Financial Success: 4 (Senior roles could exceed $150K with experience.)
Impact on Helping Others: 4 (Leading impactful initiatives becomes possible.)
Winning Track Record: 4 (A string of achievements strengthens your profile.)
- **Long-term**:
Financial Success: 4 (Potential for executive or specialized roles with high pay.)
Impact on Helping Others: 4 (Influence grows with seniority or project scope.)
Winning Track Record: 4 (Consistent success signals expertise.)
**Notes**: Your current path offers stability and growth, leveraging your existing skills and experience.

### Option 3: Switch to Quantitative Finance or Software Engineering
- **Short-term**:
Financial Success: 5 (Entry-level roles in finance or tech often start at $100K+.)
Impact on Helping Others: 3 (Varies—e.g., less direct in finance, more in software for social good.)
Winning Track Record: 3 (You’d need to build new credentials, but your skills transfer well.)
- **Medium-term**:
Financial Success: 5 (High earning potential, e.g., $200K+ in quant finance.)
Impact on Helping Others: 3 (Depends on the role—less predictable than data science.)
Winning Track Record: 4 (Success in these fields is visible and respected.)
- **Long-term**:
Financial Success: 5 (Top earners in these fields can make millions.)
Impact on Helping Others: 3 (Impact varies widely by role.)
Winning Track Record: 4 (Strong achievements possible.)
**Notes**: Switching requires some upskilling, but your math and programming background make it feasible.

### Option 4: Entrepreneurship
- **Short-term**:
Financial Success: 1 (High risk—little to no income initially.)
Impact on Helping Others: 4 (A venture solving real problems could have early impact.)
Winning Track Record: 4 (Starting something is notable, even if small-scale.)
- **Medium-term**:
Financial Success: 3 (Success could yield moderate to high returns; failure is common.)
Impact on Helping Others: 5 (A thriving business could scale solutions widely.)
Winning Track Record: 5 (A successful startup is a major credential.)
- **Long-term**:
Financial Success: 5 (Potential for significant wealth if successful.)
Impact on Helping Others: 5 (Large-scale impact possible.)
Winning Track Record: 5 (Entrepreneurial success opens elite opportunities.)
Notes: High risk, high reward—requires a strong idea and execution, but aligns with your AI and data science skills.

### Option 5: Academia/Research Without a PhD
- **Short-term**:
Financial Success: 2 (Low-paying roles like research assistant, ~$30K-$50K.)
Impact on Helping Others: 2 (Supportive roles with limited influence.)
Winning Track Record: 2 (Few notable achievements possible.)
- **Medium-term**:
Financial Success: 2 (Pay remains modest without a PhD.)
Impact on Helping Others: 3 (Contributions grow if you co-author or assist.)
Winning Track Record: 3 (Some recognition possible, but limited.)
- **Long-term**:
Financial Success: 2 (Caps out below industry or PhD levels.)
Impact on Helping Others: 3 (Niche impact possible.)
Winning Track Record: 3 (Hard to advance significantly.)
**Notes**: This path is constrained without a PhD, making it less competitive.

### Option 6: Complete or Pursue a Master’s Degree
- **Short-term**:
Financial Success: 1 (Costly unless funded; no income during study.)
Impact on Helping Others: 2 (Limited during the program.)
Winning Track Record: 3 (A degree builds your profile.)
- **Medium-term**:
Financial Success: 4 (Better job prospects post-degree.)
Impact on Helping Others: 3 (Depends on subsequent career.)
Winning Track Record: 4 (A prestigious master’s is a strong signal.)
- **Long-term**:
Financial Success: 4 (Comparable to industry paths.)
Impact on Helping Others: 4 (Depends on application.)
Winning Track Record: 4 (Opens doors, but less than a PhD.)
**Notes**: Your experience may already suffice for many jobs, but a funded program could be worth considering.

### Next Step: Rank Options with Weighted Scores
Since you’re willing to sacrifice short-term gains for long-term success, I’ll weigh long-term performance more heavily. Let’s calculate a total score for each option:

Formula: Total Score = (Short-term Avg) + (Medium-term Avg) + 2 × (Long-term Avg)
Averages are computed as (Financial + Impact + Track Record) ÷ 3.

**PhD**
- Short-term: (2+2+3)/3 = 2.33
- Medium-term: (4+4+5)/3 = 4.33
- Long-term: (4+5+5)/3 = 4.67
- Total: 2.33 + 4.33 + 2 × 4.67 = 16

**Data Science (Industry)**
- Short-term: (4+3+4)/3 = 3.67
- Medium-term: (4+4+4)/3 = 4
- Long-term: (4+4+4)/3 = 4
- Total: 3.67 + 4 + 2 × 4 = 15.67

**Quant Finance/Software Engineering**
- Short-term: (5+3+3)/3 = 3.67
- Medium-term: (5+3+4)/3 = 4
- Long-term: (5+3+4)/3 = 4
- Total: 3.67 + 4 + 2 × 4 = 15.67

**Entrepreneurship**
- Short-term: (1+4+4)/3 = 3
- Medium-term: (3+5+5)/3 = 4.33
- Long-term: (5+5+5)/3 = 5
- Total: 3 + 4.33 + 2 × 5 = 17.33

**Academia Without PhD**
- Short-term: (2+2+2)/3 = 2
- Medium-term: (2+3+3)/3 = 2.67
- Long-term: (2+3+3)/3 = 2.67
- Total: 2 + 2.67 + 2 × 2.67 = 10.01

**Master’s Degree**
- Short-term: (1+2+3)/3 = 2
- Medium-term: (4+3+4)/3 = 3.67
- Long-term: (4+4+4)/3 = 4
- Total: 2 + 3.67 + 2 × 4 = 13.67

### Final Ranking

### Final Ranking
- **Entrepreneurship**: 17.33
- **PhD**: 16
- **Data Science (Industry)**: 15.67
- **Quant Finance/Software Engineering**: 15.67
- **Master’s Degree**: 13.67
- **Academia Without PhD**: 10.01
"""