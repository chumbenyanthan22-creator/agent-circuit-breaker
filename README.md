# Agent Circuit Breaker 🛡️

A lightweight, zero-latency programmatic runtime circuit breaker engine designed to prevent autonomous AI multi-agent swarms from entering recursive execution loops and bleeding API wallet budgets overnight.

## 🚀 The Core Engine Problem
When autonomous agent systems face semantic contradictions, tool failures, or data loop traps, they can stall inside infinite loops. Existing observability tools trace technical up-time but fail to map real-time token expense compliance. Agent Circuit Breaker sits directly in the runtime callback layer to track semantic distance profile changes and disconnect runaway threads before financial token burn cascades.

## 📦 Local Setup & Deployment

```bash
# Clone the repository
git clone https://github.com
cd agent-circuit-breaker

# Run the live loop interception demo
python circuit_breaker.py
```

## 🛠️ Implementation Blueprint
Integrate the interceptor directly within your outbound model invocation loops:

```python
from circuit_breaker import NexusCoreGateway, RunawayAgentException

gateway = NexusCoreGateway(loop_similarity_threshold=0.90)
task_id = "agent-workflow-44"

try:
    # Drop this execution check right before firing your outbound LLM API call
    gateway.intercept_agent_execution(task_id, current_agent_prompt)
except RunawayAgentException as e:
    # Clean fallback handling when a thread loop is broken
    print("Execution blocked safely. External API wallet protected.")
```
