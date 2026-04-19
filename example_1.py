import requests
import json
from typing import Any, Dict, Optional


def lmstudio_generate(
    prompt: str,
    model: str = "qwen3.5-0.8b",
    temperature: float = 0.7, # Controls the randomness of the output. Higher values (e.g., 0.8) make the output more random, while lower values (e.g., 0.2) make it more deterministic.
    max_tokens: int = 2000, # Limits the maximum number of tokens in the generated output. This helps to control the length of the response and prevent excessively long outputs.
    top_p: float = 0.95, # Controls the diversity of the output by limiting the token selection to a subset of tokens with a cumulative probability above a certain threshold. For example, top_p=0.9 means only the tokens that together account for 90% of the probability mass will be considered for generation.
    stop: Optional[list[str]] = None, # A list of strings that, when generated, will cause the model to stop generating further tokens. This can be used to control the end of the response or to prevent certain outputs.
    api_url: str = "http://127.0.0.1:1234/v1/chat/completions",
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 120,
    ) -> Dict[str, Any]:
    
    """Send a text generation request to LMStudio running locally."""
    if headers is None:
        headers = {"Content-Type": "application/json"}

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
    }
    if stop is not None:
        payload["stop"] = stop

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"LMStudio request failed for {api_url}: {exc}. Check your API URL and try again."
        ) from exc



if __name__ == "__main__":
    # Example 1: Text-only request
    sample_prompt = "Write a short greeting on behalf of the local LLM API."
    sample_prompt = "Implement a python function that receives two IPv4 addresses, and returns the number of addresses between them (including the first one, excluding the last one)."
    try:
        result = lmstudio_generate(sample_prompt)
        # print("Text response:", result)  # Print the full response
        print(json.dumps(result, indent=2, ensure_ascii=False)) # Formated print
        
        # Extract content from the response
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        print("\nExtracted content:", content)

        # Save result to .md file
        with open("./results/result.md", "w", encoding="utf-8") as file:
            file.write(content)

    except RuntimeError as error:
        print("Text error:", error)
