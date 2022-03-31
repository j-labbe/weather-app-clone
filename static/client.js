(() => {
    "use strict";

    function renderTime() {
        const elem = document.getElementById("time");
        const today = new Date();
        let h = today.getHours();
        let m = today.getMinutes();
        h = h % 12;
        // '0' should be '12'
        h = h ? h : 12;
        m = m < 10 ? `0${m}` : m;
        elem.innerHTML = `${h}:${m}`;
        setTimeout(renderTime, 1000);
    }

    function handleSearchButtonClick(e) {
        console.log(e);
        if (e.target.id === "search") {
            document.getElementById("footer").classList.toggle("open");
        }
    }

    document.addEventListener("DOMContentLoaded", renderTime);

    document.addEventListener("click", handleSearchButtonClick);

})();