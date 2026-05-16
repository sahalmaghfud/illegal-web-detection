const SERVER_URL = "http://127.0.0.1:8000";

function getDomain(url) {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname;
  } catch (e) {
    return null;
  }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "CHECK_PAGE") {
    // Ack immediately to prevent message port closing
    sendResponse({ received: true });
    processPageCheck(request.url, sender.tab.id, sender.tab.windowId);
  }
  return true;
});

async function processPageCheck(url, tabId, windowId) {
  const domain = getDomain(url);
  if (!domain) return;

  console.log("Checking URL:", url);

  try {
    // Layer 1: Check Chrome Local Storage (Includes initial domains.json & previously predicted domains)
    const storageResult = await chrome.storage.local.get([domain]);
    if (storageResult[domain] !== undefined) {
      console.log("Layer 1 hit (Local Storage):", storageResult[domain]);
      blockTab(tabId, storageResult[domain], url);
      return;
    }

    // Layer 2: Check Server /check-domain
    try {
      console.log("=== MENGIRIM REQUEST KE /check-domain ===");
      console.log(`URL Endpoint: ${SERVER_URL}/check-domain?url=${encodeURIComponent(url)}`);
      const checkUrlResponse = await fetch(`${SERVER_URL}/check-domain?url=${encodeURIComponent(url)}`);
      if (checkUrlResponse.ok) {
        const checkUrlData = await checkUrlResponse.json();
        if (checkUrlData.in_list) {
          console.log("Layer 2 hit (Server /check-domain):", checkUrlData.label);
          await chrome.storage.local.set({ [domain]: checkUrlData.label });
          blockTab(tabId, checkUrlData.label, url);
          return;
        }
      }
    } catch (e) {
      console.error("Layer 2 error:", e);
    }

    // Layer 3: Server /predict
    console.log("Proceeding to Layer 3 (/predict)");

    // Request features from content script
    chrome.tabs.sendMessage(tabId, { action: "REQUEST_FEATURES" }, async (featuresResponse) => {
      if (chrome.runtime.lastError || !featuresResponse) {
        console.error("Failed to get features from content script:", chrome.runtime.lastError?.message);
        return;
      }

      try {
        // Delay slightly for render before taking screenshot
        await new Promise(r => setTimeout(r, 500));

        const imageBase64DataUrl = await chrome.tabs.captureVisibleTab(windowId, { format: "jpeg", quality: 50 });

        const predictPayload = {
          url: url,
          text_content: featuresResponse.textContent,
          image_base64: imageBase64DataUrl,
          html_features: featuresResponse.htmlFeatures
        };

        console.log("=== MENGIRIM PAYLOAD KE /predict ===");
        // Buat salinan log dengan base64 yang dipotong agar Console tidak lambat (hang)
        const payloadUntukLog = { ...predictPayload };
        if (payloadUntukLog.image_base64) {
          payloadUntukLog.image_base64 = payloadUntukLog.image_base64.substring(0, 100) + "... [DIPOTONG UNTUK LOG]";
        }
        console.log(payloadUntukLog);

        const predictResponse = await fetch(`${SERVER_URL}/predict`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(predictPayload)
        });

        if (predictResponse.ok) {
          const predictData = await predictResponse.json();
          console.log("Layer 3 hit (Server /predict):", predictData);
          await chrome.storage.local.set({ [domain]: predictData.label });
          blockTab(tabId, predictData.label, url);
        } else {
          console.error("Predict API Error", predictResponse.status);
        }
      } catch (e) {
        console.error("Layer 4 error:", e);
      }
    });

  } catch (error) {
    console.error("Process page check error:", error);
  }
}

function blockTab(tabId, label, url) {
  if (label > 0) { // Only notify if it's 1 (Judi), 2 (Porno), or 3 (Pembajakan)
    const blockedUrl = chrome.runtime.getURL(`pages/blocked.html?label=${label}&url=${encodeURIComponent(url)}`);
    chrome.tabs.update(tabId, { url: blockedUrl }).catch(() => { });
  }
}

chrome.runtime.onInstalled.addListener(async () => {
  const data = await chrome.storage.local.get(["admin_pin"]);
  if (!data.admin_pin) {
    chrome.tabs.create({ url: chrome.runtime.getURL("pages/init.html") });
  }

  // Load domains.json into local storage
  try {
    const url = chrome.runtime.getURL('data/domains.json');
    const response = await fetch(url);
    const domainsData = await response.json();
    await chrome.storage.local.set(domainsData);
    console.log("domains.json loaded into local storage.");
  } catch (e) {
    console.error("Error loading domains.json on install:", e);
  }
});
