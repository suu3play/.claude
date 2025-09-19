# 次回作業読込・実行コマンド

## 概要
指定されたプロジェクトの次回作業用ファイルを読み込み、段階的に作業を実行するカスタムスラッシュコマンドです。

## 使用方法
```
/load-next-work <プロジェクト名>
```

## 機能
- 指定プロジェクトの次回作業ファイルを自動検索
- 連番ファイルがある場合は順次読み込み・実行
- ファイル読み込み状況をプレフィックスで管理
- 作業完了状況をプレフィックスで管理

## ファイル命名規則
- 読み込み済み: `[READ]_next-work.md`
- 作業完了: `[DONE]_next-work.md`

## 実行コード

```javascript
const fs = require('fs');
const path = require('path');

// プロジェクトディレクトリのパスを取得
const getProjectPath = (projectName) => {
    const baseDir = process.cwd();
    const projectPath = path.join(baseDir, projectName);

    if (fs.existsSync(projectPath)) {
        return projectPath;
    }

    // 現在のディレクトリで検索
    const currentDirName = path.basename(baseDir);
    if (currentDirName === projectName) {
        return baseDir;
    }

    throw new Error(`プロジェクト "${projectName}" が見つかりません`);
};

// 次回作業ファイルを検索
const findNextWorkFiles = (projectDir) => {
    const files = fs.readdirSync(projectDir);

    // 読み込み済み・完了済みファイルを除外
    const nextWorkFiles = files
        .filter(f => f.match(/^(?!\[READ\]_|\[DONE\]_)next-work(-\d+)?\.md$/))
        .sort();

    return nextWorkFiles.map(fileName => ({
        fileName,
        fullPath: path.join(projectDir, fileName),
        phase: fileName.match(/next-work-(\d+)\.md$/) ? parseInt(fileName.match(/next-work-(\d+)\.md$/)[1]) : 1
    }));
};

// ファイルをリネーム（読み込み済みマーク）
const markAsRead = (filePath) => {
    const dir = path.dirname(filePath);
    const fileName = path.basename(filePath);
    const newPath = path.join(dir, `[READ]_${fileName}`);

    fs.renameSync(filePath, newPath);
    return newPath;
};

// ファイルをリネーム（完了マーク）
const markAsCompleted = (filePath) => {
    const dir = path.dirname(filePath);
    const fileName = path.basename(filePath).replace(/^\[READ\]_/, '');
    const newPath = path.join(dir, `[DONE]_${fileName}`);

    fs.renameSync(filePath, newPath);
    return newPath;
};

// 作業ファイルの内容を解析
const parseWorkFile = (filePath) => {
    const content = fs.readFileSync(filePath, 'utf8');

    // チェックリストを抽出
    const checklistRegex = /- \[ \]\s*(.+)/g;
    const tasks = [];
    let match;

    while ((match = checklistRegex.exec(content)) !== null) {
        tasks.push({
            description: match[1].trim(),
            completed: false
        });
    }

    // セクション別に分類
    const sections = {
        next: [],
        inProgress: [],
        completed: []
    };

    const lines = content.split('\n');
    let currentSection = '';

    for (const line of lines) {
        if (line.includes('次回実施事項')) {
            currentSection = 'next';
        } else if (line.includes('進行中の作業')) {
            currentSection = 'inProgress';
        } else if (line.includes('完了済み')) {
            currentSection = 'completed';
        } else if (line.match(/- \[ \]\s*(.+)/) && currentSection) {
            const taskMatch = line.match(/- \[ \]\s*(.+)/);
            if (taskMatch) {
                sections[currentSection].push({
                    description: taskMatch[1].trim(),
                    completed: false
                });
            }
        }
    }

    return {
        content,
        tasks: sections,
        allTasks: tasks
    };
};

// 作業を段階的に実行
const executeWorkPhase = async (workFile, phaseNumber) => {
    console.log(`\n=== フェーズ ${phaseNumber}: ${workFile.fileName} ===`);

    // ファイルを読み込み済みとしてマーク
    const readPath = markAsRead(workFile.fullPath);
    console.log(`✓ ファイルを読み込み済みとしてマーク: ${path.basename(readPath)}`);

    // 作業内容を解析
    const workData = parseWorkFile(readPath);

    console.log(`\n📋 作業項目 (フェーズ ${phaseNumber}):`);

    // 次回実施事項の作業を表示
    if (workData.tasks.next.length > 0) {
        console.log(`\n📝 次回実施事項`);
        workData.tasks.next.forEach((task, index) => {
            console.log(`  ${index + 1}. ${task.description}`);
        });
    }

    // 進行中の作業を表示
    if (workData.tasks.inProgress.length > 0) {
        console.log(`\n🔄 進行中の作業`);
        workData.tasks.inProgress.forEach((task, index) => {
            console.log(`  ${index + 1}. ${task.description}`);
        });
    }

    // 完了済みの作業を表示
    if (workData.tasks.completed.length > 0) {
        console.log(`\n✅ 完了済み`);
        workData.tasks.completed.forEach((task, index) => {
            console.log(`  ${index + 1}. ${task.description}`);
        });
    }

    console.log(`\n📝 技術的な注意点やコンテキストは読み込み済みファイルを確認してください`);
    console.log(`   ファイル: ${readPath}`);

    // ユーザーに作業完了確認
    console.log(`\n❓ このフェーズの作業を完了しましたか？ (y/n)`);

    // 実際の実装では、ユーザー入力を待つ処理を追加
    // 今回はデモとして自動で完了とする
    const completed = true; // 実際はユーザー入力を受け取る

    if (completed) {
        const completedPath = markAsCompleted(readPath);
        console.log(`✅ フェーズ ${phaseNumber} 完了: ${path.basename(completedPath)}`);
        return true;
    }

    return false;
};

// メイン実行関数
const loadNextWork = async (args) => {
    if (args.length === 0) {
        console.error('❌ プロジェクト名を指定してください');
        console.log('使用方法: /load-next-work <プロジェクト名>');
        return;
    }

    const projectName = args[0];
    console.log(`🚀 プロジェクト "${projectName}" の次回作業を開始します...`);

    try {
        // プロジェクトディレクトリを取得
        const projectDir = getProjectPath(projectName);
        console.log(`📁 プロジェクトディレクトリ: ${projectDir}`);

        // 次回作業ファイルを検索
        const workFiles = findNextWorkFiles(projectDir);

        if (workFiles.length === 0) {
            console.log('📄 次回作業ファイルが見つかりません');
            console.log('先に /save-next-work コマンドで作業ファイルを作成してください');
            return;
        }

        console.log(`📋 発見された作業ファイル: ${workFiles.length}個`);
        workFiles.forEach(file => {
            console.log(`  - ${file.fileName} (フェーズ ${file.phase})`);
        });

        // 各フェーズを順次実行
        for (let i = 0; i < workFiles.length; i++) {
            const success = await executeWorkPhase(workFiles[i], workFiles[i].phase);

            if (!success) {
                console.log(`⏸️  フェーズ ${workFiles[i].phase} で作業を中断しました`);
                break;
            }

            // 次のフェーズがある場合の確認
            if (i < workFiles.length - 1) {
                console.log(`\n➡️  次のフェーズに進みますか？ (y/n)`);
                // 実際の実装では、ユーザー入力を待つ
                const continueNext = true; // デモ用

                if (!continueNext) {
                    console.log(`⏸️  作業を中断しました。次回は残りのフェーズから継続できます`);
                    break;
                }
            }
        }

        console.log(`\n🎉 全ての作業フェーズが完了しました！`);

    } catch (error) {
        console.error(`❌ エラー: ${error.message}`);
    }
};

// コマンド実行
module.exports = loadNextWork;
```

## 設定

Claude Code の設定ファイル (`.claude/settings.local.json`) に以下を追加:

```json
{
  "customCommands": {
    "load-next-work": {
      "file": ".claude/commands/load-next-work.md",
      "description": "次回作業ファイルを読み込んで実行"
    }
  }
}
```

## 使用例

1. **作業保存**
   ```
   /save-next-work API認証機能の実装
   ```

2. **作業読み込み・実行**
   ```
   /load-next-work my-project
   ```

## ファイル状態の遷移

```
next-work.md
  ↓ (読み込み時)
[READ]_next-work.md
  ↓ (完了時)
[DONE]_next-work.md
```