"""
LLM Factory - Siemens SDC LLM Gateway Adapter
Provides seamless initialization for OpenAI-compatible (GPT-5.4, GPT-5.5)
models routed through https://llm.sdc.siemens.cloud/v1.
"""

import os
import logging
from typing import Optional, Any, List, Dict
from openai import AsyncOpenAI, OpenAI

logger = logging.getLogger("thermal_sentinel.llm_factory")


def get_openai_client(async_mode: bool = True):
    """
    Returns an initialized AsyncOpenAI or OpenAI client pointing to Siemens SDC Gateway with 4.0s timeout.
    """
    api_key = os.getenv("SDC_LLM_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("SDC_LLM_BASE_URL", "https://llm.sdc.siemens.cloud/v1")
    
    if async_mode:
        return AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=4.0)
    return OpenAI(api_key=api_key, base_url=base_url, timeout=4.0)



def get_chat_model(model_name: Optional[str] = None, **kwargs: Any):
    """
    Legacy wrapper returning an OpenAI client for backward compatibility.
    """
    return get_openai_client(async_mode=False)


async def generate_chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    max_completion_tokens: int = 250,
    temperature: float = 0.2,
) -> Optional[str]:
    """
    Asynchronously invokes the LLM via Siemens SDC Gateway.
    Returns generated content string, or None if unavailable.
    """
    api_key = os.getenv("SDC_LLM_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        logger.warning("No SDC_LLM_API_KEY found. Falling back to deterministic heuristics.")
        return None

    resolved_model = model or os.getenv("DEFAULT_LLM_MODEL", "gpt-5.4")
    if resolved_model == "gpt-5-4":
        resolved_model = "gpt-5.4"

    try:
        import asyncio
        client = get_openai_client(async_mode=True)
        coro = client.chat.completions.create(
            model=resolved_model,
            messages=messages,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
        )
        resp = await asyncio.wait_for(coro, timeout=3.0)
        if resp.choices and resp.choices[0].message and resp.choices[0].message.content:
            return resp.choices[0].message.content.strip()
        return None
    except Exception as e:
        logger.warning("LLM Gateway call timed out or failed (%s: %s). Using deterministic fallback.", type(e).__name__, e)
        return None

