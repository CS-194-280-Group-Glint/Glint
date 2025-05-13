from django.conf import settings
import dspy


class LMFactory:
    @staticmethod
    def get_model(
            provider: str,
            model_name: str,
            api_key: str,
            **kwargs,
    ) -> dspy.LM:
        if provider == "openai":
            return get_openai_model(model_name=model_name, api_key=api_key)
        elif provider == "gemini":
            return get_gemini_model(model_name=model_name, api_key=api_key)
        elif provider == "claude":
            return get_claude_model(model_name=model_name, api_key=api_key)
        elif provider == "meta":
            return get_meta_model(model_name=model_name, api_key=api_key)
        else:
            raise ValueError(
                f"Unsupported provider or model: provider: {provider}, model: {model_name}"
            )


def get_openai_model(
        model_name: str,
        api_key: str
) -> dspy.LM:
    model_configs = {
        "gpt-4o-mini": {"temperature": 1.0, "max_tokens": None},
        "gpt-4o": {"temperature": 1.0, "max_tokens": None},
        "o3-mini": {"temperature": 1.0, "max_tokens": 10000},
        "o1-mini": {"temperature": 1.0, "max_tokens": 10000},
        "o1": {"temperature": 1.0, "max_tokens": 10000},
        "o1-preview": {"temperature": 1.0, "max_tokens": 10000},
    }

    if model_name not in model_configs:
        raise ValueError(f"Unsupported model: {model_name}")

    config = model_configs[model_name]
    kwargs = {k: v for k, v in config.items() if v is not None}

    return dspy.LM(f"openai/{model_name}", cache=False, api_key=api_key, **kwargs)

def get_gemini_model(
        model_name: str,
        api_key: str
) -> dspy.LM:
    supported_models = ["gemini-pro", "gemini-1.5-pro-latest", "gemini-2.0-flash", "gemini-2.0-flash-exp", "gemini-2.0-flash-lite-preview-02-05"]
    if model_name not in supported_models:
        raise ValueError(f"Unsupported model: {model_name}")
    return dspy.LM(f"gemini/{model_name}", cache=False, api_key=api_key)

def get_claude_model(
        model_name: str,
        api_key: str
) -> dspy.LM:
    supported_models = [
        "claude-3-5-sonnet-20240620",  # Claude 3.5
        "claude-3-haiku-20240307",     # Claude 3
        "claude-3-opus-20240229",      # Claude 3
        "claude-3-sonnet-20240229",    # Claude 3
        "claude-2",                    # Claude 2
        "claude-2.1",                  # Claude 2.1
        "claude-instant-1.2"           # Claude Instant
    ]
    if model_name not in supported_models:
        raise ValueError(f"Unsupported model: {model_name}")
    return dspy.LM(f"anthropic/{model_name}", cache=False, api_key=api_key)

def get_meta_model(
        model_name: str,
        api_key: str
) -> dspy.LM:
    supported_models = [
        "llama-4-scout-17b-16e-instruct-fp8",
        "llama-4-maverick-17b-128e-instruct-fp8", 
        "llama-3.3-70b-instruct",
        "llama-3.3-8b-instruct"
    ]
    if model_name not in supported_models:
        raise ValueError(f"Unsupported model: {model_name}")
    return dspy.LM(f"meta/{model_name}", cache=False, api_key=api_key)


