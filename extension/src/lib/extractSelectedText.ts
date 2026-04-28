async function getActiveTabId(): Promise<number> {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) throw new Error("Could not access the current tab.");
  return tab.id;
}

export async function extractSelectedText(): Promise<string> {
  const tabId = await getActiveTabId();

  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => window.getSelection()?.toString() ?? "",
  });

  const raw = results?.[0]?.result ?? "";
  const cleaned = raw.replace(/\s+/g, " ").trim();

  if (!cleaned || cleaned.length < 30) {
    throw new Error("Please select more text before summarizing.");
  }
  return cleaned;
}