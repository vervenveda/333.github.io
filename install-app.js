(() => {
  "use strict";

  let deferredPrompt = null;
  let promptInProgress = false;
  let observer = null;

  const INSTALL_SELECTOR = "[data-install-app]";
  const HELP_SELECTOR = "[data-install-help]";

  function installButtons() {
    return Array.from(document.querySelectorAll(INSTALL_SELECTOR));
  }

  function installHelp() {
    return document.querySelector(HELP_SELECTOR);
  }

  function isStandalone() {
    return Boolean(
      window.matchMedia?.("(display-mode: standalone)").matches ||
      window.navigator.standalone === true
    );
  }

  function rememberOriginalLabel(button) {
    if (!button.dataset.originalLabel) {
      button.dataset.originalLabel = button.textContent.trim() || "Install App";
    }
  }

  function setButtonLabel(button, label) {
    button.textContent = label;
  }

  function setButtonState(mode) {
    installButtons().forEach(button => {
      rememberOriginalLabel(button);

      button.hidden = mode === "installed";
      button.disabled = mode === "prompting";
      button.dataset.installReady = String(mode === "ready");
      button.dataset.installState = mode;

      if (mode === "installed") {
        setButtonLabel(button, "Installed");
        return;
      }

      if (mode === "ready") {
        setButtonLabel(
          button,
          button.dataset.installLabel || "Install App"
        );
        return;
      }

      if (mode === "prompting") {
        setButtonLabel(
          button,
          button.dataset.installingLabel || "Opening Install…"
        );
        return;
      }

      setButtonLabel(
        button,
        button.dataset.instructionsLabel || "Installation Help"
      );
    });
  }

  function platformInstructions() {
    const userAgent = navigator.userAgent || "";
    const isIOS = /iPhone|iPad|iPod/i.test(userAgent);
    const isAndroid = /Android/i.test(userAgent);
    const isMac = /Macintosh|Mac OS X/i.test(userAgent);
    const isWindows = /Windows/i.test(userAgent);

    const lines = [
      "Install 333 Network from your browser:",
      ""
    ];

    if (isIOS) {
      lines.push(
        "• iPhone or iPad / Safari: tap Share, then choose Add to Home Screen."
      );
    } else if (isAndroid) {
      lines.push(
        "• Android / Chrome: open the browser menu, then choose Install app or Add to Home screen."
      );
    } else if (isWindows) {
      lines.push(
        "• Windows / Edge: open the browser menu, choose Apps, then Install this site as an app.",
        "• Windows / Chrome: use the install icon in the address bar or choose Install 333 Network from the browser menu."
      );
    } else if (isMac) {
      lines.push(
        "• macOS / Safari: choose File, then Add to Dock.",
        "• macOS / Chrome or Edge: use the install icon in the address bar or the browser's Apps menu."
      );
    }

    lines.push(
      "",
      "Other supported browsers:",
      "• Chrome or Edge: look for an install icon in the address bar or browser menu.",
      "• Safari on iPhone or iPad: Share → Add to Home Screen.",
      "",
      "Installation controls vary by browser and operating system.",
      "The installed 333 Network opens within this repository's application scope."
    );

    return lines.join("\n");
  }

  function showInstructions() {
    const message = platformInstructions();
    const help = installHelp();

    if (help) {
      help.hidden = false;
      help.textContent = message;
      help.setAttribute("tabindex", "-1");
      help.focus({ preventScroll: true });
      help.scrollIntoView({
        behavior: window.matchMedia?.("(prefers-reduced-motion: reduce)").matches
          ? "auto"
          : "smooth",
        block: "nearest"
      });
      return;
    }

    window.alert(message);
  }

  function hideInstructions() {
    const help = installHelp();
    if (!help) return;

    help.hidden = true;
    help.textContent = "";
  }

  function markInstalled() {
    deferredPrompt = null;
    promptInProgress = false;
    hideInstructions();
    setButtonState("installed");

    document.dispatchEvent(
      new CustomEvent("333-app-installed")
    );
  }

  async function requestInstallation(button) {
    if (promptInProgress) return;

    if (isStandalone()) {
      markInstalled();
      return;
    }

    if (!deferredPrompt) {
      showInstructions();
      return;
    }

    promptInProgress = true;
    setButtonState("prompting");

    const promptEvent = deferredPrompt;
    deferredPrompt = null;

    try {
      await promptEvent.prompt();
      const choice = await promptEvent.userChoice;

      if (choice?.outcome === "accepted") {
        installButtons().forEach(currentButton => {
          currentButton.disabled = true;
          currentButton.dataset.installState = "accepted";
          setButtonLabel(
            currentButton,
            currentButton.dataset.acceptedLabel || "Installation Requested"
          );
        });

        document.dispatchEvent(
          new CustomEvent("333-app-install-accepted")
        );
      } else {
        promptInProgress = false;
        setButtonState("help");

        document.dispatchEvent(
          new CustomEvent("333-app-install-dismissed")
        );
      }
    } catch (error) {
      console.warn("333 Network install prompt failed:", error);
      promptInProgress = false;
      setButtonState("help");
      showInstructions();
    }
  }

  function initializeButtons() {
    if (isStandalone()) {
      setButtonState("installed");
      return;
    }

    setButtonState(deferredPrompt ? "ready" : "help");
  }

  window.addEventListener("beforeinstallprompt", event => {
    event.preventDefault();
    deferredPrompt = event;
    promptInProgress = false;
    hideInstructions();
    setButtonState("ready");

    document.dispatchEvent(
      new CustomEvent("333-app-install-ready")
    );
  });

  window.addEventListener("appinstalled", markInstalled);

  window.matchMedia?.("(display-mode: standalone)")
    .addEventListener?.("change", event => {
      if (event.matches) markInstalled();
      else initializeButtons();
    });

  document.addEventListener("click", event => {
    const button = event.target.closest(INSTALL_SELECTOR);
    if (!button) return;

    event.preventDefault();
    requestInstallation(button);
  });

  document.addEventListener("keydown", event => {
    if (event.key !== "Escape") return;

    const help = installHelp();
    if (help && !help.hidden) {
      hideInstructions();
      installButtons()[0]?.focus();
    }
  });

  document.addEventListener("DOMContentLoaded", initializeButtons, {
    once: true
  });

  if (document.readyState !== "loading") {
    initializeButtons();
  }

  observer = new MutationObserver(mutations => {
    const addedInstallControl = mutations.some(mutation =>
      Array.from(mutation.addedNodes).some(node =>
        node.nodeType === Node.ELEMENT_NODE &&
        (
          node.matches?.(INSTALL_SELECTOR) ||
          node.querySelector?.(INSTALL_SELECTOR)
        )
      )
    );

    if (addedInstallControl) initializeButtons();
  });

  observer.observe(document.documentElement, {
    childList: true,
    subtree: true
  });
})();
