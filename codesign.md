## Step 1
    对于SteamMetal.4.01.01.app 的签名做了以下改动，

### 1. 删除了c_driver 
### 2. mv /Users/lijiaxi/Documents/sparkleOldApp/SteamMetal.4.01.01.app/Contents/Frameworks/renderer/d3dmetal \
    /Users/lijiaxi/Documents/sparkleOldApp/SteamMetal.4.01.01.app/Contents/Resources/

### 3 运行 sign_wine_app.sh

chmod +x sign_wine_app.sh

codesign --display --verbose=4 ./SteamDxvk.4.01.01.app 

验证codesign 是否成功


### 4 create dmg
hdiutil create -volname SteamMetalApp -srcfolder ./SteamMetal.4.01.01.app -ov -format UDZO SteamMetal.4.01.01.dmg

hdiutil create -volname "SteamDxvkApp" -srcfolder ./SteamDxvk.4.01.01.app -ov -format UDZO SteamDxvk.4.01.01.dmg


### 5 upload dmg to web

### 6 download to folder or SSD folder

### 7  run app 先绕过privicy里的设置，就可以运行

### 8  正式发布时需要AppleID 签名



