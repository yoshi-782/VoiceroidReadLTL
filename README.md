# VoiceroidReadLTL  
マストドンのLTLを読み上げするPythonコードです。  
  
## 必要なもの  
* vrx(民安☆Talk)  
* Mastodon.py  
* HTMLParser  
  
## 使い方
以下の変数に文字を登録すると、VOICEROIDに読み上げるようにしています。  
```Pyhton
#読み上げたいトゥートの文字列
readWords = ["音留"]
#以下を含むトゥートは除外
filterWords = ["よしおP"]
#除外したいユーザーID
filterID = ["JC", "kiri_bot01"]
```  
また、Listenerクラスの引数、MAXLENGTHに読まれるトゥートの最大文字数を指定できます。デフォルトでは50になってます。 
MAXLENGTHの引数に渡すと繁栄され、指定の文字数を超える場合、「以下略」と省略されます。
  
voiceroid_commandに辞書型で```"コマンド":"プリセット名"```を登録すると、VOICEROID Talk Plusのように使うことができます。
```Python
"c)":"結月ゆかり＞"
```
