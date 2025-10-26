1. 開発ワークフローの読み込み

    - [プロジェクトルート]\.claude\rules\development-workflow.md を読み込む
    - 必要に応じて関連するルール・テンプレートファイルを読み込む

2. Issue 分析と改修計画立案
    - 指定された[プロジェクト名]のディレクトリに移動し、gh issue view [issue 番号] で読み込む
    - issue 内容を分析し、実装要件を整理
    - 開発ワークフローに基づいた改修計画を策定
    - TodoWrite ツールを使用した作業計画の作成
    - コミット以降の作業は行わない

使用方法

/issue [プロジェクト名]　[issue 番号]

例：

-   /issue portfolio 7
-   /issue portfolio 15
