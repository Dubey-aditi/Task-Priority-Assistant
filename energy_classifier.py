import asyncio
import re
from claude_agent_sdk import query, ClaudeAgentOptions


async def classify_energy_async(task: str) -> dict:
    """Classify a task by energy level and suggest optimal execution order."""
    prompt = f"""Classify the following task by energy level required to complete it AND
suggest an optimal execution order that keeps me engaged while still protecting priority work.

Task: "{task}"

First, classify energy level using ONLY one word: "low", "medium", or "high".

Guidelines for classification:
- low: minimal physical/mental effort (reading, sending emails, making calls, planning)
- medium: moderate effort (organizing, researching, writing, light cooking)
- high: significant physical/mental effort (exercising, deep cleaning, shopping, intensive cooking, coding)

Then, provide:
1) Suggested position in my to-do sequence: FIRST / MIDDLE / LAST
2) One short reason based on:
   - momentum (starting with something doable),
   - variety (alternating energy levels),
   - and priority (not postponing important work indefinitely).

Rules for sequencing:
- Avoid starting with only low-energy tasks if they cause procrastination.
- Avoid stacking too many high-energy tasks back-to-back.
- Important tasks should appear early or middle — never always last.
- Keep reason very concise and focused(max 10 words).

Respond in this exact format:
ENERGY: [low/medium/high]
POSITION: [FIRST/MIDDLE/LAST]
REASON: [your short reason]"""

    options = ClaudeAgentOptions(max_turns=1)

    result_text = ""
    async for message in query(prompt=prompt, options=options):
        if hasattr(message, "content") and message.content:
            for block in message.content:
                if hasattr(block, "text"):
                    result_text += block.text

    return parse_classification_response(result_text)


def parse_classification_response(response: str) -> dict:
    """Parse the classification response into structured data."""
    result = {"energy": "Medium", "position": "Middle", "reason": ""}

    energy_match = re.search(r"ENERGY:\s*(low|medium|high)", response, re.IGNORECASE)
    if energy_match:
        # Capitalize first letter for display
        result["energy"] = energy_match.group(1).capitalize()

    position_match = re.search(
        r"POSITION:\s*(FIRST|SECOND|THIRD|MIDDLE|LATE|LAST)", response, re.IGNORECASE
    )
    if position_match:
        # Capitalize first letter, rest lowercase (e.g., First, Middle, Last)
        pos = position_match.group(1).capitalize()
        result["position"] = pos

    reason_match = re.search(r"REASON:\s*(.+?)(?:\n|$)", response, re.IGNORECASE)
    if reason_match:
        reason = reason_match.group(1).strip()
        # Sentence case for reason
        if reason:
            reason = reason[0].upper() + reason[1:]
        result["reason"] = reason

    return result


def classify_energy(task: str) -> dict:
    """Synchronous wrapper for classify_energy_async."""
    return asyncio.run(classify_energy_async(task))
