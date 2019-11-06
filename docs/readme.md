## How to use? 

# Step1. API TOKENの取得
- 下記を参考にGTMのTOKENを取得してください


# Step2. Config directory以下に設定ファイルを配置する

# Step3. CLI上で下記のコマンドをうつ
```
python setup.py --config <file_name> --tag <CREATE / UPDATE> --trigger <CREATE / UPDATE> --bind <YES / NO>
```
- example)  template.jsonというファイル名の設定ファイルを使って、tagとtriggerを新規に作成し、それらをbindする場合　
```  　　
python setup.py --config template.json --tag CREATE --trigger CREATE --bind YES
```

# GTM　REST APIに関するReference


# Tagに関してのReference 
- https://developers.google.com/tag-manager/api/v2/tag-dictionary-reference

# Triggerに関してのReference
- https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/workspaces/triggers#resource
 


- TODO
  - [x] 新規のtagの作成
  - [x] 既存のtagの更新
  - [x] 新規triggerの作成
  - [x] triggerの更新
  - [x] tagとtriggerのbind
  - [x] Command line tool化
  　--ta c / u --tg c / u  --bind
  - [] 要件の再確認
  - [] 微修正
  - [] Dockernize
