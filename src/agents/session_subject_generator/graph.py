"""Main graph for session subject generator agent."""

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from .agent import create_subject_generator_agent


class SessionSubjectState(TypedDict):
    """State schema for session subject generation.
    
    Input fields:
        user_message: The user's first message in the session
        agent_name: Name of the agent being used
        agent_description: Description of the agent's purpose
        
    Output field:
        subject: Generated session subject (3-7 words, max 50 chars)
    
    """

    user_message: str
    agent_name: str
    agent_description: str
    subject: str


def generate_subject_node(state: SessionSubjectState) -> dict[str, Any]:
    """Generate a session subject based on user message and agent context.
    
    Args:
        state: Current state with user_message, agent_name, agent_description
        
    Returns:
        State update with subject field populated
    
    """
    # Create the agent
    agent = create_subject_generator_agent()
    
    # Build the input message with context
    input_message = f"""Generate a session subject based on this context:

User's first message: "{state['user_message']}"

Agent being used: {state['agent_name']}
Agent description: {state['agent_description']}

Generate a concise subject (3-7 words, max 50 chars) that captures the user's intent."""
    
    # Invoke the agent to generate the subject
    result = agent.invoke({"messages": [{"role": "user", "content": input_message}]})
    
    # Extract the generated subject from the last message
    subject = result["messages"][-1].content.strip()
    
    # Ensure subject doesn't exceed 50 characters
    if len(subject) > 50:
        subject = subject[:47] + "..."
    
    return {"subject": subject}


# Build the graph
builder = StateGraph(SessionSubjectState)

# Add the single node
builder.add_node("generate_subject", generate_subject_node)

# Define the flow: START -> generate_subject -> END
builder.add_edge(START, "generate_subject")
builder.add_edge("generate_subject", END)

# Compile the graph
graph = builder.compile()

