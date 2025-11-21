module.exports = {
  apps: [
    {
      name: "magic-app",
      script: "./.output/server/index.mjs",
      env: {
        PORT: 3001,
      },
    },
  ],
}
