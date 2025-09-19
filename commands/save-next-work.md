# 次回作業保存コマンド

## 概要
現在の作業状況と次回実施すべき作業内容をMarkdownファイルとして出力し、次回の作業継続を効率的に行えるようにするカスタムスラッシュコマンドです。

## 使用方法
```
/save-next-work [作業内容の説明]
```

## 機能
- 現在のプロジェクト状況を分析
- 次回実施すべき作業項目をリスト化
- 適切なファイル名で次回作業用ファイルを生成
- 作業フェーズが複数ある場合は連番付きで複数ファイルを生成

## 出力ファイル形式
- 基本: `next-work.md`
- 複数フェーズ: `next-work-01.md`, `next-work-02.md`, ...

## 実行コード

```javascript
const fs = require('fs');
const path = require('path');

// 現在のプロジェクト名を取得
const getCurrentProjectName = () => {
    const cwd = process.cwd();
    return path.basename(cwd);
};

// 既存の次回作業ファイルをチェック
const getNextFileNumber = (projectDir) => {
    const files = fs.readdirSync(projectDir);
    const nextWorkFiles = files.filter(f => f.match(/^next-work(-\d+)?\.md$/));

    if (nextWorkFiles.length === 0) return '';

    const numbers = nextWorkFiles
        .map(f => f.match(/next-work-(\d+)\.md$/))
        .filter(m => m)
        .map(m => parseInt(m[1]));

    if (numbers.length === 0) return '-02';

    const maxNum = Math.max(...numbers);
    return `-${String(maxNum + 1).padStart(2, '0')}`;
};

// 現在の作業状況を分析
const analyzeCurrentWork = async () => {
    // GitHubの課題やPRを確認
    let analysis = {
        currentBranch: '',
        uncommittedChanges: false,
        issues: [],
        prs: [],
        recentCommits: []
    };

    try {
        // Git ブランチ確認
        const { execSync } = require('child_process');
        analysis.currentBranch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();

        // 未コミット変更確認
        const status = execSync('git status --porcelain', { encoding: 'utf8' });
        analysis.uncommittedChanges = status.length > 0;

        // 最近のコミット取得
        const commits = execSync('git log --oneline -5', { encoding: 'utf8' });
        analysis.recentCommits = commits.split('\n').filter(l => l.trim());

    } catch (error) {
        console.log('Git情報の取得に失敗しました');
    }

    return analysis;
};

// 次回作業ファイルを生成
const generateNextWorkFile = (projectName, workDescription, analysis) => {
    const timestamp = new Date().toISOString().split('T')[0];
    const projectDir = process.cwd();
    const fileNumber = getNextFileNumber(projectDir);
    const fileName = `next-work${fileNumber}.md`;
    const filePath = path.join(projectDir, fileName);

    const content = `# 次回作業: ${projectName}

## 作業概要
${workDescription || '継続作業'}

## 作成日時
${timestamp}

## 現在の状況

### Git状況
- ブランチ: ${analysis.currentBranch || 'N/A'}
- 未コミット変更: ${analysis.uncommittedChanges ? 'あり' : 'なし'}

### 最近のコミット
${analysis.recentCommits.map(c => `- ${c}`).join('\n') || '- なし'}

## 次回実施事項

- [ ]
- [ ]
- [ ]

## 進行中の作業

- [ ]
- [ ]

## 完了済み

- [x]

## 技術的な注意点

### 前回からの継続課題
-

### 新たに発見した課題
-

## 参考資料・リンク
-
-

## 備考
-
`;

    fs.writeFileSync(filePath, content);
    return { fileName, filePath };
};

// メイン実行関数
const saveNextWork = async (args) => {
    const workDescription = args.join(' ');
    const projectName = getCurrentProjectName();

    console.log(`プロジェクト "${projectName}" の次回作業を保存中...`);

    const analysis = await analyzeCurrentWork();
    const result = generateNextWorkFile(projectName, workDescription, analysis);

    console.log(`✓ 次回作業ファイルを生成しました: ${result.fileName}`);
    console.log(`  パス: ${result.filePath}`);

    // ファイルの内容をエディタで開くかどうか確認
    console.log(`\n次回作業ファイルを編集しますか？ (y/n)`);

    return result;
};

// コマンド実行
module.exports = saveNextWork;
```

## 設定

Claude Code の設定ファイル (`.claude/settings.local.json`) に以下を追加:

```json
{
  "customCommands": {
    "save-next-work": {
      "file": ".claude/commands/save-next-work.md",
      "description": "次回作業用ファイルを生成"
    }
  }
}
```