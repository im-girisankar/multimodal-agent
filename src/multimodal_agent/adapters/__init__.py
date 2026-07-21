"""Optional heavy adapters (STT, vision, TTS, LLM).

None of these are imported automatically.  Import them explicitly only when
the corresponding extras are installed:

    from multimodal_agent.adapters.stt import WhisperModality   # needs 'audio' extra
    from multimodal_agent.adapters.vision import VisionModality  # needs 'vision' extra
    from multimodal_agent.adapters.tts import TTSSink            # needs 'audio' extra
    from multimodal_agent.adapters.llm import LLMReasoner        # needs 'llm' extra
"""
