const form = document.querySelector("#form");
form.addEventListener("submit", function(e) {
    e.preventDefault();
    getColors();
})

const getColors = () => {
    console.log('into get colors')
    const query = form.elements.query.value;
    fetch("/palette", {
        method: "POST",
        headers: {
            "Content-type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            query: query
        })
    })
    .then((response) => response.json())
    .then((data) => {
        const colors = data.colors;
        console.log('what is the value of returned colors? ', colors)
        const container = document.querySelector(".container");
        createColorBlocks(colors, container);
    })
}

const createColorBlocks = (colors, parent) => {
    parent.innerHTML = "";
    for (const color of colors) {
        const div = document.createElement("div");
        div.classList.add("color");
        div.style.backgroundColor = color;
        div.style.width = `calc(100%/ ${colors.length})`
        
        div.addEventListener("click", function() {
            navigator.clipboard.writeText(color);
        })

        const span = document.createElement("span");
        span.innerText = color;
        div.appendChild(span)

        parent.appendChild(div)
    }
}