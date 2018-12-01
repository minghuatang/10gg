apps = [
]

urls = [
    (r'/api/alert', 'api.AlertHandler'),
    (r'/api/log/pull', 'api.LogPullHandler'),
    (r'/api/log/tips', 'api.LogTipsHandler'),
    (r'/api/log', 'api.LogFilterHandler'),
]
