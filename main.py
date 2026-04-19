import requests
import base64
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any
from promt import *
from prompt_en import *


def image_to_base64(image_path: str) -> str:
    """Convert an image file to base64 string."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_json_from_response(response: Dict[str, Any]) -> Dict[str, Any] | str:
    """
    Extract clean JSON from LMStudio API response.
    
    Handles cases where the model returns JSON wrapped in markdown code blocks.
    
    Args:
        response: The full response dict from LMStudio API
        
    Returns:
        Parsed JSON object or raw content if no JSON found
    """
    try:
        # Get the content from the response
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if not content:
            raise ValueError("No content found in response")
        
        # Try to find JSON wrapped in markdown code block (```json ... ```)
        json_match = re.search(r"```(?:json)?\s*(.*?)```", content, re.DOTALL)
        
        if json_match:
            # If JSON wrapped in code block, extract it
            json_str = json_match.group(1).strip()
        else:
            # If no code block, try to parse the content directly
            json_str = content.strip()
        
        # Parse and validate JSON
        return json.loads(json_str)
    
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse JSON from response: {exc}. Content: {content}") from exc
    except (KeyError, IndexError) as exc:
        raise ValueError(f"Invalid response structure: {exc}") from exc


def lmstudio_generate_with_image(
    prompt: str,
    image_path: str,
    model: str = "qwen3.5-0.8b",
    temperature: float = 0.2, # Controls the randomness of the output. Higher values (e.g., 0.8) make the output more random, while lower values (e.g., 0.2) make it more deterministic.
    max_tokens: int = 2000,
    top_p: float = 0.95,
    stop: Optional[list[str]] = None,
    api_url: str = "http://127.0.0.1:1234/v1/chat/completions",
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 120,
) -> Dict[str, Any]:
    """
    Send a request with image to LMStudio for vision-based analysis.
    
    Note: Image processing takes longer than text, so timeout is set to 120 seconds by default.
    Adjust if your hardware is slower.
    """
    if headers is None:
        headers = {"Content-Type": "application/json"}

    # Convert image to base64
    image_base64 = image_to_base64(image_path)
    
    # Determine image type from file extension
    image_extension = Path(image_path).suffix.lower()
    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(image_extension, "image/jpeg")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_base64}"
                        },
                    },
                ],
            }
        ],
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
            f"LMStudio image request failed for {api_url}: {exc}. Проверьте, что LMStudio запущен и доступен на указанном порту."
        ) from exc

# Save result to the file in same directory as the image
def save_result_to_file(result: Dict[str, Any], image_path: str) -> None:
    output_path = Path(image_path).with_suffix(".json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Result saved to {output_path}")


if __name__ == "__main__":
    # Example 2: Request with image
    # Adjust the image path and prompt as needed
    image_path = "data/5.jpg"
    prompt = prompt_en_2

    # Set parameters for image processing, adjust as needed based on your hardware capabilities and desired output
    model = "qwen3.5-0.8b"
    temperature = 0.3  # Lower temperature for more deterministic output, adjust as needed
    top_p = 0.95 # Controls the diversity of the output by limiting the token selection to a subset of tokens with a cumulative probability above a certain threshold. For example, top_p=0.9 means only the tokens that together account for 90% of the probability mass will be considered for generation.
    timeout = 280 # Increase if necessary
    try:
        # Increase timeout for image processing, adjust as needed based on your hardware capabilities
        response = lmstudio_generate_with_image(
            prompt, 
            image_path,
            model=model,
            temperature=temperature,
            top_p=top_p,
            timeout=timeout,
        )
        print("Full response:", response)
        
        # Extract clean JSON from the response
        clean_json = extract_json_from_response(response)
        print("\nExtracted JSON:")
        print(json.dumps(clean_json, indent=2, ensure_ascii=False))

        path = Path(image_path)
        save_result_to_file(clean_json, f"./results/{path.name}")
    except (RuntimeError, FileNotFoundError, ValueError) as error:
        print("Error:", error)
