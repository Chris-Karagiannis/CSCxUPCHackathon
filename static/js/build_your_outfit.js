const catalog = document.getElementById('catalog');
const stageSlot = [...document.querySelectorAll('#stage .slot')];

function productCard(p){
    return `
        <div class="card draggable-card" draggable="true"
        data-product='${JSON.stringify(p)}'} >
            <img src="${p.img}" class="card-img-top"/>
            <div class=""card-body py-2">
                <small>${p.brand}</small>
                <small class="fw-semibold">$${Number(p.price).toFixed(2)}</small>
            </div>
            <div class="small text-truncate">${p.title}</div>
        </div>
    `;
}

// basic drag events
catalog.addEventListener('dragstart', e => {
    if (!e.target.closest('.draggable-card')) return ;
    const card = e.target.closest('.draggable-card');
    e.dataTransfer.setData('application/json', card.dataset.product);
});

stageSlots.forEach(slot => {
    slot.addEventListener('dragover', e => {
        e.preventDefault(); slot.classList.add("highlight");
    });
    slot.addEventListener('dragleave', () => {
        slot.classList.remove("highlight")
    });
    slot.addEventListener('drop', e => {
        e.preventDefault();
        slot.classList.remove("highlight");
        const p = JSON.parse(e.dataTransfer.getData('application/json'))
        slot.innerHTML = `<img src="${p.img}" alt="" class="w-100 rounded-3">`;
        slot.classList.add('filled');
        slot.dataset.productId = p.id;
    });
});

// Add-all from mockup
document.getElementById('addAllFromMockup').onclick = async () => {
    const ids = stageSlots.map(s => s.dataset.productId).filter(Boolean);
    for (const id of ids){
        await fetch("/cart/add", {
            method: "POST",
            headers:{"Content-Type": "application/json"},
            body: JSON.stringify({producr_id: Number(id), qty: 1})
        })
    }
    alert("Added all from mockup!");
};

// Save
document.getElementById('saveMockup').onclick = async () => {
    const payload = stageSlots.map(s => ({
        slot: s.dataset.slot, 
        product_id: s.dataset.productId || null 
    }));
    if (data.ok) locaiton.href = `/mockups/${data.id}`;
};

// Load catalog (server returns your product fields)
(async () => {
    const res = await fetch("/api/products?limit=30")
    const items = await res.json();
    catalog.innerHTML = items.map(productCard).join("");
})();





