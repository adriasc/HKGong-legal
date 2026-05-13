(() => {
  const form = document.querySelector("#starter-signup-form");
  if (!form) return;

  const status = document.querySelector("#starter-signup-status");
  const mailchimpAction = (form.dataset.mailchimpAction || "").trim();
  const fallbackAction = (form.dataset.fallbackAction || "").trim();

  if (mailchimpAction) {
    form.action = mailchimpAction;
    form.method = "post";
    form.enctype = "application/x-www-form-urlencoded";
    form.target = "_blank";
    return;
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const emailInput = form.querySelector("input[name='EMAIL']");
    const email = emailInput ? emailInput.value.trim() : "";
    if (!email || !emailInput.checkValidity()) {
      if (status) status.textContent = "Enter a valid email address.";
      if (emailInput) emailInput.focus();
      return;
    }

    const subject = "Send me the HKGong Starter Guide";
    const body = [
      "Please add me to the HKGong starter guide list.",
      "",
      `Email: ${email}`,
      "Source: hkgong-website-starter-guide",
    ].join("\n");

    const mailto = fallbackAction || "mailto:hello@hkgong.com";
    const separator = mailto.includes("?") ? "&" : "?";
    window.location.href = `${mailto}${separator}body=${encodeURIComponent(body)}&subject=${encodeURIComponent(subject)}`;

    if (status) {
      status.textContent = "Opening your email app while the newsletter form is being connected.";
    }
  });
})();
