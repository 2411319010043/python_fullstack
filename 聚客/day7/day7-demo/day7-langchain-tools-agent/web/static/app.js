const form = document.getElementById("agent-form");
const questionInput = document.getElementById("question");
const imageSourceInput = document.getElementById("image_source");
const submitButton = document.getElementById("submit-btn");
const statusText = document.getElementById("status");
const answerBox = document.getElementById("answer");
const structuredBox = document.getElementById("structured");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionInput.value.trim();
  const imageSource = imageSourceInput.value.trim();

  if (!question) {
    statusText.textContent = "\u95ee\u9898\u4e0d\u80fd\u4e3a\u7a7a";
    return;
  }

  submitButton.disabled = true;
  statusText.textContent = "\u8bf7\u6c42\u4e2d...";
  answerBox.textContent = "\u5904\u7406\u4e2d...";
  structuredBox.textContent = "\u5904\u7406\u4e2d...";

  const payload = {
    question,
    image_source: imageSource || null,
  };

  try {
    const response = await fetch("/api/agent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || `HTTP ${response.status}`);
    }

    const data = await response.json();
    answerBox.textContent = data.answer ?? "";
    structuredBox.textContent = JSON.stringify(data.structured ?? data, null, 2);
    statusText.textContent = `\u5b8c\u6210: ${data.task_type ?? "unknown"}`;
  } catch (error) {
    answerBox.textContent = "\u8bf7\u6c42\u5931\u8d25";
    structuredBox.textContent = String(error);
    statusText.textContent = "\u8bf7\u6c42\u5931\u8d25";
  } finally {
    submitButton.disabled = false;
  }
});
