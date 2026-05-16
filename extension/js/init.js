document.addEventListener("DOMContentLoaded", async () => {
    const data = await chrome.storage.local.get(["admin_pin"]);
    if (data.admin_pin) {
        document.body.innerHTML = `
            <div style="font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f5f7fa; margin: 0;">
                <div style="background: white; padding: 40px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; max-width: 400px; border: 1px solid #e2e8f0;">
                    <div style="color: #28a745; margin-bottom: 15px;"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg></div>
                    <h2 style="color: #2c3e50; margin: 0 0 10px 0;">PIN Telah Diatur</h2>
                    <p style="color: #6c757d; margin: 0; line-height: 1.5;">Halaman ini tidak dapat digunakan lagi. PIN Anda sudah tersimpan dengan aman.</p>
                </div>
            </div>`;
        return;
    }

    const pinInput = document.getElementById("pin-input");
    const pinConfirm = document.getElementById("pin-confirm");
    const saveBtn = document.getElementById("save-btn");
    const errorMsg = document.getElementById("error-msg");

    function enforceNumeric(e) {
        e.target.value = e.target.value.replace(/[^0-9]/g, '');
    }

    pinInput.addEventListener("input", enforceNumeric);
    pinConfirm.addEventListener("input", enforceNumeric);

    saveBtn.addEventListener("click", async () => {
        const pin = pinInput.value;
        const confirmPin = pinConfirm.value;

        if (pin.length !== 4 || confirmPin.length !== 4) {
            errorMsg.textContent = "PIN harus berupa 4 angka penuh.";
            errorMsg.style.display = "block";
            return;
        }

        if (pin !== confirmPin) {
            errorMsg.textContent = "Konfirmasi PIN tidak cocok.";
            errorMsg.style.display = "block";
            return;
        }

        errorMsg.style.display = "none";

        // Tampilkan prompt peringatan agar user konfirmasi dua kali
        const confirmation = confirm(`PERINGATAN!\n\nApakah Anda yakin ingin menyimpan PIN?\n\nPastikan Anda mengingat PIN ini karena TIDAK BISA DIGANTI lagi di kemudian hari.`);

        if (!confirmation) {
            return; // Batalkan penyimpanan jika user menekan tombol Cancel/Batal
        }

        await chrome.storage.local.set({ admin_pin: pin });
        document.body.innerHTML = `
            <div style="font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f5f7fa; margin: 0;">
                <div style="background: white; padding: 40px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; max-width: 400px; border: 1px solid #e2e8f0;">
                    <div style="color: #28a745; margin-bottom: 15px;"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg></div>
                    <h2 style="color: #28a745; margin: 0 0 10px 0;">PIN Berhasil Disimpan!</h2>
                    <p style="color: #6c757d; margin-bottom: 25px; line-height: 1.5;">Silakan tutup halaman ini dan gunakan ekstensi seperti biasa.</p>
                    <button id="close-init-btn" style="background: linear-gradient(135deg, #007bff, #0056b3); color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 10px; cursor: pointer; width: 100%; font-weight: 600; box-shadow: 0 4px 15px rgba(0,123,255,0.3);">Tutup Halaman</button>
                </div>
            </div>`;

        const closeInitBtn = document.getElementById("close-init-btn");
        if (closeInitBtn) {
            closeInitBtn.addEventListener("click", () => window.close());
        }
    });
});
