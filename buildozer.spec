[app]

title = احترم نفسك

package.name = ehtaremnafsak
package.domain = org.ehtaremnafsak

source.dir = .

source.include_exts = py,png,jpg,jpeg,wav,mp3,kv,atlas

version = 1.0

requirements = python3,kivy,pyjnius

orientation = portrait

fullscreen = 1

android.api = 35
android.minapi = 23

android.archs = arm64-v8a,armeabi-v7a

android.permissions = RECORD_AUDIO,FOREGROUND_SERVICE,FOREGROUND_SERVICE_MICROPHONE,WAKE_LOCK,POST_NOTIFICATIONS

android.private_storage = True

android.accept_sdk_license = True

services = service_main.py:main

android.enable_androidx = True

android.gradle_dependencies = androidx.core:core:1.15.0

[buildozer]

log_level = 2

warn_on_root = 1