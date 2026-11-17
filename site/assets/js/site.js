/* TL Propreté — menu mobile et formulaire de devis */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");

  /* Menu mobile */
  var toggle = document.querySelector(".menu-toggle");
  var menu = document.getElementById("menu-mobile");
  function setMenu(open) {
    document.body.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.querySelector(".menu-toggle-label").textContent = open ? "Fermer" : "Menu";
    if (open) { menu.removeAttribute("inert"); var f = menu.querySelector("a"); if (f) f.focus(); }
    else { menu.setAttribute("inert", ""); }
  }
  if (toggle && menu) {
    menu.setAttribute("inert", "");
    toggle.addEventListener("click", function () { setMenu(!document.body.classList.contains("menu-open")); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && document.body.classList.contains("menu-open")) { setMenu(false); toggle.focus(); } });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  }

  /* Formulaire de devis : envoi sans rechargement, avec repli classique si JS absent */
  var form = document.getElementById("form-devis");
  if (!form) return;
  var status = form.querySelector(".form-status");
  var started = form.querySelector('input[name="t"]');
  if (started) started.value = String(Math.floor(Date.now() / 1000));

  function show(msg, isError) {
    status.textContent = msg;
    status.classList.add("is-shown");
    status.classList.toggle("is-error", !!isError);
    status.setAttribute("tabindex", "-1");
    status.focus();
  }
  function fieldError(el, msg) {
    var wrap = el.closest(".field");
    var err = wrap.querySelector(".field-error");
    if (!err) { err = document.createElement("p"); err.className = "field-error"; err.id = el.id + "-err"; wrap.appendChild(err); }
    err.textContent = msg;
    el.setAttribute("aria-invalid", "true");
    el.setAttribute("aria-describedby", err.id);
  }
  function clearErrors() {
    [].forEach.call(form.querySelectorAll("[aria-invalid]"), function (el) { el.removeAttribute("aria-invalid"); el.removeAttribute("aria-describedby"); });
    [].forEach.call(form.querySelectorAll(".field-error"), function (el) { el.remove(); });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    clearErrors();
    var first = null;
    [].forEach.call(form.querySelectorAll("[required]"), function (el) {
      var v = el.value.trim();
      var bad = !v || (el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v));
      if (bad) {
        fieldError(el, !v ? "Ce champ est nécessaire pour préparer le devis." : "Cette adresse e-mail n'est pas valide. Exemple : nom@domaine.fr");
        if (!first) first = el;
      }
    });
    if (first) { first.focus(); return; }

    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true; btn.textContent = "Envoi en cours…";
    fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
      .then(function (res) {
        if (res && res.ok) {
          form.reset();
          show("Demande envoyée. Nous vous répondons sous 24 heures ouvrées pour convenir d'une visite.", false);
        } else {
          show((res && res.error) || "L'envoi n'a pas abouti. Réessayez, ou écrivez-nous à contact@tlproprete.fr.", true);
        }
      })
      .catch(function () { show("L'envoi n'a pas abouti : vérifiez votre connexion, ou écrivez-nous à contact@tlproprete.fr.", true); })
      .then(function () { btn.disabled = false; btn.textContent = "Envoyer ma demande"; });
  });
})();

/* Pré-sélection de la prestation depuis les pages prestations (?prestation=...) */
(function () {
  var sel = document.getElementById("f-prestation");
  if (!sel || !window.URLSearchParams) return;
  var v = new URLSearchParams(location.search).get("prestation");
  if (v && sel.querySelector('option[value="' + v.replace(/[^a-z0-9-]/g, "") + '"]')) sel.value = v;
})();
