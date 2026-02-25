const state = {
  token: localStorage.getItem("token"),
  accounts: [],
  statement: null,
};

const els = {
  totalBalance: document.getElementById("total-balance"),
  accountCount: document.getElementById("account-count"),
  lastClosing: document.getElementById("last-closing"),
  lastRange: document.getElementById("last-range"),
  accounts: document.getElementById("accounts"),
  refreshAccounts: document.getElementById("refresh-accounts"),
  signupForm: document.getElementById("signup-form"),
  loginForm: document.getElementById("login-form"),
  createAccountForm: document.getElementById("create-account-form"),
  depositForm: document.getElementById("deposit-form"),
  withdrawForm: document.getElementById("withdraw-form"),
  transferForm: document.getElementById("transfer-form"),
  issueCardForm: document.getElementById("issue-card-form"),
  cardsAccountFilter: document.getElementById("cards-account-filter"),
  cardList: document.getElementById("card-list"),
  statementForm: document.getElementById("statement-form"),
  transactionList: document.getElementById("transaction-list"),
  sumCredit: document.getElementById("sum-credit"),
  sumDebit: document.getElementById("sum-debit"),
  closingBalance: document.getElementById("closing-balance"),
  logoutBtn: document.getElementById("logout-btn"),
};

const toast = (msg, tone = "info") => {
  const box = document.getElementById("toast");
  box.textContent = msg;
  box.style.borderColor = tone === "error" ? "#f87171" : "var(--border)";
  box.classList.add("show");
  setTimeout(() => box.classList.remove("show"), 2600);
};

const formatCurrency = (amount, currency = "USD") =>
  new Intl.NumberFormat("en-US", { style: "currency", currency }).format(amount || 0);

const api = async (path, options = {}) => {
  const headers = options.headers ? { ...options.headers } : {};
  const isFormData = options.body instanceof FormData;
  const isUrlEncoded = options.body instanceof URLSearchParams;

  // Attach auth token when available
  if (state.token) headers["Authorization"] = `Bearer ${state.token}`;

  // Only stringify JSON payloads; leave FormData/URLSearchParams intact
  if (options.body && !isFormData && !isUrlEncoded) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
    options.body = JSON.stringify(options.body);
  }

  const res = await fetch(path, { ...options, headers });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || res.statusText);
  }
  return res.json();
};

const setToken = (token) => {
  state.token = token;
  if (token) localStorage.setItem("token", token);
  else localStorage.removeItem("token");
};

const populateAccountSelects = () => {
  const selects = [
    els.depositForm?.account_id,
    els.withdrawForm?.account_id,
    els.transferForm?.from_account_id,
    els.transferForm?.to_account_id,
    els.issueCardForm?.account_id,
    els.cardsAccountFilter,
    els.statementForm?.account_id,
  ];
  selects.forEach((sel) => {
    if (!sel) return;
    sel.innerHTML = "";
    state.accounts.forEach((acc) => {
      const opt = document.createElement("option");
      opt.value = acc.id;
      opt.textContent = `${acc.account_number} · ${acc.currency}`;
      sel.appendChild(opt);
    });
  });
};

const renderAccounts = () => {
  els.accounts.innerHTML = "";
  let total = 0;
  state.accounts.forEach((acc) => {
    total += acc.balance;
    const card = document.createElement("div");
    card.className = "card account-card";
    card.innerHTML = `
      <div class="chip">Acct · ${acc.account_number}</div>
      <p class="label">Balance</p>
      <p class="balance">${formatCurrency(acc.balance, acc.currency)}</p>
      <p class="sub">Status: ${acc.status} • ${acc.currency}</p>
      <p class="sub">Created: ${new Date(acc.created_at).toLocaleString()}</p>
    `;
    els.accounts.appendChild(card);
  });
  els.totalBalance.textContent = formatCurrency(total);
  els.accountCount.textContent = state.accounts.length;
  populateAccountSelects();
};

const fetchAccounts = async () => {
  const accounts = await api("/accounts");
  state.accounts = accounts;
  renderAccounts();
  if (accounts.length) {
    els.cardsAccountFilter.value = accounts[0].id;
    await loadCards(accounts[0].id);
  } else {
    els.cardList.innerHTML = "";
  }
};

const loadCards = async (accountId) => {
  if (!accountId) return;
  const cards = await api(`/cards/account/${accountId}`);
  els.cardList.innerHTML = "";
  cards.forEach((c) => {
    const row = document.createElement("div");
    row.className = "list-item";
    row.innerHTML = `
      <div>
        <div class="label">Card #${c.id}</div>
        <div>${c.expiry_date} • Limit: ${formatCurrency(c.daily_limit)}</div>
      </div>
      <div class="badge ${c.status === "BLOCKED" ? "warn" : "success"}">${c.status}</div>
    `;
    if (c.status !== "BLOCKED") {
      const btn = document.createElement("button");
      btn.textContent = "Block";
      btn.style.width = "auto";
      btn.onclick = async () => {
        await api(`/cards/${c.id}/block`, { method: "PATCH" });
        toast("Card blocked");
        loadCards(accountId);
      };
      row.appendChild(btn);
    }
    els.cardList.appendChild(row);
  });
};

const handleAuth = () => {
  els.signupForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
      await api("/auth/signup", {
        method: "POST",
        body: {
          email: form.get("email"),
          full_name: form.get("full_name"),
          password: form.get("password"),
        },
      });
      toast("Signup successful. Login next.");
      e.target.reset();
    } catch (err) {
      toast(err.message, "error");
    }
  });

  els.loginForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
      const res = await api("/auth/login", {
        method: "POST",
        body: new URLSearchParams({
          username: form.get("email"),
          password: form.get("password"),
        }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      setToken(res.access_token);
      toast("Logged in");
      await fetchAccounts();
    } catch (err) {
      toast(err.message, "error");
    }
  });

  els.logoutBtn?.addEventListener("click", () => {
    setToken(null);
    state.accounts = [];
    renderAccounts();
    els.transactionList.innerHTML = "";
    toast("Logged out");
  });
};

const handleAccounts = () => {
  els.createAccountForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
      await api("/accounts", {
        method: "POST",
        body: { currency: form.get("currency") },
      });
      toast("Account created");
      await fetchAccounts();
    } catch (err) {
      toast(err.message, "error");
    }
  });

  els.refreshAccounts?.addEventListener("click", async () => {
    try {
      await fetchAccounts();
      toast("Accounts refreshed");
    } catch (err) {
      toast(err.message, "error");
    }
  });
};

const handleTransactions = () => {
  const submitJson = (formEl, path) => {
    formEl.addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = new FormData(e.target);
      const payload = Object.fromEntries(form.entries());
      payload.amount = parseFloat(payload.amount);
      payload.account_id && (payload.account_id = Number(payload.account_id));
      payload.from_account_id && (payload.from_account_id = Number(payload.from_account_id));
      payload.to_account_id && (payload.to_account_id = Number(payload.to_account_id));
      if (payload.from_account_id && payload.to_account_id && payload.from_account_id === payload.to_account_id) {
        toast("Select two different accounts", "error");
        return;
      }
      try {
        await api(path, { method: "POST", body: payload });
        toast("Transaction complete");
        await fetchAccounts();
      } catch (err) {
        toast(err.message, "error");
      }
    });
  };

  submitJson(els.depositForm, "/transactions/deposit");
  submitJson(els.withdrawForm, "/transactions/withdraw");
  submitJson(els.transferForm, "/transactions/transfer");
};

const handleCards = () => {
  els.issueCardForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    try {
      await api("/cards/", {
        method: "POST",
        body: {
          account_id: Number(form.get("account_id")),
          expiry_date: form.get("expiry_date"),
          daily_limit: parseFloat(form.get("daily_limit") || "0"),
        },
      });
      toast("Card issued");
      await loadCards(form.get("account_id"));
    } catch (err) {
      toast(err.message, "error");
    }
  });

  els.cardsAccountFilter?.addEventListener("change", (e) => {
    loadCards(e.target.value);
  });
};

const handleStatements = () => {
  const today = new Date();
  const first = new Date(today.getFullYear(), today.getMonth(), 1);
  els.statementForm.from_date.value = first.toISOString().slice(0, 10);
  els.statementForm.to_date.value = today.toISOString().slice(0, 10);

  els.statementForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const accountId = form.get("account_id");
    const from = `${form.get("from_date")}T00:00:00Z`;
    const to = `${form.get("to_date")}T23:59:59Z`;
    try {
      const data = await api(`/statements/account/${accountId}?from_date=${encodeURIComponent(from)}&to_date=${encodeURIComponent(to)}`);
      state.statement = data;
      els.sumCredit.textContent = formatCurrency(data.total_credit);
      els.sumDebit.textContent = formatCurrency(data.total_debit);
      els.closingBalance.textContent = formatCurrency(data.closing_balance);
      els.lastClosing.textContent = formatCurrency(data.closing_balance);
      els.lastRange.textContent = `${new Date(from).toLocaleDateString()} – ${new Date(to).toLocaleDateString()}`;

      els.transactionList.innerHTML = "";
      if (!data.transactions.length) {
        const empty = document.createElement("p");
        empty.className = "sub";
        empty.textContent = "No transactions in this range.";
        els.transactionList.appendChild(empty);
      } else {
        data.transactions
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .forEach((t) => {
            const row = document.createElement("div");
            row.className = "list-item";
            row.innerHTML = `
              <div>
                <div class="label">${new Date(t.created_at).toLocaleString()}</div>
                <div>${t.type}</div>
              </div>
              <div class="badge ${t.type === "CREDIT" ? "success" : "warn"}">${formatCurrency(t.amount)}</div>
            `;
            els.transactionList.appendChild(row);
          });
      }
    } catch (err) {
      toast(err.message, "error");
    }
  });
};

const init = async () => {
  handleAuth();
  handleAccounts();
  handleTransactions();
  handleCards();
  handleStatements();
  if (state.token) {
    try {
      await fetchAccounts();
    } catch {
      setToken(null);
    }
  }
};

init();
