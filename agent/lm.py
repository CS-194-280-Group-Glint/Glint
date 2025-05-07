from django.conf import settings
import dspy


class LMFactory:
    @staticmethod
    def get_model(
            provider: str,
            model_name: str,
            **kwargs,
    ) -> dspy.LM:
        if provider == "openai":
            return get_openai_model(model_name)
        else:
            raise ValueError(
                f"Unsupported provider or model: provider: {provider}, model: {model_name}"
            )


def get_openai_model(model_name: str) -> dspy.LM:
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

    return dspy.LM(f"openai/{model_name}", cache=False, api_key=settings.OPENAI_API_KEY, **kwargs)
