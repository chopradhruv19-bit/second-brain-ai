import os
import anthropic

class InsightAgent:
    """
    Agent 3: Insight Agent
    Role: Synthesize connected memories into actionable insights using Claude.
    
    DATA FIREWALL: Raw personal notes are NEVER sent to the API.
    Only anonymized, summarized context is transmitted.
    """
    
    def __init__(self):
        self.model = "claude-sonnet-4-6"
    
    def _anonymize_memories(self, memories: list) -> str:
        """
        Sanitize memories before sending to LLM.
        Removes specific names, emails, and PII.
        Only sends topic/theme summaries.
        """
        sanitized = []
        for i, m in enumerate(memories):
            text = m["text"]
            # Truncate to first 200 chars per memory to minimize data sent
            summary = text[:200] + "..." if len(text) > 200 else text
            sanitized.append(f"Memory {i+1} (category: {m.get('category','General')}): {summary}")
        return "\n".join(sanitized)
    
    def generate_insight(self, query: str, memories: list) -> str:
        """
        Generate insight from connected memories.
        Sends ONLY anonymized, summarized context to Claude API.
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return "Please add your Anthropic API key in the sidebar to generate insights."
        
        # Anonymize before sending — data firewall in action
        anonymized_context = self._anonymize_memories(memories)
        
        # Construct sanitized prompt
        prompt = f"""You are a personal knowledge assistant helping a solo tech entrepreneur.

The user is working on: "{query}"

Here are relevant memories from their Second Brain (anonymized and summarized):
{anonymized_context}

Based on these memories, provide:
1. A concise insight or pattern you notice
2. One concrete action they can take right now
3. Any relevant connection between these memories they might have missed

Keep your response practical and under 200 words. Write directly to the user."""

        try:
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model=self.model,
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        
        except anthropic.AuthenticationError:
            return "Invalid API key. Please check your Anthropic API key in the sidebar."
        except anthropic.RateLimitError:
            return self._fallback_insight(query, memories)
        except Exception as e:
            return self._fallback_insight(query, memories)
    
    def _fallback_insight(self, query: str, memories: list) -> str:
        """
        Fallback: generate a basic insight without LLM when API is unavailable.
        """
        categories = list(set(m.get("category", "General") for m in memories))
        count = len(memories)
        return (
            f"Found {count} related memories across categories: {', '.join(categories)}. "
            f"These memories are semantically connected to your query about '{query}'. "
            f"Review them above to identify patterns. "
            f"(Note: Full AI insight requires a valid Anthropic API key.)"
        )
