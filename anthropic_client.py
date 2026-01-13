#!/usr/bin/env python3
"""
Anthropic API Client with Extended Thinking Support

This module provides a proper implementation for handling Claude's extended thinking
feature. The key requirement is to preserve thinking blocks EXACTLY as received
when sending follow-up messages in a conversation.

Key Rules for Extended Thinking:
1. Never modify the content of thinking/redacted_thinking blocks
2. Never remove them from assistant messages in conversation history
3. Keep the exact order of content blocks as returned
4. The thinking block must be the first block in the assistant's content array

Usage:
    client = ClaudeClient(api_key="your-api-key")

    # First message with extended thinking
    response = client.send_message("Hello, explain quantum computing")
    print(response)

    # Follow-up message (thinking blocks are preserved automatically)
    response = client.send_message("Can you elaborate on superposition?")
    print(response)

    # Start a fresh conversation
    client.clear_conversation()

Author: Akhil Reddy
"""

import os
from typing import Optional
from dataclasses import dataclass, field

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


@dataclass
class ConversationMessage:
    """Represents a message in the conversation history."""
    role: str
    content: any  # Can be string or list of content blocks


@dataclass
class ClaudeClient:
    """
    Claude API client with proper extended thinking support.

    This client automatically preserves thinking blocks in conversation history
    to avoid the "thinking blocks must be preserved exactly" error.

    Attributes:
        api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        model: Model to use (default: claude-sonnet-4-20250514)
        max_tokens: Maximum tokens in response (default: 16000)
        thinking_enabled: Whether to use extended thinking (default: True)
        thinking_budget: Token budget for thinking (default: 10000)
    """
    api_key: Optional[str] = None
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 16000
    thinking_enabled: bool = True
    thinking_budget: int = 10000
    _messages: list = field(default_factory=list)
    _client: any = field(default=None, init=False)

    def __post_init__(self):
        """Initialize the Anthropic client."""
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "anthropic package is not installed. "
                "Install it with: pip install anthropic"
            )

        # Use environment variable if no API key provided
        if self.api_key is None:
            self.api_key = os.environ.get("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self._client = anthropic.Anthropic(api_key=self.api_key)
        self._messages = []

    def send_message(self, user_message: str) -> str:
        """
        Send a message to Claude and get a response.

        IMPORTANT: This method automatically preserves thinking blocks from
        previous responses. When extended thinking is enabled, Claude returns
        thinking/redacted_thinking blocks that MUST be included unchanged in
        follow-up messages.

        Args:
            user_message: The user's message to send

        Returns:
            The text content of Claude's response (thinking is preserved
            internally but not returned)
        """
        # Add user message to history
        self._messages.append({
            "role": "user",
            "content": user_message
        })

        # Build API request parameters
        request_params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": self._messages,
        }

        # Add thinking configuration if enabled
        if self.thinking_enabled:
            request_params["thinking"] = {
                "type": "enabled",
                "budget_tokens": self.thinking_budget
            }

        # Make API call
        response = self._client.messages.create(**request_params)

        # CRITICAL: Store the COMPLETE response content including thinking blocks
        # This is the key fix for the extended thinking API error.
        # The response.content is a list that may contain:
        # - thinking blocks (type: "thinking")
        # - redacted_thinking blocks (type: "redacted_thinking")
        # - text blocks (type: "text")
        #
        # We must preserve ALL of these exactly as received when sending
        # follow-up messages. DO NOT filter, modify, or reorder them.
        self._messages.append({
            "role": "assistant",
            "content": response.content  # Keep ALL content blocks unchanged
        })

        # Extract just the text content for return value
        text_content = self._extract_text_content(response.content)

        return text_content

    def _extract_text_content(self, content_blocks) -> str:
        """
        Extract text content from response, excluding thinking blocks.

        This is only for the return value - the full content with thinking
        blocks is still preserved in conversation history.

        Args:
            content_blocks: List of content blocks from API response

        Returns:
            Concatenated text content
        """
        text_parts = []

        for block in content_blocks:
            # Handle both dict and object-style access
            if hasattr(block, 'type'):
                block_type = block.type
                block_text = getattr(block, 'text', '')
            else:
                block_type = block.get('type', '')
                block_text = block.get('text', '')

            if block_type == "text":
                text_parts.append(block_text)

        return "\n".join(text_parts)

    def clear_conversation(self):
        """
        Clear conversation history to start fresh.

        Use this when you want to start a new conversation without any
        previous context (including thinking blocks).
        """
        self._messages = []

    def get_conversation_history(self) -> list:
        """
        Get the full conversation history including thinking blocks.

        Returns:
            List of messages with their content (including thinking blocks)
        """
        return self._messages.copy()

    def disable_thinking(self):
        """Disable extended thinking for subsequent messages."""
        self.thinking_enabled = False

    def enable_thinking(self, budget_tokens: int = 10000):
        """
        Enable extended thinking for subsequent messages.

        Args:
            budget_tokens: Token budget for thinking (default: 10000)
        """
        self.thinking_enabled = True
        self.thinking_budget = budget_tokens


def create_client(
    api_key: Optional[str] = None,
    thinking_enabled: bool = True,
    thinking_budget: int = 10000
) -> ClaudeClient:
    """
    Factory function to create a ClaudeClient with extended thinking support.

    Args:
        api_key: Anthropic API key (optional, uses env var if not provided)
        thinking_enabled: Whether to enable extended thinking (default: True)
        thinking_budget: Token budget for thinking (default: 10000)

    Returns:
        Configured ClaudeClient instance
    """
    return ClaudeClient(
        api_key=api_key,
        thinking_enabled=thinking_enabled,
        thinking_budget=thinking_budget
    )


# Example usage and demonstration
if __name__ == "__main__":
    print("=" * 60)
    print("Anthropic API Client with Extended Thinking Support")
    print("=" * 60)
    print()
    print("This module fixes the common error:")
    print("  'thinking blocks must be preserved exactly as received'")
    print()
    print("The key is to store response.content (which includes thinking")
    print("blocks) EXACTLY as returned and pass it back unchanged in")
    print("follow-up messages.")
    print()
    print("Example usage:")
    print("-" * 60)
    print("""
from anthropic_client import ClaudeClient

# Create client (uses ANTHROPIC_API_KEY env var)
client = ClaudeClient()

# First message - thinking blocks are generated
response1 = client.send_message("What is 15 * 23?")
print(response1)

# Follow-up message - thinking blocks from response1 are
# automatically preserved in the conversation history
response2 = client.send_message("Now multiply that by 2")
print(response2)

# Start fresh conversation (clears thinking blocks)
client.clear_conversation()
""")
    print("-" * 60)
    print()
    print("To test with a real API key, set ANTHROPIC_API_KEY and run:")
    print("  python -c 'from anthropic_client import ClaudeClient; ...")
