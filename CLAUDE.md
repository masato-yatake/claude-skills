# このリポジトリ：masato-yatake/claude-skills
Claude Code スキルの公開マーケットプレイス（Public・MIT）。

セッション開始時：
1. `git remote -v` の origin と、かんばんの「■ リポジトリ」を照合する。不一致なら作業せず「リポ不一致：origin=〜／かんばん=〜」とだけ報告して止まる。
2. 一致したら `git fetch && git pull --ff-only`。
最初の報告は「1行目：origin=〜／かんばん=一致」「2行目：pull の結果」で始める。

運用ルール：
- スキルの正本はこのリポ。デスクトップアプリの Skills 設定はここから入れ直す。
- 変更は claude/〜 ブランチ＋PR。マージは Masato。
- 公開リポなので、農場固有の情報（住所・金額・氏名以外の個人情報）は書かない。
- 変更後は `claude plugin validate .` を通す。
