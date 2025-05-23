
import { api } from "./api.js";  // Relative path

async function communicate(data) {
    console.log("cmrd: ", data);
}

async function button_click() {
    api("/cmrd")
        .then(data => {
            communicate(data.msg);
        })
        .catch(err => console.error(err));

    api("/hangar")
        .then(data => {
            communicate(data.msg);
        })
        .catch(err => console.error(err));

    document.getElementById("btn_test").innerText = "Camarada";
    document.getElementById("btn_test").style.backgroundColor ="rgb(235, 20, 20)";
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("btn_test").addEventListener("click", button_click);
});
