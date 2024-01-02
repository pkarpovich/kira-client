module.exports = {
    apps: [
        {
            name: 'kira-client',
            script: 'poetry run python kira_client/main.py',
            interpreter: 'none',
            cwd: '/home/pi/kira-client',
            env: {},
        }
    ]
};