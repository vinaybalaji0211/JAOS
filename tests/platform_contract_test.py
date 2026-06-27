from platform.platform_contract import PlatformContract

platform = PlatformContract(
    "Memory Platform"
)

platform.initialize()
platform.start()
platform.pause()
platform.resume()
platform.stop()

platform.show_status()

print(
    platform.health()
)