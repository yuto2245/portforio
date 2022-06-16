


<!DOCTYPE html>
<html lanr="ja">
    <head>
        <title>ブラウザメモ</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device=width, initial-scal=1.0">
        <meta name="description"content="ブラウザメモはメモアプリを開くことなくブラウザ上でメモすることができます。文字数もカウントできるので、文章作成に活用してください。">
        <link rel="stylesheet" href="css/memo.css">
        <link rel="stylesheet" href="css/button.css">
        <link rel="stylesheet" href="css/google.com">
        <link rel="stylesheet" href="css/notify.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.icons8.com/fonts/line-awesome/1.1/css/line-awesome-font-awesome.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP&display=swap" rel="stylesheet">
    </head>
    <body>

        <div class="main">
            <h2>ブラウザメモ</h2>
            <div id="notify">
            <p></p>
            </div>
            <div class="section">
                <p>入力フォーム１</p>
                <form action="http://google.com/search" method="get" target="blank">
                <input type="text" name="q" class="textarea1" rows="1"  cols="" placeholder="　タイトル">
                <button class="gbutton" type="submit">Googleで検索</button><br>
                </form>
                <textarea id="1"  class="textarea2" rows="20" cols="" placeholder="　文章を入力・コピー＆ペースト" onkeyup="ShowLength1(value);"></textarea>
                <p id="inputlength1">0文字</p>
                <button id="btn" class="button" type="submit" onclick="copyToClipboard1()">コピーする</button>
            </div>
            <div class="section">
                <p>入力フォーム２</p>
                <textarea class="textarea1" rows="1"  cols="" placeholder="　タイトル"></textarea><br>
                <textarea id="2" class="textarea2" rows="20" cols="" placeholder=" 文章を入力・コピー＆ペースト" onkeyup="ShowLength2(value);"></textarea>
                <p id="inputlength2">0文字</p><button  class="button" onclick="copyToClipboard2()">コピーする</button>
            </div>
            <div class="section">
                <p>入力フォーム３</p>
                <textarea class="textarea1" rows="1"  cols="" placeholder="　タイトル"></textarea><br>
                <textarea id="3" class="textarea2" rows="20" cols="" placeholder="　文章を入力・コピー＆ペースト" onkeyup="ShowLength3(value);"></textarea>
                <p id="inputlength3">0文字</p><button  class="button" onclick="copyToClipboard3()">コピーする</button>
            </div>
        </div>


        <script>//コピー
        function copyToClipboard1() {
            // コピー対象をJavaScript上で変数として定義する
            var copyTarget = document.getElementById("1");

            // コピー対象のテキストを選択する
            copyTarget.select();

            // 選択しているテキストをクリップボードにコピーする
            document.execCommand("Copy");

            // コピーをお知らせする
            document.getElementById("notify").innerHTML = "コピー完了！";
            }

            const Btn = document.getElementById('btn') 　　          // htmlで作成したid=btnを取得
 const test1 = document.getElementById('notify')        // htmlで作成したid=test1を取得

 Btn.addEventListener('click', function(){             // イベントにclickを記述する事によりbtnがクリックされた時というアクションになる
    test1.setAttribute('style', 'display:block;')      // クリックアクション内に記述しているため、クリックされたらcssの記述を追加される
  });

        function copyToClipboard2() {
            // コピー対象をJavaScript上で変数として定義する
            var copyTarget = document.getElementById("2");

            // コピー対象のテキストを選択する
            copyTarget.select();

            // 選択しているテキストをクリップボードにコピーする
            document.execCommand("Copy");

            // コピーをお知らせする
            alert("入力フォーム2の文章をコピーしました！ : " + copyTarget.value);
            }
        
            function copyToClipboard3() {
            // コピー対象をJavaScript上で変数として定義する
            var copyTarget = document.getElementById("3");

            // コピー対象のテキストを選択する
            copyTarget.select();

            // 選択しているテキストをクリップボードにコピーする
            document.execCommand("Copy");

            // コピーをお知らせする
            alert("入力フォーム3の文章をコピーしました！ : " + copyTarget.value);
            }
        </script>


        <script>//文字カウント
         function ShowLength1( str ) {
            document.getElementById("inputlength1").innerHTML = str.length + "文字";
         }

         function ShowLength2( str ) {
            document.getElementById("inputlength2").innerHTML = str.length + "文字";
         }

         function ShowLength3( str ) {
            document.getElementById("inputlength3").innerHTML = str.length + "文字";
         }
        </script>
    </body>
</html>

