[app]
title = Translator
package.name = translator
package.domain = org.brian
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,deep-translator,gtts,pygame==2.1.3
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, RECORD_AUDIO
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r28c

[buildozer]
log_level = 2
