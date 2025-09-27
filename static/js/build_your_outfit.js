const catalog = document.getElementById("catalog");
const stageSlots = [...document.querySelectorAll('#stage .slot')];

// Safer: encode product JSON for attribute
function encodeProduct(p){ return encodeURIComponent(JSON.stringify(p)); }
function decodeProduct(s){ return JSON.parse(decodeURIComponent(s)); }

  function productCard(p){
    return `
      <div class="card draggable-card" draggable="true"
           data-product='${encodeProduct(p)}'>
        <img src="${p.img}" class="card-img-top" alt="${p.title}">
        <div class="card-body py-2">
          <div class="small text-truncate" title="${p.title}">${p.title}</div>
          <div class="d-flex justify-content-between">
            <small class="fw-semibold">$${Number(p.price).toFixed(2)}</small>
          </div>
        </div>
      </div>
    `;
  }

  // Drag start from catalog
  catalog.addEventListener('dragstart', e => {
    const card = e.target.closest('.draggable-card');
    if (!card) return;
    e.dataTransfer.setData('application/json', card.dataset.product);
  });

  // Accept drop on slots
  stageSlots.forEach(slot => {
    slot.addEventListener('dragover', e => { e.preventDefault(); slot.classList.add("highlight"); });
    slot.addEventListener('dragleave', () => slot.classList.remove("highlight"));
    slot.addEventListener('drop', e => {
      e.preventDefault();
      slot.classList.remove("highlight");
      const p = decodeProduct(e.dataTransfer.getData('application/json'));
      slot.innerHTML = ` <div class="position-relative">
                            <img src="${p.img}" class="w-100 rounded-3"
                             style="border-radius: 15px; max-height: 250px; object-fit: cover; width: 100%;">
                            <button type="button" class="btn-close position-absolute top-0 end-0 m-1 remove-btn"></button>
                          </div>`
      slot.classList.add('filled');
      slot.dataset.productId = p.id;
    });
  });

  document.getElementById("stage").addEventListener("click", e => {
    if (e.target.classList.contains("remove-btn")) {
      const slot = e.target.closest(".slot");
      slot.innerHTML = "";
      slot.classList.remove("filled");
      delete slot.dataset.productId;
    }
  });

  // Add-all from mockup
  document.getElementById('addAllFromMockup').onclick = async () => {
    const ids = stageSlots.map(s => s.dataset.productId).filter(Boolean);
    console.log("YOY")
    if (ids.length === 0) {
      console.log("NO")
      // show a different modal if no items
      const emptyModalEl = document.getElementById('emptyMockupModal');
      const emptyModal = new bootstrap.Modal(emptyModalEl);
      emptyModal.show();
      return;
    }
    // otherwise, add items
    for (const id of ids){
      await fetch("/cart/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ product_id: Number(id), qty: 1 })
      });
    }
    // success modal
    console.log("YES")
    const successModalEl = document.getElementById('mockupModal');
    const successModal = new bootstrap.Modal(successModalEl);
    successModal.show();
  };

// render helper
function render(items){
  if (!items?.length){
    catalog.innerHTML = `<div class="text-muted">No results.</div>`;
    return;
  }
  catalog.innerHTML = items.map(productCard).join("");
}

// load from API
async function loadProducts(q=""){
  const url = `/api/products?limit=50${q ? `&q=${encodeURIComponent(q)}` : ""}`;
  const res = await fetch(url);
  const { items } = await res.json();
  console.log(items)
  render(items);
}

// debounce utility
function debounce(fn, delay){
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), delay); };
}

// wire search (debounced on input, immediate on Enter)
const debouncedSearch = debounce(() => loadProducts(searchInput.value.trim()), 300);

searchInput.addEventListener("input", debouncedSearch);
searchInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    loadProducts(searchInput.value.trim());
  }
});

// initial load
loadProducts();