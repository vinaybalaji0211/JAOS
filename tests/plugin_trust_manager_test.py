from brain.plugin_trust_manager import (
    PluginTrustManager
)


trusted_plugin = {
    "name": "Weather Plugin",
    "trust_score": 85,
    "permissions": [
        "web_access"
    ],
    "status": "ACTIVE"
}

review_plugin = {
    "name": "Unknown Plugin",
    "trust_score": 55,
    "permissions": [
        "web_access"
    ],
    "status": "REGISTERED"
}

blocked_plugin = {
    "name": "Danger Plugin",
    "trust_score": 90,
    "permissions": [
        "access_secrets",
        "delete_file"
    ],
    "status": "ACTIVE"
}

PluginTrustManager.show_decision(
    trusted_plugin
)

PluginTrustManager.show_decision(
    review_plugin
)

PluginTrustManager.show_decision(
    blocked_plugin
)