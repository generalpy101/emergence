import json

import httpx

from emergence.analysis.llm import MockLlm, OpenAiCompatClient, extract_json
from emergence.models import Analysis


def test_extract_clean_json():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extract_fenced_json():
    assert extract_json('Sure! Here is the JSON:\n```json\n{"a": 1}\n```') == {"a": 1}


def test_extract_prose_wrapped_json():
    assert extract_json('I think...\n{"a": {"b": [1, 2]}}\nHope that helps!') == {
        "a": {"b": [1, 2]}
    }


def test_extract_garbage_returns_none():
    assert extract_json("no json here at all") is None
    assert extract_json("") is None


def test_mock_llm_output_is_valid_analysis():
    analysis, error = _parse_with_slug(MockLlm().complete("some prompt https://x.io"))
    assert error is None
    assert analysis is not None
    assert analysis.llm_meta is None  # set by analyze_candidate, not the client


def test_mock_llm_is_deterministic():
    assert MockLlm().complete("same").text == MockLlm().complete("same").text


def test_mock_llm_varies_by_prompt():
    assert MockLlm().complete("prompt a").text != MockLlm().complete("prompt b").text


def _parse_with_slug(response):
    from emergence.analysis.analyze import _parse_analysis

    return _parse_analysis(response.text, "test-slug")


def test_openai_compat_client_request_shape():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["body"] = json.loads(request.content)
        captured["auth"] = request.headers.get("authorization")
        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": '{"ok": true}'}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 4},
            },
        )

    client = OpenAiCompatClient(
        base_url="http://localhost:11434/v1/",
        api_key="secret",
        model="llama3.1:8b",
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    response = client.complete("hello")

    assert captured["url"] == "http://localhost:11434/v1/chat/completions"  # trailing / handled
    assert captured["body"]["model"] == "llama3.1:8b"
    assert captured["body"]["messages"] == [{"role": "user", "content": "hello"}]
    assert captured["body"]["chat_template_kwargs"] == {"enable_thinking": False}
    assert captured["auth"] == "Bearer secret"
    assert response.text == '{"ok": true}'
    assert response.input_tokens == 10
    assert response.output_tokens == 4


def test_analysis_roundtrip_with_meta():
    analysis, _ = _parse_with_slug(MockLlm().complete("p"))
    dumped = analysis.model_dump_json()
    assert Analysis.model_validate_json(dumped).candidate_slug == "test-slug"
