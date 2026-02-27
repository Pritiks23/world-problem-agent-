const btn = document.getElementById("generate");
const output = document.getElementById("output");

btn.addEventListener("click", async () => {
  const domain = document.getElementById("domain").value;
  output.textContent = "Generating ideas...";

  const prompt = `
You are a strategic global innovation agent.
Given this domain: ${domain}
List 5 of the world's biggest problems and for each:
- Why it is massive
- A bold idea for how this domain can help
- Why it could realistically work
Return as JSON array of 5 objects.
`;

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_OPENAI_API_KEY"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [{role: "user", content: prompt}],
        temperature: 0.8
      })
    });

    const data = await response.json();
    const content = data.choices[0].message.content;
    output.textContent = content;
  } catch (err) {
    output.textContent = "Error: " + err;
  }
});
