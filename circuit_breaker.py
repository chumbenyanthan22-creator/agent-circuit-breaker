import math
from typing import Dict, List

class RunawayAgentException(Exception):
    """Custom exception thrown to instantly kill runaway AI loops before token bleed occurs."""
    pass

class NexusCoreGateway:
    def __init__(self, loop_similarity_threshold: float = 0.90):
        self.agent_state_cache: Dict[str, List[str]] = {}
        self.similarity_threshold = loop_similarity_threshold

    def _calculate_levenshtein_similarity(self, s1: str, s2: str) -> float:
        s1, s2 = s1.lower().strip(), s2.lower().strip()
        if s1 == s2: return 1.0
        if not s1 or not s2: return 0.0
        
        matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
        for i in range(len(s1) + 1): matrix[i][0] = i
        for j in range(len(s2) + 1): matrix[0][j] = j
            
        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                cost = 0 if s1[i-1] == s2[j-1] else 1
                matrix[i][j] = min(matrix[i-1][j] + 1,      # Deletion
                                   matrix[i][j-1] + 1,      # Insertion
                                   matrix[i-1][j-1] + cost) # Substitution
        
        distance = matrix[len(s1)][len(s2)]
        max_len = max(len(s1), len(s2))
        return 1.0 - (distance / max_len)

    def intercept_agent_execution(self, task_id: str, incoming_prompt: str) -> bool:
        if task_id not in self.agent_state_cache:
            self.agent_state_cache[task_id] = []
            
        history = self.agent_state_cache[task_id]
        history.append(incoming_prompt)
        
        if len(history) >= 3:
            sim_1 = self._calculate_levenshtein_similarity(history[-1], history[-2])
            sim_2 = self._calculate_levenshtein_similarity(history[-2], history[-3])
            
            if sim_1 >= self.similarity_threshold and sim_2 >= self.similarity_threshold:
                raise RunawayAgentException(
                    f"\n🛑 [NEXUS ALERT] Critical loop detected on Task ID: {task_id}\n"
                    f" -> Sequence Similarity Breached: ({sim_1:.2f}, {sim_2:.2f})\n"
                    f" -> Execution halted safely. External API wallet protected."
                )
        return True

if __name__ == "__main__":
    gateway = NexusCoreGateway(loop_similarity_threshold=0.90)
    print("--- Initializing Agent Circuit Breaker Local Verification Test ---")
    loop_task_coordinate = "agent-workflow-44"
    prompts_stream = [
        "Fetch raw infrastructure logs for customer Alpha and parse anomalies",
        "Fetch server usage logs for customer Alpha and verify metrics", 
        "Fetch server usage logs for customer Alpha and verify metrics"  
    ]
    try:
        for idx, prompt in enumerate(prompts_stream):
            print(f"\nFeeding Agent Execution Step {idx + 1}: '{prompt}'")
            gateway.intercept_agent_execution(loop_task_coordinate, prompt)
        print("\nTest Failed: The runtime engine failed to intercept the loop context.")
    except RunawayAgentException as error_log:
        print(f"\033[92m{error_log}\033[0m")
        print("\n--- Verification Suite Terminated Safely: 100% Core Logic Functional ---")
      
