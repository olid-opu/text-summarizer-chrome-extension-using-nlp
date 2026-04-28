async function getActiveTabId(): Promise<number> {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) throw new Error("Could not access the current tab.");
  return tab.id;
}

export async function extractPageText(): Promise<string> {
  const tabId = await getActiveTabId();

  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => {
      const nodes = document.querySelectorAll(
        "p, h1, h2, h3, article, section, main",
      );
      const parts: string[] = [];
      nodes.forEach((n) => {
        const t = (n as HTMLElement).innerText;
        if (t) parts.push(t);
      });
      return parts.join("\n");
    },
  });

  const raw = results?.[0]?.result ?? "";
  const cleaned = raw.replace(/\s+/g, " ").trim();

  if (cleaned.length < 100) {
    throw new Error("Not enough readable text found on this page.");
  }
  return cleaned;
}