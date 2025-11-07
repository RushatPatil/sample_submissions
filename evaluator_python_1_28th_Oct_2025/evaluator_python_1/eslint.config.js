// eslint.config.js
import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    rules: {
      "no-undef": "error",
      "no-unused-vars": "error",
      "semi": "error",
      "no-unreachable": "error",
      "no-extra-semi": "error"
    }
  }
];
