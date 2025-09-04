# pymemo

This is a modest application built using Python and Tkinter.

## Features

*   Create, save, and manage your notes.
*   Search your memos with regular expressions.
*   Keyword highlighting.
*   Link to other memos using `[[memo_name]]` syntax.
*   Automatically detects and opens URLs.
*   Organize memos with tags.

## How to Run

1.  Install the dependencies (though there don't seem to be any external ones besides what's built-in to Python).
2.  Run the application:
    ```bash
    python pymemo.py
    ```

## Configuration

To configure the application, first copy the `config.pymemo` directory from the project root to your home directory and rename it to `.pymemo`.

For example, on Windows, you would copy `config.pymemo` to `C:\Users\<YourUsername>\.pymemo`.

The configuration file will then be located at `~/.pymemo/config`.

You can specify the directory where your memos are stored by setting the `work_dir` option in this file.

Example:
```ini
[Main]
WORK_DIR = D:\path\to\your\memos
```

## History

This application was originally developed around 2005 for Python 2, and has now been updated to run on Python 3.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# pymemo (日本語)

PythonとTkinterで構築された、シンプルなグラフィカルユーザーインターフェースを持つささやかなアプリケーションです。

## 特徴

*   ノートの作成、保存、管理
*   正規表現によるメモの検索
*   キーワードのハイライト
*   `[[メモ名]]`構文を使用した他のメモへのリンク
*   URLの自動検出とオープン
*   タグによるメモの整理

## 実行方法

1.  依存関係をインストールします（Pythonに組み込まれているもの以外に外部の依存関係はないようです）。
2.  アプリケーションを実行します:
    ```bash
    python pymemo.py
    ```

## 設定

アプリケーションを設定するには、まずプロジェクトのルートにある`config.pymemo`ディレクトリをホームディレクトリにコピーし、`.pymemo`に名前を変更します。

例えば、Windowsの場合、`config.pymemo`を`C:\Users\<ユーザー名>\.pymemo`にコピーします。

その後、設定ファイルは`~/.pymemo/config`に配置されます。

このファイルの`work_dir`オプションで、メモを保存するディレクトリを指定できます。

例:
```ini
[Main]
WORK_DIR = D:\path\to\your\memos
```

## 経緯

このアプリケーションは元々2005年頃にPython 2向けに開発され、今回Python 3で動作するように更新されました。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。