document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const label = parseInt(params.get("label"), 10);
    const url = params.get("url");

    const messageEl = document.getElementById("warning-message");
    const urlEl = document.getElementById("blocked-url");
    const imgEl = document.getElementById("char-image");

    let numImages = 0;

    if (label === 1) {
        messageEl.innerText = "Situs ini terindikasi sebagai situs Judi Online!";
        numImages = 4;
    } else if (label === 2) {
        messageEl.innerText = "Situs ini terindikasi sebagai situs Pornografi!";
        numImages = 3;
    } else if (label === 3) {
        messageEl.innerText = "Situs ini terindikasi sebagai situs Pembajakan!";
        numImages = 3;
    }

    if (numImages > 0) {
        const randomImageNum = Math.floor(Math.random() * numImages) + 1;
        imgEl.src = `char/${label}/${randomImageNum}.png`;
        imgEl.style.display = "block";
    }

    if (url) {
        try {
            let domain = new URL(url).hostname;
            if (domain.length > 30) {
                domain = domain.substring(0, 27) + "...";
            }
            urlEl.innerText = `Domain yang diblokir: ${domain}`;
        } catch (e) {
            let displayUrl = url.length > 30 ? url.substring(0, 27) + "..." : url;
            urlEl.innerText = `Domain yang diblokir: ${displayUrl}`;
        }
    }

    const closeBtn = document.getElementById("close-btn");
    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            window.close();
        });
    }
});
