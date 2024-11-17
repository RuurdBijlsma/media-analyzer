from pathlib import Path

import pytest
from PIL import Image

from app.machine_learning.visual_llm.MiniCPMVisualLLM import MiniCPMVisualLLM
from app.machine_learning.visual_llm.VisualLLMProtocol import ChatMessage


@pytest.mark.cuda
def test_minicpm_visual_llm(tests_folder: Path) -> None:
    visual_llm = MiniCPMVisualLLM()
    image = Image.open(tests_folder / "assets/cat.jpg")
    answer = visual_llm.image_question(
        image=image, question="What creature is laying on this bed?"
    )
    assert "cat" in answer.lower()
    found_cat = False
    for message in visual_llm.stream_chat(
        ChatMessage(message="What creature is laying on this bed?", images=[image])
    ):
        if "cat" in message.lower():
            found_cat = True
    assert found_cat