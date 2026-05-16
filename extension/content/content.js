function extractTextContent() {
  const title = document.title || "";
  const bodyText = document.body ? document.body.innerText : "";
  // Mengambil title dan 1500 karakter pertama dari text content
  return title + " " + bodyText.substring(0, 1500);
}

function extractHTMLFeatures() {
  // SILAHKAN GANTI ARRAY INI DENGAN 139 TAG HTML YANG DIBUTUHKAN.
  // Pastikan array berjumlah pas 139 sesuai inputan layer 4 model Anda.
  const htmlTags = [
    'a', 'abbr', 'acronym', 'address', 'area', 'article', 'aside', 'audio',
    'b', 'base', 'bdi', 'bdo', 'big', 'blockquote', 'body', 'br',
    'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col',
    'colgroup', 'content', 'data', 'datalist', 'dd', 'del', 'details',
    'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'em', 'embed',
    'fencedframe', 'fieldset', 'figcaption', 'figure', 'font', 'footer',
    'form', 'frame', 'frameset', 'geolocation', 'h1', 'h2', 'h3', 'h4',
    'h5', 'h6', 'head', 'header', 'hgroup', 'hr', 'html', 'i',
    'iframe', 'image', 'img', 'input', 'ins', 'kbd', 'label', 'legend',
    'li', 'link', 'main', 'map', 'mark', 'marquee', 'math', 'menu',
    'menuitem', 'meta', 'meter', 'nav', 'nobr', 'noembed', 'noframes',
    'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p',
    'param', 'picture', 'plaintext', 'pre', 'progress', 'q', 'rb',
    'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'script', 'search',
    'section', 'select', 'selectedcontent', 'shadow', 'slot', 'small',
    'source', 'span', 'strike', 'strong', 'style', 'sub', 'summary',
    'sup', 'svg', 'table', 'tbody', 'td', 'template', 'textarea',
    'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt',
    'u', 'ul', 'var', 'video', 'wbr', 'xmp'
  ];

  const features = [];
  for (let i = 0; i < 139; i++) {
    const tag = htmlTags[i] || `dummy_tag_${i}`;
    const count = document.getElementsByTagName(tag).length;
    features.push(count);
  }
  return features;
}



chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "REQUEST_FEATURES") {
    sendResponse({
      textContent: extractTextContent(),
      htmlFeatures: extractHTMLFeatures()
    });
  }
});

function initCheck() {
  if (window.self !== window.top) return; // Abaikan iframes
  if (window.location.protocol === "chrome-extension:") return;

  chrome.runtime.sendMessage({ action: "CHECK_PAGE", url: window.location.href });
}

// Beri sedikit waktu untuk render DOM
setTimeout(initCheck, 500);
