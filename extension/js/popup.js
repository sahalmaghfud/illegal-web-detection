const SERVER_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", async () => {
  const statusText = document.getElementById("status-text");

  let currentUrl = "";
  let currentDomain = "";

  // Dapatkan URL tab saat ini
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    if (tabs && tabs.length > 0) {
      currentUrl = tabs[0].url;

      if (currentUrl.startsWith("chrome-extension://") && currentUrl.includes("pages/blocked.html")) {
        try {
          const urlObj = new URL(currentUrl);
          const originalUrl = urlObj.searchParams.get("url");
          if (originalUrl) {
            currentUrl = originalUrl;
          }
        } catch (e) { }
      }

      try {
        currentDomain = new URL(currentUrl).hostname;
      } catch (e) {
        currentDomain = currentUrl;
      }

      // Cek di local storage untuk melihat status prediksi yang sudah ada
      const data = await chrome.storage.local.get([currentDomain]);
      if (data[currentDomain] !== undefined) {
        const label = data[currentDomain];
        if (label === 0) {
          statusText.innerText = "Aman (Normal)";
          statusText.style.color = "green";
        } else if (label === 1) {
          statusText.innerText = "Judi Online";
          statusText.style.color = "red";
        } else if (label === 2) {
          statusText.innerText = "Pornografi";
          statusText.style.color = "red";
        } else if (label === 3) {
          statusText.innerText = "Pembajakan";
          statusText.style.color = "red";
        } else {
          statusText.innerText = "Tidak Diketahui";
        }
      } else {
        // Jika belum ada di local storage (kemungkinan belum selesai di-scan)
        statusText.innerText = "Belum terdeteksi / Normal";
        statusText.style.color = "gray";
      }
    }
  });

  const adminPin = document.getElementById("admin-pin");
  const adminLabel = document.getElementById("admin-label");
  const adminBtn = document.getElementById("admin-btn");
  const adminMsg = document.getElementById("admin-msg");
  const adminError = document.getElementById("admin-error");

  adminBtn.addEventListener("click", async () => {
    if (!currentUrl || !currentDomain) {
      alert("Gagal mendapatkan URL dari tab aktif.");
      return;
    }

    const enteredPin = adminPin.value;
    const { admin_pin } = await chrome.storage.local.get(["admin_pin"]);

    if (!admin_pin || enteredPin !== admin_pin) {
      adminError.innerText = "PIN salah!";
      adminError.style.display = "block";
      adminMsg.style.display = "none";
      setTimeout(() => { adminError.style.display = "none"; }, 3000);
      return;
    }

    const newLabel = parseInt(adminLabel.value);

    adminBtn.disabled = true;
    adminBtn.innerText = "Memproses...";

    try {
      // 1. Simpan label baru di local storage
      await chrome.storage.local.set({ [currentDomain]: newLabel });

      // 2. Kirim laporan ke server
      await fetch(`${SERVER_URL}/report`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          url: currentDomain,
          label_reported_by_user: newLabel
        })
      });

      adminError.style.display = "none";
      adminMsg.style.display = "block";

      setTimeout(() => {
        adminMsg.style.display = "none";
        // Jika tab saat ini adalah blocked page dan statusnya sudah diubah jadi normal (0), kita bisa arahkan kembali ke URL asli
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          if (tabs && tabs.length > 0) {
            const tabUrl = tabs[0].url;
            if (newLabel === 0 && tabUrl.startsWith("chrome-extension://") && tabUrl.includes("pages/blocked.html")) {
              chrome.tabs.update(tabs[0].id, { url: currentUrl });
            } else {
              chrome.tabs.reload(tabs[0].id);
            }
          }
        });
      }, 1000);

    } catch (e) {
      console.error(e);
      adminError.innerText = "Terjadi kesalahan koneksi!";
      adminError.style.display = "block";
      setTimeout(() => { adminError.style.display = "none"; }, 3000);
    } finally {
      adminBtn.disabled = false;
      adminBtn.innerText = "Ubah Status & Kirim Laporan";
    }
  });
});
