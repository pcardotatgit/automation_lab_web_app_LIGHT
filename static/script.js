// used by the code editor features

// Initialize CodeMirror
const editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
  lineNumbers: true,
  mode: "python",
  theme: "default",
});

