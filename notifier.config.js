module.exports = {
	apps: [{
		name: "Capitol Trading Notifier",
		script: "./main.py",
		interpreter: "/usr/bin/python3.8"
		instances: 1,
		exec_mode: "fork",
		cron_restart: "0 8 * * *",
		watch: false,
		autorestart: false
	},
	{
		name: "Capitol Trading Notifier",
		script: "./main.py",
		interpreter: "/usr/bin/python3.8"
		instances: 1,
		exec_mode: "fork",
		cron_restart: "0 23 * * *",
		watch: false,
		autorestart: false
	}]
}
