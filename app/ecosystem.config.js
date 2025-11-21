module.exports = {
  apps: [
    {
      name: "django-app",
      script: "/root/infographs/app/django_start.sh",
      interpreter: "/bin/bash",
      cwd: "/root/infographs/app",
      env: {
        DJANGO_SETTINGS_MODULE: "app.settings.production",
      },
    },
  ],
}
