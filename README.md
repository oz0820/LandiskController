# LandiskController

IO DATA のLANDISKをスクリプトでシャットダウンするコードです。  
設計が不十分なので、**実行時に Internal Server Error が発生**します。

とりあえず動作する状態なので、十分検討した上で使用してください。

Var 1.20で動作確認しています


#### 実行可能バイナリについて
nuitkaを入れて、次のコードを実行すれば良い感じになると思います。
```
nuitka --standalone --onefile LandiskShutdowner.py
```
