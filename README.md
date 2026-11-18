# oppaypay-desktop

⚠️ **警告 / WARNING** ⚠️

このライブラリは、PayPayの**Web版ポータルサイト**のAPIを模倣して動作します。  
本家 `oppaypay` (モバイルアプリエミュレーション) と比較して、以下の重大な制約とリスクがあります。利用前に必ずお読みください。

## 🚨 重要な注意事項

1. **本家 `oppaypay` より下位互換です(サポートもほぼできません）**  
   モバイル版APIが提供する高度な機能（詳細な残高内訳、特定のP2P機能、堅牢なセッション維持など）の多くは、Web版APIでは提供されていないか、仕様が異なります。

2. **大規模な利用は強くお勧めしません**  
   Web版のAPIは、短時間での連続アクセスや自動化されたパターンに対して、モバイル版よりもはるかに厳しいレートリミットやボット検知（WAF）を適用する傾向があります。アカウントの一時凍結や機能制限のリスクが高まります。

3. **`webtoken` はすぐに死にます**  
   Web版で発行されるアクセストークン (`access_token`) は、有効期限が非常に短く設定されているか、不正利用検知システムによって即座に無効化（Kill）される仕様となっています。長時間のバッチ処理や常駐型ボットでのセッション維持は現実的ではありません。

---

## 📦 インストール

```bash
pip install -r requirements.txt
```
# Let's go
```
from oppaypay_desktop import PayPayDesktop

# 認証情報の設定
PHONE = "07012345678"
PASSWORD = "your_password"

try:
    # クライアントの初期化とログイン
    client = PayPayDesktop(phone=PHONE, password=PASSWORD)
    client.login()
    
    # 残高の取得（例）
    balance = client.get_balance()
    print(f"残高: {balance}")

except Exception as e:
    print(f"エラーが発生しました: {e}")
```
---

### 💡 実装上のポイント
 **`_webgl.json` の活用**: 将来的にブラウザのフィンガープリント偽装が必要になった際、このJSONを読み込んでリクエストヘッダーやTLS設定に反映させる拡張が可能です。

このスケルトンをベースに、実際にキャプチャしたWeb版のAPIエンドポイントを `client.py` に追加していくことで、目的の機能を実装できます。
