import ast
import json
from groq import Groq

# 1. Function to score a code fix by parsing AST and measuring line/character length.
def score_fix(original: str, fix: str) -> float:
    """
    Scores a fix candidate. Invalid syntax gets 0.0.
    Valid syntax starts at 1.0, adds 0.3 for fewer lines, and 0.2 for fewer characters.
    """
    print("[DEBUG] Scoring candidate fix...")
    try:
        ast.parse(fix)
    except (SyntaxError, ValueError, TypeError) as e:
        print(f"[DEBUG] Invalid Python code in fix: {e}")
        return 0.0

    score = 1.0
    
    original_lines = len(original.splitlines())
    fix_lines = len(fix.splitlines())
    if fix_lines < original_lines:
        score += 0.3
        
    if len(fix) < len(original):
        score += 0.2
        
    print(f"[DEBUG] Candidate fix scored: {score}")
    return score

# 2. Function to perform single-point crossover between two parent fixes.
def crossover(fix1: str, fix2: str) -> str:
    """
    Splits two parent fixes in half and combines them.
    Takes the first half of fix1 lines and the second half of fix2 lines.
    """
    print("[DEBUG] Performing crossover...")
    lines1 = fix1.splitlines()
    lines2 = fix2.splitlines()
    
    mid1 = len(lines1) // 2
    mid2 = len(lines2) // 2
    
    child_lines = lines1[:mid1] + lines2[mid2:]
    return "\n".join(child_lines)

# 3. Function to mutate a fix by calling the Groq API.
def mutate(fix: str, api_key: str) -> str:
    """
    Mutates a fix by calling Groq to slightly improve the Python code.
    Returns the original fix unchanged in case of any API errors.
    """
    print("[DEBUG] Mutating fix via Groq API...")
    try:
        client = Groq(api_key=api_key)
        
        system_prompt = "You are a senior Python code reviewer."
        user_message = (
            "Improve this Python fix slightly. \n"
            "Return only the improved code. No explanation.\n\n"
            f"{fix}"
        )
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Clean potential markdown formatting
        cleaned_text = response_text
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:].strip()
            if cleaned_text.lower().startswith("python"):
                cleaned_text = cleaned_text[6:].strip()
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3].strip()
            
        print("[DEBUG] Mutation complete.")
        return cleaned_text
    except Exception as e:
        print(f"[DEBUG] Mutation failed: {e}. Returning original fix.")
        return fix

# 4. Function to evolve code fixes using a genetic algorithm over 3 generations.
def evolve_fix(code: str, bug: dict, api_key: str) -> str:
    """
    Generates 4 fix candidates and evolves them over 3 generations.
    Each generation keeps the top 2 fixes, performs crossover, mutates, and forms a new population.
    """
    print("[DEBUG] Starting evolutionary fix process...")
    candidates = []
    
    try:
        client = Groq(api_key=api_key)
        system_prompt = "You are a senior Python code reviewer."
        user_message = (
            f"Given the original Python code:\n{code}\n\n"
            f"And the detected bug:\n{json.dumps(bug)}\n\n"
            "Please provide a complete corrected version of the code that fixes this bug.\n"
            "Return only the corrected code. No explanation. No markdown."
        )
        
        for i in range(4):
            print(f"[DEBUG] Generating initial fix candidate {i+1} of 4...")
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                temperature=0.7,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            candidate_text = response.choices[0].message.content.strip()
            
            # Clean markdown code blocks if present
            cleaned_candidate = candidate_text
            if cleaned_candidate.startswith("```"):
                cleaned_candidate = cleaned_candidate[3:].strip()
                if cleaned_candidate.lower().startswith("python"):
                    cleaned_candidate = cleaned_candidate[6:].strip()
            if cleaned_candidate.endswith("```"):
                cleaned_candidate = cleaned_candidate[:-3].strip()
                
            candidates.append(cleaned_candidate)
            
    except Exception as e:
        print(f"[DEBUG] Error generating initial candidates: {e}")
        if candidates:
            return candidates[0]
        return code
        
    first_candidate = candidates[0] if candidates else code
    
    try:
        for gen in range(1, 4):
            print(f"[DEBUG] Processing generation {gen}...")
            scored_population = []
            for cand in candidates:
                score = score_fix(code, cand)
                scored_population.append((cand, score))
                
            scores_only = [item[1] for item in scored_population]
            print(f"Generation {gen} scores: {scores_only}")
            
            scored_population.sort(key=lambda x: x[1], reverse=True)
            
            top1 = scored_population[0][0]
            top2 = scored_population[1][0]
            
            child_crossover = crossover(top1, top2)
            child_mutated = mutate(child_crossover, api_key)
            
            candidates = [top1, top2, child_crossover, child_mutated]
            
        final_scored = []
        for cand in candidates:
            score = score_fix(code, cand)
            final_scored.append((cand, score))
            
        final_scored.sort(key=lambda x: x[1], reverse=True)
        best_fix = final_scored[0][0]
        print(f"[DEBUG] Best score after 3 generations: {final_scored[0][1]}")
        return best_fix
        
    except Exception as e:
        print(f"[DEBUG] Error during evolution loop: {e}")
        return first_candidate
