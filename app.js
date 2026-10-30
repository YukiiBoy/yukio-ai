const defaultProducts = [
  {
    id: 1,
    name: "Discord Nitro 1 Bulan",
    category: "discord",
    tag: "Discord",
    emoji: "💬",
    description:
      "Nikmati fitur premium Discord tanpa batas, emote eksklusif, dan pengalaman streaming lebih nyaman.",
    price: 59000,
    oldPrice: 69000,
    rating: 4.9,
  },
  {
    id: 2,
    name: "Discord Nitro 3 Bulan",
    category: "discord",
    tag: "Discord",
    emoji: "✨",
    description:
      "Paket hemat untuk pengguna yang ingin menikmati premium Discord lebih lama.",
    price: 149000,
    oldPrice: 179000,
    rating: 4.8,
  },
  {
    id: 3,
    name: "Roblox 800 Robux",
    category: "roblox",
    tag: "Roblox",
    emoji: "🎮",
    description:
      "Top up Robux cepat dan aman untuk menambah item premium dan kebutuhan permainan favoritmu.",
    price: 125000,
    oldPrice: 150000,
    rating: 4.9,
  },
  {
    id: 4,
    name: "Roblox 2200 Robux",
    category: "roblox",
    tag: "Roblox",
    emoji: "🏆",
    description:
      "Paket premium untuk pengguna aktif yang ingin lebih banyak fitur dan item di Roblox.",
    price: 289000,
    oldPrice: 339000,
    rating: 4.8,
  },
  {
    id: 5,
    name: "Spotify Premium 1 Bulan",
    category: "music",
    tag: "Music",
    emoji: "🎵",
    description:
      "Nikmati musik tanpa iklan, waktu putar tak terbatas, dan akses offline lebih nyaman.",
    price: 35000,
    oldPrice: 45000,
    rating: 4.7,
  },
  {
    id: 6,
    name: "Netflix Premium 1 Bulan",
    category: "streaming",
    tag: "Streaming",
    emoji: "📺",
    description:
      "Streaming film dan serial favorit dengan pengalaman lebih lancar dan premium.",
    price: 65000,
    oldPrice: 82000,
    rating: 4.8,
  },
  {
    id: 7,
    name: "Steam Wallet 100k",
    category: "game",
    tag: "Game",
    emoji: "🎲",
    description:
      "Isi saldo Steam untuk membeli game, DLC, item, dan kebutuhan gaming lainnya.",
    price: 98000,
    oldPrice: 120000,
    rating: 4.9,
  },
  {
    id: 8,
    name: "YouTube Premium 1 Bulan",
    category: "streaming",
    tag: "Streaming",
    emoji: "▶️",
    description:
      "Tonton video tanpa iklan, unduh konten, dan nikmati pengalaman lebih nyaman.",
    price: 42000,
    oldPrice: 50000,
    rating: 4.7,
  },
];

const STORAGE_KEYS = {
  products: "veloraProducts",
  orders: "veloraOrders",
  cart: "veloraCart",
  wishlist: "veloraWishlist",
};

function loadProducts() {
  const stored = JSON.parse(localStorage.getItem(STORAGE_KEYS.products));
  return stored && stored.length ? stored : defaultProducts;
}

function saveProducts(products) {
  localStorage.setItem(STORAGE_KEYS.products, JSON.stringify(products));
}

function loadOrders() {
  const stored = JSON.parse(localStorage.getItem(STORAGE_KEYS.orders));
  return stored || [];
}

function saveOrders(orders) {
  localStorage.setItem(STORAGE_KEYS.orders, JSON.stringify(orders));
}

function getProducts() {
  return loadProducts();
}

function getCart() {
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.cart)) || [];
}

function saveCart(cart) {
  localStorage.setItem(STORAGE_KEYS.cart, JSON.stringify(cart));
}

function getWishlist() {
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.wishlist)) || [];
}

function saveWishlist(list) {
  localStorage.setItem(STORAGE_KEYS.wishlist, JSON.stringify(list));
}

function formatCurrency(value) {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0,
  }).format(value);
}

function showToast(message) {
  const toast = document.getElementById("toast");
  if (!toast) return;

  toast.textContent = message;
  toast.classList.add("show");

  clearTimeout(showToast.timeoutId);
  showToast.timeoutId = setTimeout(() => {
    toast.classList.remove("show");
  }, 1700);
}

function updateCartCount() {
  const cart = getCart();
  const wishlist = getWishlist();
  const cartCount = document.getElementById("cartCount");
  const wishlistCount = document.getElementById("wishlistCount");

  if (cartCount) {
    cartCount.textContent = cart.reduce((sum, item) => sum + item.qty, 0);
  }

  if (wishlistCount) {
    wishlistCount.textContent = wishlist.length;
  }
}

function renderProducts() {
  const productGrid = document.getElementById("productGrid");
  if (!productGrid) return;

  const products = getProducts();
  const wishlist = getWishlist();
  const category = document.querySelector(".filter-btn.active")?.dataset.category || "all";
  const query = (document.getElementById("searchInput")?.value || "").trim().toLowerCase();

  const filtered = products.filter((product) => {
    const matchesCategory = category === "all" || product.category === category;
    const haystack = `${product.name} ${product.tag} ${product.category} ${product.description}`.toLowerCase();
    const matchesSearch = haystack.includes(query);
    return matchesCategory && matchesSearch;
  });

  if (!filtered.length) {
    productGrid.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1; min-height: 220px; background: rgba(255,255,255,0.02); border:1px solid var(--line); border-radius:20px;">
        <div class="empty-emoji">🔎</div>
        <p>Produk yang Anda cari tidak ditemukan.</p>
      </div>
    `;
    return;
  }

  productGrid.innerHTML = filtered
    .map((product) => {
      const inWishlist = wishlist.includes(product.id);

      return `
        <article class="product-card">
          <div class="product-top">
            <span class="product-tag">${product.tag}</span>
            <button class="wish-btn ${inWishlist ? "active" : ""}" data-wishlist="${product.id}" aria-label="Wishlist">
              ${inWishlist ? "♥" : "♡"}
            </button>
          </div>

          <div class="product-art">${product.emoji}</div>

          <h3>${product.name}</h3>
          <p>${product.description}</p>

          <div class="meta-row">
            <div class="price-wrap">
              <small>${formatCurrency(product.oldPrice || product.price)}</small>
              <strong>${formatCurrency(product.price)}</strong>
            </div>
            <div class="rating">★ ${product.rating}</div>
          </div>

          <div class="product-actions">
            <button class="add-cart" data-add-cart="${product.id}">Tambah</button>
            <button class="quick-buy" data-quick-buy="${product.id}">Beli</button>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderCart() {
  const cartContainer = document.getElementById("cartItems");
  const subtotalEl = document.getElementById("subtotalPrice");
  if (!cartContainer || !subtotalEl) return;

  const cart = getCart();
  if (!cart.length) {
    cartContainer.innerHTML = `
      <div class="empty-state">
        <div class="empty-emoji">🛍️</div>
        <p>Keranjang masih kosong</p>
      </div>
    `;
    subtotalEl.textContent = formatCurrency(0);
    updateCartCount();
    return;
  }

  cartContainer.innerHTML = cart
    .map(
      (item) => `
        <div class="cart-item">
          <div class="cart-item-art">${item.emoji}</div>
          <div class="cart-item-info">
            <h4>${item.name}</h4>
            <span>Qty: ${item.qty}</span>
            <div class="cart-item-price">${formatCurrency(item.price * item.qty)}</div>
          </div>
          <button class="remove-item" data-remove-item="${item.id}">Hapus</button>
        </div>
      `
    )
    .join("");

  const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
  subtotalEl.textContent = formatCurrency(total);
  updateCartCount();
}

function addToCart(productId) {
  const products = getProducts();
  const cart = getCart();
  const product = products.find((item) => item.id === Number(productId));
  if (!product) return;

  const existing = cart.find((item) => item.id === product.id);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({
      id: product.id,
      name: product.name,
      emoji: product.emoji,
      price: product.price,
      qty: 1,
    });
  }

  saveCart(cart);
  renderCart();
  document.getElementById("cartPanel")?.classList.add("open");
  showToast(`${product.name} ditambahkan ke keranjang`);
}

function removeFromCart(productId) {
  const cart = getCart();
  const updated = cart.filter((item) => item.id !== Number(productId));
  saveCart(updated);
  renderCart();
  showToast("Produk dihapus dari keranjang");
}

function toggleWishlist(productId) {
  const wishlist = getWishlist();
  const id = Number(productId);
  const exists = wishlist.includes(id);

  const updated = exists
    ? wishlist.filter((item) => item !== id)
    : [...wishlist, id];

  saveWishlist(updated);
  renderProducts();
  updateCartCount();
  showToast(exists ? "Wishlist dihapus" : "Produk disimpan ke wishlist");
}

function renderOrdersTable() {
  const tbody = document.getElementById("ordersTableBody");
  if (!tbody) return;

  const orders = loadOrders();

  if (!orders.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align:center; color: var(--muted); padding: 20px;">
          Belum ada pesanan masuk
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = orders
    .map(
      (order) => `
        <tr>
          <td>#${order.id}</td>
          <td>${order.customerName}</td>
          <td>${order.customerEmail}</td>
          <td>${order.items.map((item) => `${item.name} x${item.qty}`).join(", ")}</td>
          <td>${formatCurrency(order.total)}</td>
          <td>${order.status}</td>
        </tr>
      `
    )
    .join("");
}

function renderProductsTable() {
  const tbody = document.getElementById("productsTableBody");
  if (!tbody) return;

  const products = getProducts();

  tbody.innerHTML = products
    .map(
      (product) => `
        <tr>
          <td>${product.name}</td>
          <td>${product.category}</td>
          <td>${formatCurrency(product.price)}</td>
          <td class="table-actions">
            <button class="table-btn" data-edit-product="${product.id}">Edit</button>
            <button class="table-btn delete" data-delete-product="${product.id}">Hapus</button>
          </td>
        </tr>
      `
    )
    .join("");
}

function addProduct(product) {
  const products = getProducts();
  products.unshift(product);
  saveProducts(products);
  renderProductsTable();
  renderProducts();
}

function editProduct(productId, updatedValues) {
  const products = getProducts();
  const idx = products.findIndex((p) => p.id === Number(productId));
  if (idx === -1) return;

  products[idx] = { ...products[idx], ...updatedValues };
  saveProducts(products);
  renderProductsTable();
  renderProducts();
}

function deleteProduct(productId) {
  const products = getProducts();
  const updated = products.filter((p) => p.id !== Number(productId));
  saveProducts(updated);
  renderProductsTable();
  renderProducts();
}

function startCountdown() {
  const end = new Date(Date.now() + 1000 * 60 * 60 * 24 + 1000 * 60 * 8 + 1000 * 15);
  const hoursEl = document.getElementById("hours");
  const minutesEl = document.getElementById("minutes");
  const secondsEl = document.getElementById("seconds");

  if (!hoursEl || !minutesEl || !secondsEl) return;

  const tick = () => {
    const now = new Date();
    const diff = Math.max(0, end - now);
    const h = Math.floor(diff / (1000 * 60 * 60));
    const m = Math.floor((diff / (1000 * 60)) % 60);
    const s = Math.floor((diff / 1000) % 60);

    hoursEl.textContent = String(h).padStart(2, "0");
    minutesEl.textContent = String(m).padStart(2, "0");
    secondsEl.textContent = String(s).padStart(2, "0");
  };

  tick();
  setInterval(tick, 1000);
}

function handleHomeEvents() {
  document.addEventListener("click", (event) => {
    const addBtn = event.target.closest("[data-add-cart]");
    if (addBtn) addToCart(addBtn.dataset.addCart);

    const quickBuyBtn = event.target.closest("[data-quick-buy]");
    if (quickBuyBtn) {
      addToCart(quickBuyBtn.dataset.quickBuy);
      document.getElementById("cartPanel")?.classList.add("open");
    }

    const removeBtn = event.target.closest("[data-remove-item]");
    if (removeBtn) removeFromCart(removeBtn.dataset.removeItem);

    const wishlistBtn = event.target.closest("[data-wishlist]");
    if (wishlistBtn) toggleWishlist(wishlistBtn.dataset.wishlist);

    const filterBtn = event.target.closest(".filter-btn");
    if (filterBtn) {
      document.querySelectorAll(".filter-btn").forEach((btn) => {
        btn.classList.toggle("active", btn === filterBtn);
      });
      renderProducts();
    }

    const faqBtn = event.target.closest(".faq-question");
    if (faqBtn) {
      const item = faqBtn.parentElement;
      item.classList.toggle("active");
    }
  });

  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", () => renderProducts());
  }

  document.getElementById("cartToggle")?.addEventListener("click", () => {
    const panel = document.getElementById("cartPanel");
    if (panel) panel.classList.toggle("open");
  });

  document.getElementById("closeCart")?.addEventListener("click", () => {
    document.getElementById("cartPanel")?.classList.remove("open");
  });

  document.getElementById("wishlistBtn")?.addEventListener("click", () => {
    if (!getWishlist().length) {
      showToast("Wishlist masih kosong");
      return;
    }
    showToast(`${getWishlist().length} item favorit tersimpan`);
  });

  document.getElementById("checkoutNow")?.addEventListener("click", () => {
    const cart = getCart();
    if (!cart.length) {
      showToast("Keranjang masih kosong");
      return;
    }
    const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
    showToast(`Total checkout: ${formatCurrency(total)}`);
  });

  document.getElementById("openSupport")?.addEventListener("click", () => {
    document.getElementById("chatWidget")?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  });

  document.getElementById("toggleChat")?.addEventListener("click", () => {
    const widget = document.getElementById("chatWidget");
    if (widget) {
      widget.style.display = widget.style.display === "none" ? "block" : "none";
    }
  });

  document.getElementById("chatForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const input = document.getElementById("chatInput");
    const body = document.getElementById("chatBody");
    if (!input || !body) return;

    const message = input.value.trim();
    if (!message) return;

    const userMsg = document.createElement("div");
    userMsg.className = "chat-msg user";
    userMsg.textContent = message;
    body.appendChild(userMsg);

    const botMsg = document.createElement("div");
    botMsg.className = "chat-msg bot";
    const replies = [
      "Halo! Produk yang Anda cari tersedia. Mau cek Discord premium atau Roblox top up?",
      "Tersedia, kami bisa bantu proses order dengan cepat.",
      "Silakan pilih produk yang Anda inginkan, lalu kami lanjutkan checkout.",
      "Untuk order cepat, kirim nama akun dan produk yang ingin dibeli.",
    ];
    botMsg.textContent = replies[Math.floor(Math.random() * replies.length)];
    body.appendChild(botMsg);

    input.value = "";
    body.scrollTop = body.scrollHeight;
  });

  document.getElementById("orderForm")?.addEventListener("submit", (event) => {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const customerName = formData.get("customerName")?.toString().trim();
    const customerEmail = formData.get("customerEmail")?.toString().trim();
    const customerPhone = formData.get("customerPhone")?.toString().trim();
    const paymentMethod = formData.get("paymentMethod")?.toString().trim();
    const notes = formData.get("notes")?.toString().trim();

    const cart = getCart();

    if (!cart.length) {
      showToast("Keranjang masih kosong");
      return;
    }

    const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);

    const orders = loadOrders();
    const newOrder = {
      id: Date.now(),
      customerName,
      customerEmail,
      customerPhone,
      paymentMethod,
      notes,
      items: cart,
      total,
      status: "Menunggu Konfirmasi",
      createdAt: new Date().toISOString(),
    };

    orders.unshift(newOrder);
    saveOrders(orders);

    saveCart([]);
    renderCart();
    form.reset();
    showToast("Order berhasil dikirim. Tim kami akan segera menghubungi Anda.");
  });

  document.getElementById("newsletterForm")?.addEventListener("submit", (event) => {
    event.preventDefault();
    showToast("Email Anda berhasil terdaftar untuk promo terbaru.");
    event.target.reset();
  });
}

function handleAdminEvents() {
  const productForm = document.getElementById("productForm");
  if (!productForm) return;

  const editingState = { id: null };

  const resetForm = () => {
    productForm.reset();
    editingState.id = null;
  };

  document.getElementById("cancelEditBtn")?.addEventListener("click", resetForm);

  productForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const name = document.getElementById("productName").value.trim();
    const emoji = document.getElementById("productEmoji").value.trim();
    const category = document.getElementById("productCategory").value;
    const tag = document.getElementById("productTag").value.trim();
    const price = Number(document.getElementById("productPrice").value);
    const oldPrice = Number(document.getElementById("productOldPrice").value || 0);
    const description = document.getElementById("productDescription").value.trim();

    if (!name || !emoji || !category || !tag || !price || !description) {
      showToast("Lengkapi semua field produk.");
      return;
    }

    const productData = {
      id: editingState.id || Date.now(),
      name,
      emoji,
      category,
      tag,
      price,
      oldPrice: oldPrice || price,
      description,
      rating: 4.8,
    };

    if (editingState.id) {
      editProduct(editingState.id, productData);
      showToast("Produk berhasil diperbarui.");
    } else {
      addProduct(productData);
      showToast("Produk baru berhasil ditambahkan.");
    }

    resetForm();
    renderProducts();
  });

  document.addEventListener("click", (event) => {
    const editBtn = event.target.closest("[data-edit-product]");
    if (editBtn) {
      const products = getProducts();
      const product = products.find((p) => p.id === Number(editBtn.dataset.editProduct));
      if (!product) return;

      editingState.id = product.id;

      document.getElementById("productName").value = product.name;
      document.getElementById("productEmoji").value = product.emoji;
      document.getElementById("productCategory").value = product.category;
      document.getElementById("productTag").value = product.tag;
      document.getElementById("productPrice").value = product.price;
      document.getElementById("productOldPrice").value = product.oldPrice || product.price;
      document.getElementById("productDescription").value = product.description;
    }

    const deleteBtn = event.target.closest("[data-delete-product]");
    if (deleteBtn) {
      deleteProduct(deleteBtn.dataset.deleteProduct);
      showToast("Produk berhasil dihapus.");
    }
  });

  document.getElementById("resetDemoBtn")?.addEventListener("click", () => {
    localStorage.setItem(STORAGE_KEYS.products, JSON.stringify(defaultProducts));
    localStorage.setItem(STORAGE_KEYS.orders, JSON.stringify([]));
    localStorage.setItem(STORAGE_KEYS.cart, JSON.stringify([]));
    localStorage.setItem(STORAGE_KEYS.wishlist, JSON.stringify([]));
    renderProductsTable();
    renderOrdersTable();
    renderProducts();
    showToast("Demo berhasil direset.");
  });

  renderProductsTable();
  renderOrdersTable();
}

document.addEventListener("DOMContentLoaded", () => {
  const page = document.body.dataset.page;

  if (page === "home") {
    handleHomeEvents();
    renderProducts();
    renderCart();
    updateCartCount();
    startCountdown();
  }

  if (page === "admin") {
    handleAdminEvents();
  }
});
