"""
LLM Provider Utility
Supports multiple LLM backends (OpenAI, Anthropic, Azure, etc.) via environment variables.
"""
import os
from typing import Any
from dotenv import load_dotenv
from google import genai

class LLMProvider:
    def __init__(self, provider: str = None, model: str = None, api_key: str = None, base_url: str = None, azure_deployment: str = None):
        # Allow explicit override per layer, else fallback to env
        self.provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
        # Provider-specific env variable mapping
        provider_env = {
            "openai": {
                "api_key": api_key or os.getenv("OPENAI_API_KEY"),
                "base_url": base_url or os.getenv("OPENAI_BASE_URL"),
                "model": model or os.getenv("OPENAI_MODEL", "gpt-4")
            },
            "gemini": {
                "api_key": api_key or os.getenv("GEMINI_API_KEY"),
                "base_url": base_url or os.getenv("GEMINI_BASE_URL"),
                "model": model or os.getenv("GEMINI_MODEL", "gemini-pro")
            },
            "groq": {
                "api_key": api_key or os.getenv("GROQ_API_KEY"),
                "base_url": base_url or os.getenv("GROQ_BASE_URL"),
                "model": model or os.getenv("GROQ_MODEL", "llama3-70b-8192")
            },
            "openrouter": {
                "api_key": api_key or os.getenv("OPENROUTER_API_KEY"),
                "base_url": base_url or os.getenv("OPENROUTER_BASE_URL"),
                "model": model or os.getenv("OPENROUTER_MODEL", "openrouter/codellama-34b-instruct")
            },
            "langsmith": {
                "api_key": api_key or os.getenv("LANGSMITH_API_KEY"),
                "base_url": base_url or os.getenv("LANGSMITH_BASE_URL"),
                "model": model or os.getenv("LANGSMITH_MODEL", "langsmith-default")
            },
            "azure": {
                "api_key": api_key or os.getenv("AZURE_API_KEY"),
                "base_url": base_url or os.getenv("AZURE_BASE_URL"),
                "model": model or os.getenv("AZURE_MODEL", "gpt-4"),
                "azure_deployment": azure_deployment or os.getenv("AZURE_DEPLOYMENT_NAME")
            }
        }
        env = provider_env.get(self.provider, provider_env["openai"])
        self.api_key = env["api_key"]
        self.base_url = env.get("base_url")
        self.model = env["model"]
        self.azure_deployment = env.get("azure_deployment")

    def chat(self, messages, temperature=0.2, max_tokens=512):
        """
        Provider-agnostic chat interface. Supports Gemini, Groq, OpenRouter. Others raise NotImplementedError.
        messages: list of dicts with 'role' and 'content'.
        """
        import requests
        if self.provider == "gemini":
            # Gemini expects a single prompt string
            prompt = "\n".join([m["content"] for m in messages if m["role"] in ("system", "user")])
            client = genai.Client()
            # The Gemini API (google.genai) does not support temperature/max_output_tokens as arguments to generate_content as of Feb 2026.
            # Only pass model and contents.
            response = client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        elif self.provider == "groq":
            # Groq API: OpenAI-compatible endpoint
            url = self.base_url or "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        elif self.provider == "openrouter":
            # OpenRouter API: OpenAI-compatible endpoint
            url = self.base_url or "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        elif self.provider == "langsmith":
            raise NotImplementedError("LangSmith chat integration not implemented.")
        elif self.provider == "azure":
            raise NotImplementedError("Azure chat integration not implemented.")
        else:
            raise NotImplementedError(f"Provider {self.provider} not supported for chat().")
    def __init__(self, provider: str = None, model: str = None, api_key: str = None, base_url: str = None, azure_deployment: str = None):
        # Allow explicit override per layer, else fallback to env
        self.provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
        # Provider-specific env variable mapping
        provider_env = {
            "openai": {
                "api_key": api_key or os.getenv("OPENAI_API_KEY"),
                "base_url": base_url or os.getenv("OPENAI_BASE_URL"),
                "model": model or os.getenv("OPENAI_MODEL", "gpt-4")
            },
            "gemini": {
                "api_key": api_key or os.getenv("GEMINI_API_KEY"),
                "base_url": base_url or os.getenv("GEMINI_BASE_URL"),
                "model": model or os.getenv("GEMINI_MODEL", "gemini-pro")
            },
            "groq": {
                "api_key": api_key or os.getenv("GROQ_API_KEY"),
                "base_url": base_url or os.getenv("GROQ_BASE_URL"),
                "model": model or os.getenv("GROQ_MODEL", "llama3-70b-8192")
            },
            "openrouter": {
                "api_key": api_key or os.getenv("OPENROUTER_API_KEY"),
                "base_url": base_url or os.getenv("OPENROUTER_BASE_URL"),
                "model": model or os.getenv("OPENROUTER_MODEL", "openrouter/codellama-34b-instruct")
            },
            "langsmith": {
                "api_key": api_key or os.getenv("LANGSMITH_API_KEY"),
                "base_url": base_url or os.getenv("LANGSMITH_BASE_URL"),
                "model": model or os.getenv("LANGSMITH_MODEL", "langsmith-default")
            },
            "azure": {
                "api_key": api_key or os.getenv("AZURE_API_KEY"),
                "base_url": base_url or os.getenv("AZURE_BASE_URL"),
                "model": model or os.getenv("AZURE_MODEL", "gpt-4"),
                "azure_deployment": azure_deployment or os.getenv("AZURE_DEPLOYMENT_NAME")
            }
        }
        env = provider_env.get(self.provider, provider_env["openai"])
        self.api_key = env["api_key"]
        self.base_url = env.get("base_url")
        self.model = env["model"]
        self.azure_deployment = env.get("azure_deployment")

    def get_client(self) -> Any:
        if self.provider == "groq":
            # Placeholder for Groq client setup
            # import groq
            # return groq.Client(api_key=self.api_key)
            raise NotImplementedError("Groq client integration not implemented.")
        elif self.provider == "openrouter":
            # Placeholder for OpenRouter client setup
            # import openrouter
            # return openrouter.Client(api_key=self.api_key)
            raise NotImplementedError("OpenRouter client integration not implemented.")
        elif self.provider == "langsmith":
            # Placeholder for LangSmith client setup
            # import langsmith
            # return langsmith.Client(api_key=self.api_key)
            raise NotImplementedError("LangSmith client integration not implemented.")
        elif self.provider == "azure":
            # Placeholder for Azure client setup
            # import azure_client
            # return azure_client.Client(api_key=self.api_key)
            raise NotImplementedError("Azure client integration not implemented.")
        else:
            raise NotImplementedError(f"Unsupported or unimplemented LLM provider: {self.provider}")

    def get_model_name(self) -> str:
        if self.provider == "azure" and self.azure_deployment:
            return self.azure_deployment
        return self.model

