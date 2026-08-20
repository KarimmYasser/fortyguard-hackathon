"""
LLM Factory — Siemens SDC LLM Gateway Adapter
Provides seamless initialization for OpenAI-compatible (GPT-5, GPT-5.4, GPT-5.5)
and Anthropic-compatible (Claude Sonnet 4.6, Claude Opus 4.5, Claude Haiku) models
routed through https://llm.sdc.siemens.cloud/v1.
"""

import os
import logging
from typing import Optional, Any
from langchain_core.language_models.chat_models import BaseChatModel

logger = logging.getLogger("thermal_sentinel.llm_factory")

def get_chat_model(
    model_name: Optional[str] = None,
    provider: Optional[str] = None,
    temperature: float = 0.1,
    streaming: bool = True,
    **kwargs: Any,
) -> BaseChatModel:
    """
    Factory function to initialize a Chat Model routed via Siemens SDC LLM Gateway
    or fallback direct provider keys.

    Supported Providers:
    - 'openai' (default): routes GPT models (e.g. gpt-5, gpt-5-mini, gpt-5.4, gpt-5.5)
      via https://llm.sdc.siemens.cloud/v1
    - 'anthropic': routes Claude models (e.g. claude-sonnet-4-6@default, claude-opus-4-5@20251101)
      via https://llm.sdc.siemens.cloud
    """
    sdc_base_url = os.getenv("SDC_LLM_BASE_URL", "https://llm.sdc.siemens.cloud/v1")
    sdc_api_key = os.getenv("SDC_LLM_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")

    resolved_provider = (
        provider or os.getenv("DEFAULT_LLM_PROVIDER", "openai")
    ).lower()

    if not model_name:
        model_name = os.getenv(
            "DEFAULT_LLM_MODEL",
            "gpt-5-mini" if resolved_provider == "openai" else "claude-sonnet-4-6@default",
        )

    logger.info(
        "Initializing LLM: provider=%s, model=%s, base_url=%s",
        resolved_provider,
        model_name,
        sdc_base_url,
    )

    if resolved_provider == "anthropic" or "claude" in model_name.lower():
        from langchain_anthropic import ChatAnthropic

        # SDC Anthropic endpoints route via https://llm.sdc.siemens.cloud
        anthropic_base = sdc_base_url.replace("/v1", "") if "/v1" in sdc_base_url else sdc_base_url
        anthropic_key = sdc_api_key or os.getenv("ANTHROPIC_API_KEY", "")

        return ChatAnthropic(
            model=model_name,
            anthropic_api_key=anthropic_key,
            anthropic_api_url=anthropic_base,
            temperature=temperature,
            streaming=streaming,
            **kwargs,
        )

    # Default to OpenAI-compatible interface (GPT-5, GPT-5.4, GPT-5.5, GPT-5-mini)
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=model_name,
        openai_api_key=sdc_api_key,
        openai_api_base=sdc_base_url,
        temperature=temperature,
        streaming=streaming,
        **kwargs,
    )
